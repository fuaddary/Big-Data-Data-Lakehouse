import os
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

# 1. Konfigurasi SparkSession dengan Delta Lake
builder = SparkSession.builder.appName("BronzeIngestion") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder, extra_packages=["io.delta:delta-spark_2.12:3.1.0"]).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print("--- Menjalankan Proses Ingestion ke Layer Bronze ---")

# 2. Baca file CSV Mentah
# Pastikan Anda sudah menjalankan `python generate_data.py` sebelumnya
csv_path = "raw_transactions.csv"
if not os.path.exists(csv_path):
    print(f"Error: File {csv_path} tidak ditemukan. Jalankan python generate_data.py terlebih dahulu.")
    exit(1)

# Baca as-is, tanpa mengubah tipe data banyak (schema-on-read mentah)
raw_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(csv_path)

print("Sample Data Mentah:")
raw_df.show(5)
print(f"Total baris mentah: {raw_df.count()}")

# 3. Simpan ke format Delta (Layer Bronze)
# Bronze layer menyimpan data mentah tanpa modifikasi sebagai arsip
bronze_path = "./data/bronze/transactions"

# Mode 'append' digunakan karena data raw biasanya datang bertahap
raw_df.write.format("delta") \
    .mode("append") \
    .save(bronze_path)

print(f"Data berhasil disimpan ke Bronze Layer di {bronze_path}")
spark.stop()
