from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

# 1. Konfigurasi SparkSession
builder = SparkSession.builder.appName("DeltaTimeTravel") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder, extra_packages=["io.delta:delta-spark_2.12:3.1.0"]).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

print("--- Demonstrasi Time Travel di Delta Lake ---")

silver_path = "./data/silver/transactions"

# 2. Update data untuk mensimulasikan perubahan (misal mengubah status PENDING jadi COMPLETED)
from delta.tables import DeltaTable

print("Melakukan update pada data Silver (mengubah PENDING menjadi COMPLETED)...")
deltaTable = DeltaTable.forPath(spark, silver_path)
deltaTable.update(
    condition = "status = 'PENDING'",
    set = { "status": "'COMPLETED'" }
)

# 3. Menampilkan History Tabel
print("\nHistory Perubahan Tabel Silver:")
history_df = deltaTable.history()
history_df.select("version", "timestamp", "operation", "operationParameters").show(truncate=False)

# 4. Query Time Travel (Melihat versi sebelumnya)
# Mendapatkan versi terbaru
latest_version = history_df.agg({"version": "max"}).collect()[0][0]

print(f"\nQuery data versi saat ini (Versi {latest_version}):")
current_df = spark.read.format("delta").load(silver_path)
current_df.groupBy("status").count().show()

print(f"\nQuery data versi sebelumnya (Versi 0 - sebelum di-update):")
# Kita baca as of version 0
old_df = spark.read.format("delta").option("versionAsOf", 0).load(silver_path)
old_df.groupBy("status").count().show()

print("Demonstrasi Time Travel selesai.")
spark.stop()
