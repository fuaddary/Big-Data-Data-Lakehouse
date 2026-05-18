from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, to_date
from delta import configure_spark_with_delta_pip

# 1. Konfigurasi SparkSession
builder = SparkSession.builder.appName("GoldAggregation") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder, extra_packages=["io.delta:delta-spark_2.12:3.1.0"]).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print("--- Menjalankan Proses Agregasi ke Layer Gold ---")

# 2. Baca dari Silver Layer (Data yang sudah bersih)
silver_path = "./data/silver/transactions"
silver_df = spark.read.format("delta").load(silver_path)

# 3. Agregasi Bisnis (Gold Layer)
# Misalnya: Laporan Total Pendapatan per Hari untuk transaksi yang COMPLETED
gold_df = silver_df \
    .filter(col("status") == "COMPLETED") \
    .withColumn("date", to_date(col("transaction_date"))) \
    .groupBy("date") \
    .agg(
        sum("amount").alias("total_revenue"),
        count("transaction_id").alias("total_transactions")
    ) \
    .orderBy("date")

print("Sample Data Agregasi (Gold):")
gold_df.show(10)

# 4. Simpan ke Gold Layer
gold_path = "./data/gold/daily_revenue"

gold_df.write.format("delta") \
    .mode("overwrite") \
    .save(gold_path)

print(f"Data agregasi siap untuk dashboard BI tersimpan di {gold_path}")
spark.stop()
