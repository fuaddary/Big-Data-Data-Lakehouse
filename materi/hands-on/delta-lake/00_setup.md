# Setup Lingkungan Hands-on: Spark + Delta Lake

Pada praktikum ini, kita akan menggunakan container Docker yang berisi JupyterLab dan Apache Spark, serta mengkonfigurasinya untuk menggunakan Delta Lake.

## 1. Prasyarat
Pastikan laptop Anda telah terinstall:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) atau Docker Engine.
- RAM minimal 4 GB dialokasikan untuk Docker.

## 2. Menjalankan Container

Buka terminal, arahkan ke direktori `materi/hands-on/delta-lake/`, lalu jalankan:

```bash
docker-compose up -d
```

Proses ini akan mengunduh image Jupyter PySpark (mungkin butuh waktu beberapa menit tergantung kecepatan internet).

## 3. Mengakses JupyterLab

Setelah container berjalan, buka browser dan akses:
👉 **[http://localhost:8888](http://localhost:8888)**

Di panel sebelah kiri JupyterLab, masuk ke folder `work/`. Di folder inilah skrip Python kita berada.

## 4. Konfigurasi PySpark dengan Delta Lake

Secara default, instalasi Spark belum memuat library Delta Lake. Di setiap file skrip Python (`.py`) atau Jupyter Notebook (`.ipynb`), kita perlu mendeklarasikan dependensi paket Delta Lake saat inisialisasi `SparkSession`.

Contoh inisialisasi yang wajib ada di setiap skrip kita:

```python
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder.appName("DeltaLakeHandsOn") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

# Menggunakan Delta Lake versi 3.1.0 (kompatibel dengan Spark 3.5)
spark = configure_spark_with_delta_pip(builder, extra_packages=["io.delta:delta-spark_2.12:3.1.0"]).getOrCreate()
```

## 5. Menjalankan Skrip Python

Anda dapat menjalankan skrip-skrip yang disediakan dengan dua cara:
1. **Via Terminal di JupyterLab**: Buka Terminal (File > New > Terminal), navigasi ke folder `work`, lalu jalankan:
   ```bash
   python 01_bronze_ingestion.py
   ```
2. **Via Jupyter Notebook**: Buat notebook baru (`.ipynb`), copy-paste isi skrip ke dalam cell, dan jalankan secara interaktif. Ini sangat disarankan agar Anda bisa melihat output Dataframe secara langsung.

## Langkah Selanjutnya

Silakan lanjutkan ke materi **01_bronze_ingestion.py**.
