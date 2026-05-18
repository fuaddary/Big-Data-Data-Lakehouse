from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, drop_duplicates, coalesce, lit
from delta import configure_spark_with_delta_pip

# 1. Konfigurasi SparkSession
builder = SparkSession.builder.appName("SilverTransformation") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder, extra_packages=["io.delta:delta-spark_2.12:3.1.0"]).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print("--- Menjalankan Proses Transformasi ke Layer Silver ---")

# 2. Baca dari Bronze Layer (Delta format)
bronze_path = "./data/bronze/transactions"
bronze_df = spark.read.format("delta").load(bronze_path)

print(f"Jumlah data di Bronze: {bronze_df.count()}")

# 3. Data Cleaning (Transformasi ke Silver)
silver_df = bronze_df \
    .dropDuplicates(["transaction_id"]) \
    .filter(col("amount").isNotNull() & (col("amount") != "")) \
    .fillna({"status": "UNKNOWN"}) \
    .withColumn("amount", col("amount").cast("double")) \
    .withColumn("transaction_date", to_timestamp(col("transaction_date")))

# Tampilkan sample hasil cleaning
print("Sample Data Bersih (Silver):")
silver_df.show(5)
print(f"Jumlah data setelah dibersihkan: {silver_df.count()}")

# 4. Simpan ke Silver Layer
silver_path = "./data/silver/transactions"

# Mode 'overwrite' atau 'merge' (upsert) biasa digunakan di Silver
# Di sini kita gunakan overwrite untuk mempermudah
silver_df.write.format("delta") \
    .mode("overwrite") \
    .save(silver_path)

print(f"Data bersih berhasil disimpan ke Silver Layer di {silver_path}")
spark.stop()
