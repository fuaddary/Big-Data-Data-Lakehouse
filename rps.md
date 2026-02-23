# RENCANA PEMBELAJARAN SEMESTER (RPS)

## Big Data dan Data Lakehouse

---

|                            |                                          |
| -------------------------- | ---------------------------------------- |
| **Nama Mata Kuliah** | Big Data dan Data Lakehouse              |
| **Kode Mata Kuliah** |                                          |
| **Semester**         | 6                                        |
| **SKS**              | 3 SKS (2 SKS Teori + 1 SKS Praktik)      |
| **Program Studi**    | Teknik Informatika / Teknologi Informasi |
| **Prasyarat**        | Basis Data, Pemrograman                  |
| **Dosen Pengampu**   | Fuad Dary Rosyadi S.Kom., M.Kom          |
| **Tanggal Revisi**   | Februari 2026                            |

---

## Capaian Pembelajaran Lulusan (CPL)

| Kode  | Deskripsi                                                                                                                                                                                                                 |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CPL 2 | Mampu mengkaji dan memanfaatkan ilmu pengetahuan dan teknologi dalam rangka mengaplikasikannya pada bidang Cybersecurity, Internet of Things dan Smartcity, serta integrasi sistem dan layanan komputasi awan.            |
| CPL 3 | Mampu menyelesaikan masalah dengan mengimplementasikan teknologi informasi dan komunikasi dan memperhatikan prinsip keberlanjutan serta memahami kewirausahaan berbasis teknologi.                                        |
| CPL 6 | Mampu merancang, mengintegrasikan, dan mengelola platform atau komponen perangkat keras maupun perangkat lunak menggunakan pemrograman integratif dan big data untuk mendukung aplikasi dan basis data berbasis jaringan. |
| CPL 7 | Mampu merancang, membangun, mengelola aplikasi berbasis komputer menggunakan layanan awan untuk memenuhi kebutuhan organisasi.                                                                                            |

---

## Capaian Pembelajaran Mata Kuliah (CPMK)

| Kode   | CPMK                                                                                                                                                                                              | CPL                                                    | Bobot |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ----- |
| CPMK-1 | Mahasiswa mampu menjelaskan dan mengidentifikasi konsep dasar Big Data, termasuk volume data yang besar, kecepatan data, keragaman data, dan nilai data.                                          | CPL 3 (10%), CPL 6 (10%)                               | 20%   |
| CPMK-2 | Mahasiswa mampu merancang dan mengelola infrastruktur Big Data untuk keperluan analisis menggunakan teknologi Big Data, seperti sistem manajemen database Apache Hadoop, Apache Spark, dan NoSQL. | CPL 2 (7.5%), CPL 3 (7.5%), CPL 6 (7.5%), CPL 7 (7.5%) | 30%   |
| CPMK-3 | Mahasiswa mampu merancang dan mengimplementasikan struktur Data Lakehouse yang efisien.                                                                                                           | CPL 2 (7.5%), CPL 3 (7.5%), CPL 6 (7.5%), CPL 7 (7.5%) | 30%   |
| CPMK-4 | Mahasiswa mampu menerapkan teknik analisis data besar untuk mengekstrak informasi berharga dari kumpulan data yang besar.                                                                         | CPL 2 (6.67%), CPL 3 (6.67%), CPL 6 (6.67%)            | 20%   |

---

## Rencana Pembelajaran Per Minggu

| Minggu       | CPMK                   | Kemampuan Akhir yang Diharapkan                                                                 | Bahan Kajian / Materi                                                                                                                                                           | Metode Pembelajaran                             | Pengalaman Belajar                                                                                        | Kriteria & Indikator Penilaian                                                                     | Bobot         |
| ------------ | ---------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------- |
| **1**  | CPMK-1                 | Mahasiswa mampu menjelaskan definisi, sejarah, dan karakteristik Big Data (5V)                  | - Definisi Big Data`<br>`- Sejarah perkembangan Big Data`<br>`- Karakteristik 5V: Volume, Velocity, Variety, Veracity, Value                                                | Ceramah, Diskusi, Tanya Jawab                   | Mendengarkan kuliah, berdiskusi tentang kasus nyata Big Data di industri                                  | Ketepatan penjelasan konsep 5V; partisipasi diskusi                                                | 5%            |
| **2**  | CPMK-1                 | Mahasiswa mampu mengidentifikasi ekosistem dan use case Big Data di berbagai industri           | - Ekosistem teknologi Big Data`<br>`- Use case industri: keuangan, kesehatan, e-commerce, telekomunikasi`<br>`- Tantangan pengelolaan Big Data                              | Ceramah, Studi Kasus, Presentasi                | Menganalisis studi kasus industri dan mempresentasikan temuan                                             | Kualitas analisis studi kasus; kemampuan presentasi                                                | 5%            |
| **3**  | CPMK-1                 | Mahasiswa mampu membedakan paradigma pemrosesan data: batch vs. streaming                       | - Pemrosesan batch vs. real-time/streaming`<br>`- Latensi dan throughput`<br>`- Contoh tool: batch (MapReduce) vs. streaming (Kafka Streams, Flink)                         | Ceramah, Demonstrasi, Diskusi                   | Membandingkan skenario penggunaan masing-masing paradigma                                                 | Ketepatan klasifikasi skenario; kualitas argumen perbandingan                                      | 5%            |
| **4**  | CPMK-2                 | Mahasiswa mampu menjelaskan arsitektur dan komponen Apache Hadoop                               | - HDFS (Hadoop Distributed File System)`<br>`- YARN (Yet Another Resource Negotiator)`<br>`- MapReduce programming model`<br>`- Hadoop Cluster setup                      | Ceramah, Demonstrasi, Praktikum                 | Mengonfigurasi Hadoop single-node cluster dan menjalankan job MapReduce sederhana                         | Keberhasilan konfigurasi cluster; ketepatan penjelasan komponen                                    | 7%            |
| **5**  | CPMK-2                 | Mahasiswa mampu menggunakan Apache Spark untuk pemrosesan data terdistribusi                    | - Arsitektur Spark: Driver, Executor, Cluster Manager`<br>`- RDD (Resilient Distributed Dataset)`<br>`- DataFrame dan Spark SQL`<br>`- Transformations dan Actions        | Ceramah, Praktikum                              | Membuat Spark job untuk memproses dataset besar menggunakan DataFrame API                                 | Keberhasilan eksekusi job Spark; efisiensi kode                                                    | 7%            |
| **6**  | CPMK-2                 | Mahasiswa mampu menggunakan database NoSQL untuk penyimpanan data tidak terstruktur             | - Jenis NoSQL: Document (MongoDB), Column-family (Cassandra), Key-Value (Redis), Graph`<br>`- Kapan memilih NoSQL vs SQL`<br>`- CRUD operations di MongoDB                  | Ceramah, Praktikum                              | Mengimplementasikan schema desain dan operasi CRUD pada MongoDB untuk kasus e-commerce                    | Ketepatan desain schema; keberhasilan operasi CRUD                                                 | 7%            |
| **7**  | CPMK-2                 | Mahasiswa mampu mengimplementasikan streaming data dengan Apache Kafka                          | - Arsitektur Kafka: Producer, Consumer, Broker, Zookeeper/KRaft`<br>`- Topics, Partitions, Consumer Groups`<br>`- Kafka Connect dan Kafka Streams                           | Ceramah, Praktikum                              | Membangun pipeline streaming sederhana: producer → Kafka → consumer                                     | Keberhasilan pipeline streaming; pemahaman arsitektur Kafka                                        | 7%            |
| **8**  | CPMK-1, CPMK-2         | **UJIAN TENGAH SEMESTER (UTS)**                                                           | Semua materi Minggu 1–7                                                                                                                                                        | Ujian Tertulis                                  | Mengerjakan soal UTS secara mandiri                                                                       | Ketepatan jawaban konseptual dan analitis                                                          | **20%** |
| **9**  | CPMK-3                 | Mahasiswa mampu menjelaskan evolusi arsitektur data dan konsep Data Lakehouse                   | - Evolusi: Data Warehouse → Data Lake → Data Lakehouse`<br>`- Kelebihan dan kekurangan masing-masing`<br>`- Arsitektur referensi Data Lakehouse                           | Ceramah, Diskusi, Studi Kasus                   | Membandingkan arsitektur data warehouse vs. data lake vs. data lakehouse pada kasus nyata                 | Ketepatan perbandingan; kualitas argumen pemilihan arsitektur                                      | 7%            |
| **10** | CPMK-3                 | Mahasiswa mampu merancang pipeline Data Lakehouse dengan arsitektur Medallion                   | - Medallion Architecture: Bronze, Silver, Gold layers`<br>`- Delta Lake: ACID transactions, Time Travel, Schema Evolution`<br>`- Konfigurasi Delta Lake                     | Ceramah, Demonstrasi, Praktikum                 | Mengimplementasikan pipeline Bronze → Silver → Gold menggunakan Delta Lake dan Spark                    | Keberhasilan implementasi pipeline; kualitas transformasi data                                     | 7%            |
| **11** | CPMK-3                 | Mahasiswa mampu mengimplementasikan Data Catalog dan tata kelola data                           | - Apache Iceberg dan Apache Hudi: perbandingan dengan Delta Lake`<br>`- Data Catalog: Apache Atlas, AWS Glue`<br>`- Data Governance: kualitas data, lineage, access control | Ceramah, Praktikum                              | Menkatalogisasi dataset dalam sistem Data Lakehouse yang telah dibangun                                   | Kelengkapan katalog data; penerapan policy governance                                              | 7%            |
| **12** | CPMK-4                 | Mahasiswa mampu membangun pipeline ETL/ELT dan orkestrasi workflow                              | - Konsep ETL vs. ELT`<br>`- Apache Airflow: DAG, Operator, Scheduler`<br>`- Best practices pipeline data                                                                    | Ceramah, Praktikum                              | Membuat DAG Airflow untuk mengotomasi pipeline ETL dari sumber data ke Data Lakehouse                     | Keberhasilan eksekusi DAG; ketepatan scheduling                                                    | 6%            |
| **13** | CPMK-4                 | Mahasiswa mampu menerapkan Machine Learning pada data berskala besar                            | - Spark MLlib: Classification, Regression, Clustering`<br>`- Feature engineering pada skala besar`<br>`- MLflow untuk experiment tracking                                   | Ceramah, Praktikum                              | Melatih model klasifikasi menggunakan Spark MLlib pada dataset besar dan melacak eksperimen dengan MLflow | Akurasi model; kualitas feature engineering; penggunaan MLflow                                     | 7%            |
| **14** | CPMK-4                 | Mahasiswa mampu membangun dashboard visualisasi data dari Data Lakehouse                        | - Visualisasi data besar: Apache Superset, Grafana`<br>`- Koneksi query engine: Trino/Presto`<br>`- Storytelling dengan data                                                | Ceramah, Praktikum                              | Membangun dashboard interaktif yang menampilkan insight dari Data Lakehouse yang telah dibangun           | Kualitas visualisasi; relevansi insight; interaktivitas dashboard                                  | 7%            |
| **15** | CPMK-2, CPMK-3, CPMK-4 | Mahasiswa mampu merancang dan mengimplementasikan sistem Big Data dan Data Lakehouse end-to-end | Proyek kelompok: integrasi semua komponen (ingest → store → process → analyze → visualize)                                                                                  | Project-Based Learning, Konsultasi              | Menyelesaikan dan mendokumentasikan proyek end-to-end sistem Big Data                                     | Kelengkapan sistem; kualitas implementasi; dokumentasi                                             | 10%           |
| **16** | CPMK-2, CPMK-3, CPMK-4 | **FINAL PROJECT — Demo & Presentasi Sistem End-to-End**                                  | Presentasi dan demonstrasi sistem Big Data & Data Lakehouse yang telah dibangun secara lengkap                                                                                  | Project-Based Learning, Presentasi, Tanya Jawab | Mempresentasikan sistem secara langsung, mendemonstrasikan semua fitur, dan menjawab pertanyaan penguji   | Kelengkapan fitur sistem; kualitas arsitektur; kedalaman analisis; kualitas presentasi dan jawaban | **30%** |

---

## Bobot Penilaian

| Komponen Penilaian                 | Waktu              | Bobot          | CPMK            |
| ---------------------------------- | ------------------ | -------------- | --------------- |
| Keaktifan & Partisipasi            | Sepanjang semester | 5%             | Semua CPMK      |
| Tugas Mingguan & Laporan Praktikum | Minggu 1–7, 9–14 | 20%            | CPMK-1, 2, 3, 4 |
| Ujian Tengah Semester (UTS)        | Minggu 8           | 20%            | CPMK-1, CPMK-2  |
| Proyek Kelompok                    | Minggu 15          | 25%            | CPMK-2, 3, 4    |
| Final Project (Demo & Presentasi)  | Minggu 16          | 30%            | CPMK-2, 3, 4    |
| **Total**                    |                    | **100%** |                 |

---

## Referensi Utama

1. White, T. (2015). *Hadoop: The Definitive Guide* (4th ed.). O'Reilly Media.
2. Zaharia, M., et al. (2018). *Learning Spark: Lightning-Fast Data Analytics* (2nd ed.). O'Reilly Media.
3. Armbrust, M., et al. (2021). *Delta Lake: The Definitive Guide*. O'Reilly Media.
4. Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.
5. Narkhede, N., Shapira, G., & Palino, T. (2017). *Kafka: The Definitive Guide*. O'Reilly Media.
