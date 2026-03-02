# Pertemuan 2: Ekosistem Big Data dan Use Case di Industri

|                           |                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------- |
| **Mata Kuliah**     | Big Data dan Data Lakehouse                                                           |
| **Pertemuan**       | 2 (Minggu 2)                                                                          |
| **Durasi**          | 120 menit                                                                             |
| **CPMK**            | CPMK-1                                                                                |
| **Kemampuan Akhir** | Mahasiswa mampu mengidentifikasi ekosistem dan use case Big Data di berbagai industri |
| **Metode**          | Ceramah, Studi Kasus, Diskusi Kelompok, Kuis Interaktif, Presentasi                   |

---

## Agenda Perkuliahan

| Waktu          | Durasi | Kegiatan                                    | Keterangan                                              |
| -------------- | ------ | ------------------------------------------- | ------------------------------------------------------- |
| 00:00 – 00:15 | 15 min | Pembukaan & Kuis Review Pertemuan 1         | Kuis interaktif 5V + review tugas                       |
| 00:15 – 00:35 | 20 min | Bagian 1: Ekosistem Teknologi Big Data      | Peta teknologi dan arsitektur referensi                 |
| 00:35 – 00:50 | 15 min | 🎯 Aktivitas 1: Technology Matching Game    | Kelompok mencocokkan teknologi ke kategori pipeline     |
| 00:50 – 01:10 | 20 min | Bagian 2: Use Case Big Data di Industri     | Studi kasus 4 industri utama                            |
| 01:10 – 01:30 | 20 min | 🎯 Aktivitas 2: Analisis Use Case Industri  | Kelompok merancang solusi Big Data untuk skenario nyata |
| 01:30 – 01:40 | 10 min | Bagian 3: Tantangan Pengelolaan Big Data    | Teknis, organisasi, etika, dan regulasi                 |
| 01:40 – 01:50 | 10 min | 🎯 Aktivitas 3: Debat — Tantangan Terbesar | Debat kelas: tantangan mana yang paling sulit diatasi?  |
| 01:50 – 02:00 | 10 min | 🎯 Aktivitas 4: Refleksi & Penugasan        | Kuis penutup + penugasan minggu depan                   |

> 📊 **Komposisi waktu:** ~40% ceramah, ~60% aktivitas mahasiswa

---

## Pembukaan & Kuis Review Pertemuan 1 (15 menit)

### 🎯 Kuis Interaktif: "Seberapa Ingat Kamu?" (10 menit)

> **Format:** Kuis cepat — mahasiswa menjawab dengan mengangkat tangan, menjawab lisan, atau via platform polling (Mentimeter/Kahoot jika tersedia)

**Ronde 1: Benar atau Salah (5 soal, masing-masing 30 detik)**

| No | Pernyataan                                                       | Jawaban                                            |
| -- | ---------------------------------------------------------------- | -------------------------------------------------- |
| 1  | Big Data hanya tentang data yang berukuran besar (Volume)        | ❌ Salah — ada 5V                                 |
| 2  | Sekitar 80% data di dunia adalah data tidak terstruktur          | ✅ Benar                                           |
| 3  | RDBMS seperti MySQL sudah cukup untuk mengelola Big Data         | ❌ Salah — perlu teknologi terdistribusi          |
| 4  | "Garbage In, Garbage Out" berkaitan dengan dimensi Veracity      | ✅ Benar                                           |
| 5  | Doug Laney pertama kali memperkenalkan konsep 5V pada tahun 2001 | ❌ Salah — awalnya 3V (Volume, Velocity, Variety) |

**Ronde 2: Tebak V! (5 soal, masing-masing 20 detik)**

> Dosen membacakan skenario, mahasiswa harus menjawab **itu termasuk V yang mana**.

| No | Skenario                                                         | Jawaban            |
| -- | ---------------------------------------------------------------- | ------------------ |
| 1  | Twitter menghasilkan 6.000 tweet per detik                       | **Velocity** |
| 2  | Data pelanggan tersebar dalam format SQL, JSON, foto, dan audio  | **Variety**  |
| 3  | Netflix menghemat $1 miliar/tahun dari rekomendasi berbasis data | **Value**    |
| 4  | Facebook menyimpan 4 Petabytes data baru per hari                | **Volume**   |
| 5  | 15% aktivitas Twitter berasal dari bot — apakah data ini valid? | **Veracity** |

> 🏆 **Gamifikasi:** Mahasiswa/kelompok dengan jawaban paling banyak benar mendapat poin partisipasi bonus.

### Review Tugas Pertemuan 1 (5 menit)

- 2–3 mahasiswa berbagi **satu insight menarik** dari tugas analisis industri
- Dosen memberikan feedback singkat dan transisi ke materi hari ini

---

## Bagian 1: Ekosistem Teknologi Big Data (20 menit)

### 1.1 Apa Itu Ekosistem Big Data?

**Ekosistem Big Data** adalah kumpulan teknologi, tools, framework, dan platform yang bekerja bersama untuk **mengumpulkan, menyimpan, memproses, menganalisis, dan memvisualisasikan** data berskala besar.

> 🏗️ **Analogi:** Bayangkan membangun sebuah kota modern. Kita butuh:
>
> - **Jalan raya** (infrastruktur jaringan & penyimpanan)
> - **Pabrik** (mesin pemrosesan data)
> - **Gudang** (penyimpanan data)
> - **Kantor analisis** (tools analitik)
> - **Dashboard kota** (visualisasi)
>
> Tidak ada satu teknologi yang bisa melakukan semuanya — diperlukan **ekosistem** yang saling terhubung.

### 1.2 Arsitektur Referensi Big Data

Secara umum, aliran data dalam ekosistem Big Data mengikuti pipeline berikut:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     ARSITEKTUR REFERENSI BIG DATA                            │
│                                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐  │
│  │  DATA     │   │  DATA     │   │  DATA     │   │  DATA     │   │  DATA     │  │
│  │  SOURCE   │──▶│  INGEST   │──▶│  STORE    │──▶│  PROCESS  │──▶│  SERVE    │  │
│  │          │   │          │   │          │   │  & ANALYZE │   │  & VIZ   │  │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘  │
│                                                                              │
│  Database        Kafka          HDFS           Spark          Dashboard      │
│  API             Flume          S3/MinIO       Flink          Grafana        │
│  IoT Sensor      NiFi           NoSQL          Hive           Superset       │
│  Log Files       Sqoop          Delta Lake     MLlib          Jupyter        │
│  Media Sosial    Debezium       Iceberg        Presto/Trino   Metabase       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Kategori Teknologi dalam Ekosistem Big Data

> 💡 **Catatan untuk dosen:** Jelaskan setiap kategori secara singkat (~3 menit per kategori). Detail mendalam akan dijelajahi mahasiswa melalui Aktivitas 1.

#### 📥 Kategori 1: Data Ingestion (Pengumpulan Data)

Teknologi untuk **mengambil data dari berbagai sumber** dan memasukkannya ke dalam sistem Big Data.

| Teknologi              | Jenis        | Deskripsi                                                       |
| ---------------------- | ------------ | --------------------------------------------------------------- |
| **Apache Kafka** | Streaming    | Platform distributed streaming untuk data real-time             |
| **Apache Flume** | Batch/Stream | Mengumpulkan dan memindahkan log data dalam jumlah besar        |
| **Apache NiFi**  | Flow-based   | Automasi aliran data antar sistem dengan visual drag-and-drop   |
| **Apache Sqoop** | Batch        | Transfer data antara RDBMS dan Hadoop/HDFS                      |
| **Debezium**     | CDC          | Change Data Capture — menangkap perubahan dari database source |
| **Logstash**     | Stream       | Bagian dari ELK Stack, mengumpulkan dan memproses log           |

> 💡 **Analogi:** Data Ingestion = **"kurir"** yang mengambil paket (data) dari berbagai toko (sumber) dan mengantarkannya ke gudang (storage).

#### 💾 Kategori 2: Data Storage (Penyimpanan Data)

| Teknologi                   | Jenis          | Deskripsi                                                            |
| --------------------------- | -------------- | -------------------------------------------------------------------- |
| **HDFS**              | Distributed FS | Hadoop Distributed File System — penyimpanan terdistribusi          |
| **Amazon S3 / MinIO** | Object Storage | Penyimpanan objek untuk data terstruktur & tidak terstruktur         |
| **MongoDB**           | Document NoSQL | Database NoSQL berbasis dokumen JSON                                 |
| **Apache Cassandra**  | Column-family  | Database terdistribusi untuk write-heavy workload                    |
| **Redis**             | Key-Value      | In-memory data store untuk caching & real-time data                  |
| **Delta Lake**        | Table Format   | Open-source storage layer dengan ACID transactions di atas data lake |

> 💡 **Analogi:** Data Storage = **"gudang"** — HDFS = gudang besar terdistribusi; NoSQL = rak fleksibel; Object Storage = container serbaguna.

#### ⚙️ Kategori 3: Data Processing (Pemrosesan Data)

| Teknologi                           | Jenis        | Deskripsi                                                       |
| ----------------------------------- | ------------ | --------------------------------------------------------------- |
| **Apache Hadoop (MapReduce)** | Batch        | Framework pemrosesan terdistribusi untuk data besar             |
| **Apache Spark**              | Batch+Stream | Mesin pemrosesan data terpadu, 100× lebih cepat dari MapReduce |
| **Apache Flink**              | Stream-first | Stream processing engine dengan latensi sangat rendah           |
| **Presto / Trino**            | SQL Engine   | Distributed SQL query engine untuk data di berbagai sumber      |

> 💡 **Analogi:** MapReduce = pabrik batch tradisional; Spark = pabrik modern super cepat; Flink = assembly line tanpa henti.

#### 📊 Kategori 4: Data Analysis & Visualization

| Teknologi                    | Jenis          | Deskripsi                                                 |
| ---------------------------- | -------------- | --------------------------------------------------------- |
| **Spark MLlib**        | ML Library     | Library machine learning terdistribusi di Apache Spark    |
| **Apache Superset**    | BI Dashboard   | Platform open-source untuk visualisasi data dan dashboard |
| **Grafana**            | Monitoring Viz | Dashboard untuk monitoring dan observability              |
| **Tableau / Power BI** | BI Dashboard   | Platform visualisasi data enterprise                      |

#### 🔧 Kategori 5: Orchestration & Governance

| Teknologi                | Jenis        | Deskripsi                                               |
| ------------------------ | ------------ | ------------------------------------------------------- |
| **Apache Airflow** | Orchestrator | Platform untuk menjadwalkan dan memonitor workflow data |
| **Apache Atlas**   | Data Catalog | Metadata management dan data governance                 |
| **MLflow**         | ML Lifecycle | Platform untuk mengelola lifecycle machine learning     |

### 1.4 Peta Ekosistem Big Data

```
┌────────────────────────────────────────────────────────────────────┐
│                   PETA EKOSISTEM BIG DATA                          │
│                                                                    │
│   ┌─── Data Sources ─────────────────────────────────────────┐    │
│   │ RDBMS │ IoT │ Log │ API │ Social Media │ File │ Stream   │    │
│   └───────────────────────────────────────────────────────────┘    │
│                            │                                       │
│                            ▼                                       │
│   ┌─── Ingestion ────────────────────────────────────────────┐    │
│   │      Kafka  │  NiFi  │  Flume  │  Debezium  │  Sqoop    │    │
│   └───────────────────────────────────────────────────────────┘    │
│                            │                                       │
│                            ▼                                       │
│   ┌─── Storage ──────────────────────────────────────────────┐    │
│   │ HDFS │ S3/MinIO │ MongoDB │ Cassandra │ Delta Lake       │    │
│   └───────────────────────────────────────────────────────────┘    │
│                            │                                       │
│                            ▼                                       │
│   ┌─── Processing ───────────────────────────────────────────┐    │
│   │    Spark  │  Flink  │  Hive  │  Trino  │  MapReduce      │    │
│   └───────────────────────────────────────────────────────────┘    │
│                            │                                       │
│                            ▼                                       │
│   ┌─── Analysis & Serving ───────────────────────────────────┐    │
│   │  Superset │ Grafana │ Jupyter │ MLlib │ Tableau │ Metabase│    │
│   └───────────────────────────────────────────────────────────┘    │
│                            │                                       │
│   ┌─── Cross-cutting ───────────────────────────────────────┐     │
│   │   Airflow (Orchestration)  │  Atlas (Governance)         │    │
│   │   Docker/K8s (Infra)       │  MLflow (ML Ops)            │    │
│   └──────────────────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────────────┘
```

---

---

## Bagian 2: Use Case Big Data di Berbagai Industri (20 menit)

> Dosen menjelaskan **satu use case per industri** secara mendalam (~5 menit per industri). Masing-masing menjelaskan: masalah, data, teknologi, dan dampak. Detail tambahan akan dijelajahi mahasiswa di Aktivitas 2.

### 2.1 🏦 Industri Keuangan: Deteksi Fraud Real-time

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Transaksi   │────▶│  Kafka       │────▶│  Spark       │────▶│  Alert /     │
│  Kartu Kredit│     │  (Streaming) │     │  Streaming   │     │  Block       │
│              │     │              │     │  + ML Model  │     │  Transaksi   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

| Aspek               | Detail                                                               |
| ------------------- | -------------------------------------------------------------------- |
| **Masalah**   | Kerugian fraud kartu kredit global mencapai $32 miliar/tahun         |
| **Data**      | Transaksi real-time, lokasi, riwayat belanja, device fingerprint     |
| **Teknologi** | Kafka, Spark Streaming, Machine Learning (Random Forest, Neural Net) |
| **Proses**    | Setiap transaksi dievaluasi dalam <100ms menggunakan model ML        |
| **Dampak**    | Mengurangi kerugian fraud hingga 50–60%                             |

🇮🇩 **Indonesia:** BCA, GoPay/OVO/Dana menggunakan Big Data untuk fraud detection real-time

---

### 2.2 🏥 Industri Kesehatan: Prediksi Penyakit

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Electronic    │     │ Data Lake     │     │ ML Models     │
│ Health Record │────▶│ (HDFS/S3)     │────▶│ (Spark MLlib) │
│ + Wearable    │     │ Cleaned &     │     │ Prediksi      │
│ + Genomic     │     │ Integrated    │     │ penyakit dini │
└───────────────┘     └───────────────┘     └───────────────┘
```

| Aspek               | Detail                                                                |
| ------------------- | --------------------------------------------------------------------- |
| **Masalah**   | Deteksi dini penyakit kronis (diabetes, jantung, kanker)              |
| **Data**      | EHR, hasil lab, riwayat keluarga, data genetik, data wearable         |
| **Teknologi** | HDFS, Spark MLlib, TensorFlow (deep learning untuk citra medis)       |
| **Dampak**    | Deteksi kanker payudara 30% lebih awal; penurunan biaya perawatan 25% |

🇮🇩 **Indonesia:** BPJS Kesehatan (deteksi fraud klaim), Halodoc (tren penyakit), Kemenkes (dashboard COVID-19)

---

### 2.3 🛒 Industri E-Commerce: Recommendation Engine

| Aspek               | Detail                                                                                |
| ------------------- | ------------------------------------------------------------------------------------- |
| **Masalah**   | Menampilkan produk yang relevan dari jutaan SKU                                       |
| **Data**      | Browsing history, purchase history, rating, review, demographic                       |
| **Teknologi** | Spark MLlib, TensorFlow, Redis (real-time serving), Kafka                             |
| **Dampak**    | Amazon:**35% revenue** berasal dari rekomendasi; Netflix: hemat $1 miliar/tahun |

🇮🇩 **Indonesia:** Tokopedia (rekomendasi 100+ juta pengguna), Shopee (halaman beranda personal)

---

### 2.4 📡 Industri Telekomunikasi: Network Optimization

| Aspek               | Detail                                                                |
| ------------------- | --------------------------------------------------------------------- |
| **Masalah**   | Jaringan overloaded di jam sibuk, dead zone, kualitas layanan menurun |
| **Data**      | Data trafik per cell tower, signal strength, CDR                      |
| **Teknologi** | Apache Kafka (streaming), Spark (analisis), Grafana (monitoring)      |
| **Dampak**    | Pengurangan downtime 40%; peningkatan customer satisfaction 15%       |

🇮🇩 **Indonesia:** Telkomsel (optimasi 4G/5G), XL Axiata (platform nGage), Indosat (Customer 360°)

---

### Ringkasan Use Case per Industri

| Industri                 | Use Case Utama        | Teknologi Kunci               | Dampak Bisnis                |
| ------------------------ | --------------------- | ----------------------------- | ---------------------------- |
| **Keuangan**       | Fraud detection       | Kafka, Spark Streaming, ML    | Kurangi fraud 50–60%        |
| **Kesehatan**      | Prediksi penyakit     | HDFS, Spark MLlib, TensorFlow | Deteksi dini 30% lebih awal  |
| **E-Commerce**     | Recommendation engine | Spark, Kafka, Redis, ML       | 35% revenue dari rekomendasi |
| **Telekomunikasi** | Network optimization  | Kafka, Spark, Grafana         | Pengurangan downtime 40%     |

---

## 🎯 Aktivitas 2: "Big Data Architect Challenge" — 8 Skenario Industri (20 menit)

### Tujuan

Setiap kelompok berperan sebagai **Solution Architect** yang merancang solusi Big Data untuk skenario industri nyata.

### Instruksi (2 menit)

1. Masing-masing **kelompok** sudah terbentuk (sesuai pembagian kelompok)
2. Setiap kelompok mendapat **satu skenario industri** berbeda (di bawah)
3. Waktu kerja: 30 **menit**
4. Presentasi kilat: 5 **menit per kelompok** — cukup share screen slide kalian

### Template Slide (sudah disiapkan dosen di Google Slides)

> Setiap slide kelompok sudah berisi template ini:

```
🏢 KELOMPOK [X]: [Nama Skenario]

📌 3 SUMBER DATA:
   1. _______________
   2. _______________
   3. _______________

🔗 PIPELINE:
   [Source] → [Ingest] → [Store] → [Process] → [Serve]
   ________   ________   ________   ________   ________

💡 CARA KERJA (2 kalimat):
   _______________________________________________

📈 DAMPAK BISNIS:
   _______________________________________________
```

### 8 Skenario (1 per Kelompok)

#### 🏦 Kelompok 1: Fintech "DompetKu" — Fraud Detection

> **Konteks:** E-wallet Indonesia, 10 juta pengguna, 500K transaksi/hari.
> **Masalah:** Lonjakan fraud 300% dalam 3 bulan. Kerugian Rp 5 miliar/bulan.
> **Misi:** Rancang sistem **deteksi fraud real-time** — transaksi mencurigakan harus terblokir dalam hitungan milidetik.

#### 🏥 Kelompok 2: RS "Harapan Sehat" — Prediksi Re-admission

> **Konteks:** RS besar, 500K rekam medis, 200 dokter, 50 alat IoT.
> **Masalah:** 20% pasien kembali masuk RS dalam 30 hari (costly & bisa dicegah).
> **Misi:** Bangun sistem **prediksi pasien yang berisiko kembali** — agar bisa diberi perawatan preventif sebelum pulang.

#### 🛒 Kelompok 3: E-Commerce "PasarOnline" — Flash Sale Survival

> **Konteks:** Marketplace Indonesia, 5 juta produk, 20 juta user aktif.
> **Masalah:** Flash Sale 12.12 akan datang — traffic diprediksi naik **20× lipat**.
> **Misi:** Rancang **sistem recommendation + dynamic pricing** yang tidak down saat flash sale. Fokus: skalabilitas!

#### 📡 Kelompok 4: Operator "IndoNet" — Churn Prediction

> **Konteks:** Operator seluler, 50 juta pelanggan.
> **Masalah:** Churn rate 25%/tahun — pelanggan pindah ke kompetitor tanpa peringatan.
> **Misi:** Bangun sistem **prediksi churn** untuk identifikasi pelanggan yang akan kabur dan lakukan kampanye retensi proaktif.

#### 🎓 Kelompok 5: EdTech "PintarApp" — Personalized Learning

> **Konteks:** Platform belajar online, 2 juta siswa SMA, 10.000 konten video.
> **Masalah:** 60% siswa drop-out dari kursus sebelum selesai.
> **Misi:** Rancang sistem **rekomendasi konten personalized** + **prediksi siswa yang berisiko drop** agar bisa di-intervensi lebih awal.

#### 🚗 Kelompok 6: Ride-Hailing "JalanYuk" — Dynamic Surge Pricing

> **Konteks:** Layanan ride-hailing Indonesia, 5 juta trip/hari, 500K driver.
> **Masalah:** Di jam sibuk supply driver < demand → pelanggan batal, driver nganggur di area sepi.
> **Misi:** Rancang sistem **surge pricing + redistribusi driver** real-time berdasarkan prediksi demand per zona.

#### 🏭 Kelompok 7: Manufaktur "IndoParts" — Predictive Maintenance

> **Konteks:** Pabrik otomotif, 200 mesin produksi, 1.000 sensor IoT.
> **Masalah:** Downtime mesin tidak terduga menyebabkan kerugian Rp 2 miliar/bulan.
> **Misi:** Bangun sistem **predictive maintenance** — prediksi kapan mesin akan rusak sebelum terjadi, berdasarkan data sensor real-time.

#### 🌾 Kelompok 8: AgriTech "TaniData" — Smart Farming

> **Konteks:** Platform pertanian pintar, 50.000 petani, sensor kelembaban + drone imagery.
> **Masalah:** 30% hasil panen gagal karena keputusan irigasi & pemupukan yang tidak data-driven.
> **Misi:** Rancang sistem **rekomendasi pertanian berbasis data** — kapan menyiram, kapan panen, kapan pupuk, berdasarkan data sensor & cuaca.

Rubrik Penilaian Aktivitas 2 : Peer Review

| Kriteria                                | Bobot |
| --------------------------------------- | ----- |
| Ketepatan identifikasi sumber data      | 20%   |
| Kualitas rancangan pipeline             | 30%   |
| Ketepatan pemilihan teknologi           | 25%   |
| Kualitas penjelasan dan presentasi      | 15%   |
| Kreativitas dan pemahaman dampak bisnis | 10%   |

---

## Bagian 3: Tantangan Pengelolaan Big Data (10 menit)

> Dosen menyampaikan **overview singkat** 3 kategori tantangan. Detail akan didalami melalui Aktivitas 3 (Debat).

### 3.1 Tantangan Teknis

```
┌──────────────────────────────────────────────────────────────┐
│              TANTANGAN TEKNIS BIG DATA                        │
├──────────────┬───────────────────────────────────────────────┤
│ Skalabilitas │ Data tumbuh lebih cepat dari kapasitas →     │
│              │ Solusi: horizontal scaling, distributed sys   │
├──────────────┤───────────────────────────────────────────────┤
│ Integrasi    │ Data tersebar di banyak sumber & format →    │
│ Data         │ Solusi: ETL/ELT pipeline, Data Lakehouse     │
├──────────────┤───────────────────────────────────────────────┤
│ Kualitas     │ 26% data organisasi tidak akurat →           │
│ Data         │ Solusi: data validation, data quality tools   │
├──────────────┤───────────────────────────────────────────────┤
│ Real-time    │ Latensi vs akurasi →                         │
│ Processing   │ Solusi: Lambda/Kappa architecture             │
└──────────────┴───────────────────────────────────────────────┘
```

### 3.2 Tantangan Organisasi

| Tantangan           | Fakta                                                      |
| ------------------- | ---------------------------------------------------------- |
| **Skill Gap** | Kekurangan ~250.000 data scientist global (2025)           |
| **Biaya**     | Infrastruktur + talenta + maintenance bisa sangat mahal    |
| **Budaya**    | Transformasi data-driven butuh perubahan budaya organisasi |

### 3.3 Tantangan Etika & Regulasi

| Tantangan           | Contoh Nyata                                                 |
| ------------------- | ------------------------------------------------------------ |
| **Privasi**   | UU PDP Indonesia: sanksi pidana 6 tahun, denda Rp 6 miliar   |
| **Bias Data** | Sistem rekrutmen Amazon bias terhadap kandidat wanita (2018) |
| **Keamanan**  | Rata-rata biaya data breach: $4.45 juta/insiden (IBM, 2023)  |

---

### Rangkuman Pertemuan 2 (2 menit)

```
┌─────────────────────────────────────────────────────────────┐
│                   RANGKUMAN HARI INI                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. EKOSISTEM BIG DATA = 5 layer pipeline:                  │
│     Source → Ingest → Store → Process → Serve              │
│                                                             │
│  2. USE CASE DI 8 INDUSTRI:                                 │
│     Fintech │ Healthcare │ E-Commerce │ Telco              │
│     EdTech  │ Ride-Hail  │ Manufaktur │ AgriTech           │
│                                                             │
│  3. TANTANGAN = Teknis + Organisasi + Etika                 │
│     Semuanya saling terkait!                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Preview Pertemuan 3

- **Topik:** Paradigma Pemrosesan Data — Batch vs. Streaming
- Kita akan membandingkan **pemrosesan batch** (MapReduce) dan **streaming** (Kafka, Flink)
- Akan ada **hands-on demonstrasi** konsep batch dan streaming

### Tugas Pertemuan 2 (3 menit)

> **Jenis:** Kelompok (sesuai pembagian kelompok yang sudah ditentukan)
> **Deadline:** Sebelum Pertemuan 3 (via LMS)

**Tugas:**
Pilih **satu perusahaan atau organisasi nyata** (boleh lokal atau global) dan buat **presentasi analisis Big Data** (10–15 slide) yang mencakup:

1. **Profil Singkat** perusahaan/organisasi
2. **Identifikasi** minimal 3 sumber data Big Data yang dimiliki perusahaan
3. **Gambarkan** arsitektur ekosistem Big Data yang mungkin digunakan (mengacu pada pipeline 5 tahap)
4. **Jelaskan** minimal 2 use case Big Data yang diterapkan perusahaan
5. **Analisis** tantangan Big Data apa yang mungkin dihadapi dan bagaimana mengatasinya
6. **Berikan rekomendasi** teknologi Big Data yang bisa ditambahkan

**Format:** Presentasi (Google Slides/Canva), akan dipresentasikan pada pertemuan berikutnya.

**Kriteria Penilaian:**

| Kriteria                                    | Bobot |
| ------------------------------------------- | ----- |
| Kedalaman riset dan analisis                | 30%   |
| Kualitas arsitektur ekosistem yang digambar | 25%   |
| Relevansi dan kualitas use case             | 20%   |
| Analisis tantangan dan rekomendasi          | 15%   |
| Kualitas presentasi dan visual              | 10%   |

---

## Referensi

1. Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.
2. Marz, N., & Warren, J. (2015). *Big Data: Principles and Best Practices of Scalable Realtime Data Systems*. Manning.
3. White, T. (2015). *Hadoop: The Definitive Guide* (4th ed.). O'Reilly Media.
4. Reis, J., & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly Media.
5. McKinsey Global Institute. (2023). "The State of AI and Big Data Analytics."
6. IBM Security. (2023). "Cost of a Data Breach Report."
7. UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi. Republik Indonesia.
8. IDC. (2024). "The Global DataSphere Report."
9. Gartner. (2024). "Top Trends in Data and Analytics."
