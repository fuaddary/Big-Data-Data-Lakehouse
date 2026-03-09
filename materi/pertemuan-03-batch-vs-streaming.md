# Pertemuan 3: Paradigma Pemrosesan Data — Batch vs. Streaming

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Mata Kuliah**     | Big Data dan Data Lakehouse                                               |
| **Pertemuan**       | 3 (Minggu 3)                                                              |
| **Durasi**          | 120 menit                                                                 |
| **CPMK**            | CPMK-1                                                                    |
| **Kemampuan Akhir** | Mahasiswa mampu membedakan paradigma pemrosesan data: batch vs. streaming |
| **Metode**          | Ceramah, Demonstrasi, Diskusi Kelompok, Kuis Interaktif, Studi Kasus      |

---

## Agenda Perkuliahan

| Waktu          | Durasi | Kegiatan                                      | Keterangan                                                  |
| -------------- | ------ | --------------------------------------------- | ----------------------------------------------------------- |
| 00:00 – 00:15 | 15 min | Pembukaan & Kuis Review Pertemuan 2           | Review tugas                                                |
| 00:15 – 00:35 | 20 min | Bagian 1: Pemrosesan Batch                    | Konsep batch, MapReduce, use case                           |
| 00:35 – 00:55 | 20 min | Bagian 2: Pemrosesan Streaming                | Konsep streaming, Kafka Streams, Flink, use case            |
| 00:55 – 01:10 | 15 min | Bagian 3: Latensi, Throughput & Arsitektur    | Perbandingan mendalam, Lambda & Kappa Architecture          |
| 01:10 – 01:30 | 20 min | 🎯 Aktivitas 1: "Batch or Stream?" Challenge  | Kelompok mengklasifikasikan 16 skenario dunia nyata         |
| 01:30 – 01:45 | 15 min | 🎯 Aktivitas 2: Arsitektur Pipeline Challenge | Kelompok merancang pipeline hybrid untuk skenario industri  |
| 01:45 – 01:55 | 10 min | 🎯 Aktivitas 3: Debat — "Masa Depan Batch"   | Debat: Apakah batch processing akan punah di era real-time? |
| 01:55 – 02:00 | 5 min  | Refleksi & Penugasan                          | Kuis penutup + penugasan minggu depan                       |

> 📊 **Komposisi waktu:** ~45% ceramah, ~55% aktivitas mahasiswa

---

### Presentasi Tugas Kelompok Pertemuan 2 (5 menit)

- 2–3 kelompok melakukan **presentasi kilat** (2 menit per kelompok) tentang analisis Big Data perusahaan nyata
- Dosen memberikan feedback singkat
- **Transisi:** _"Perusahaan-perusahaan yang kalian analisis tadi — mereka semua harus memutuskan: kapan data diproses secara batch, dan kapan secara real-time. Inilah topik kita hari ini!"_

---

## Bagian 1: Pemrosesan Batch (20 menit)

### 1.1 Apa Itu Pemrosesan Batch?

**Pemrosesan Batch** adalah paradigma di mana data dikumpulkan terlebih dahulu dalam jumlah besar, lalu diproses sekaligus pada waktu tertentu.

> 🍕 **Analogi: Warung Makan vs. Restoran Catering**
>
> Bayangkan sebuah **katering pernikahan**:
>
> - Pesanan dikumpulkan dulu **semua** (1.000 porsi)
> - Baru **setelah terkumpul**, masak semua sekaligus
> - Hasilnya dikirim dalam satu waktu
>
> Inilah cara kerja **batch processing** — data dikumpulkan, ditunggu, lalu diproses bersama-sama.

```
┌───────────────────────────────────────────────────────────────────┐
│                    PEMROSESAN BATCH                                │
│                                                                   │
│   Data masuk terus-menerus...                                     │
│   │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │                 │
│   ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼                 │
│   ┌──────────────────────────────────────────┐                    │
│   │        DATA DIKUMPULKAN (Buffer)         │  ← Menunggu       │
│   │  [d1][d2][d3][d4][d5]...[d1000]          │                    │
│   └──────────────────────────────────────────┘                    │
│                         │                                         │
│                         ▼  ← Trigger (waktu/ukuran)              │
│   ┌──────────────────────────────────────────┐                    │
│   │        PROSES SEKALIGUS (Batch Job)       │                    │
│   │   MapReduce / Spark Batch / Hive          │                    │
│   └──────────────────────────────────────────┘                    │
│                         │                                         │
│                         ▼                                         │
│   ┌──────────────────────────────────────────┐                    │
│   │        HASIL (Output)                     │                    │
│   │   Laporan harian, agregasi, analytics     │                    │
│   └──────────────────────────────────────────┘                    │
│                                                                   │
│   ⏱️ Latensi: Menit hingga Jam                                   │
│   📦 Throughput: Sangat Tinggi                                    │
└───────────────────────────────────────────────────────────────────┘
```

### 1.2 Karakteristik Pemrosesan Batch

| Karakteristik          | Detail                                                       |
| ---------------------- | ------------------------------------------------------------ |
| **Waktu proses** | Data diproses dalam interval tertentu (harian, per jam, dll) |
| **Latensi**      | Tinggi (menit–jam, bahkan hari)                             |
| **Throughput**   | Sangat tinggi — jutaan record per job                       |
| **Data source**  | Data historis yang sudah tersimpan (at rest)                 |
| **Kompleksitas** | Relatif sederhana, lebih mudah di-debug dan di-monitor       |
| **Toleransi**    | Fault-tolerant — job bisa di-restart jika gagal             |

### 1.3 Teknologi Batch Processing

#### 📍 MapReduce — Sang Pelopor

**MapReduce** adalah model pemrograman yang diperkenalkan Google (2004) dan menjadi fondasi Apache Hadoop.

```
┌─────────────────────────────────────────────────────────────────┐
│                    CARA KERJA MapReduce                          │
│                                                                 │
│  INPUT DATA (Besar, terdistribusi)                               │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                           │
│  │Split1│ │Split2│ │Split3│ │Split4│                           │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘                           │
│     │        │        │        │                                │
│     ▼        ▼        ▼        ▼         ← FASE MAP            │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    (transformasi paralel)│
│  │Map 1 │ │Map 2 │ │Map 3 │ │Map 4 │                           │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘                           │
│     │        │        │        │                                │
│     └────────┴────┬───┴────────┘         ← SHUFFLE & SORT      │
│                   │                       (pengelompokan)       │
│     ┌─────────────┼──────────────┐                              │
│     ▼             ▼              ▼       ← FASE REDUCE         │
│  ┌──────┐   ┌──────┐    ┌──────┐        (agregasi)            │
│  │Red 1 │   │Red 2 │    │Red 3 │                               │
│  └──┬───┘   └──┬───┘    └──┬───┘                               │
│     │          │           │                                    │
│     ▼          ▼           ▼                                    │
│  ┌────────────────────────────────────┐                         │
│  │           OUTPUT AKHIR             │                         │
│  └────────────────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

**Contoh Sederhana: Word Count**

> Hitung frekuensi setiap kata dalam dokumen 1 TB.

```
INPUT:   "big data is big"

MAP:     ("big", 1), ("data", 1), ("is", 1), ("big", 1)

SHUFFLE: ("big", [1, 1]), ("data", [1]), ("is", [1])

REDUCE:  ("big", 2), ("data", 1), ("is", 1)
```

> 💡 **Kunci MapReduce:** Setiap Map dan Reduce berjalan **paralel** di node berbeda. Itulah kekuatannya — horizontal scaling!

#### 📍 Apache Spark (Batch Mode)

**Spark** hadir sebagai evolusi MapReduce — hingga **100× lebih cepat** karena memproses data **in-memory**, bukan lewat disk I/O berulang.

| Aspek                 | MapReduce                           | Spark (Batch)                   |
| --------------------- | ----------------------------------- | ------------------------------- |
| **Kecepatan**   | Lambat (disk I/O per stage)         | Cepat (in-memory computing)     |
| **Bahasa**      | Java (utama)                        | Scala, Python, Java, R, SQL     |
| **Iterasi**     | Buruk (baca-tulis disk per iterasi) | Sangat baik (data tetap di RAM) |
| **Ecosystem**   | MapReduce only                      | SQL, ML, Graph, Streaming       |
| **Ease of use** | Kompleks                            | Lebih sederhana (DataFrame API) |

#### 📍 Tools Batch Lainnya

| Teknologi             | Deskripsi                                                        |
| --------------------- | ---------------------------------------------------------------- |
| **Apache Hive** | SQL-like query engine di atas Hadoop — cocok untuk data analyst |
| **Apache Pig**  | High-level scripting untuk data pipeline di Hadoop               |
| **dbt**         | Alat transformasi data modern untuk data warehouse               |

### 1.4 Use Case Batch Processing di Dunia Nyata

| No | Use Case                     | Contoh                                                    | Frekuensi         |
| -- | ---------------------------- | --------------------------------------------------------- | ----------------- |
| 1  | Laporan keuangan             | Bank memproses semua transaksi setiap akhir hari          | Harian            |
| 2  | ETL data warehouse           | Sinkronisasi data dari 50+ sumber ke data warehouse       | Per jam / harian  |
| 3  | Retraining model ML          | Spotify melatih ulang model rekomendasi setiap 24 jam     | Harian / mingguan |
| 4  | Billing & invoice generation | Telkomsel menghitung tagihan 150 juta pelanggan per bulan | Bulanan           |
| 5  | Analisis historis            | Riset epidemiologi atas data kesehatan 10 tahun           | Ad hoc            |

> 🇮🇩 **Indonesia:** BI (Bank Indonesia) memproses data RTGS & SKNBI secara batch setiap end-of-day. Data seluruh transaksi perbankan nasional diolah semalam untuk laporan keesokan harinya.

---

## Bagian 2: Pemrosesan Streaming (20 menit)

### 2.1 Apa Itu Pemrosesan Streaming?

**Pemrosesan Streaming** (atau real-time processing) adalah paradigma di mana data diproses **saat data masuk** — tanpa menunggu dikumpulkan terlebih dahulu.

> 🍕 **Analogi: Kembali ke Dunia Makanan**
>
> Sekarang bayangkan **warung sate pinggir jalan**:
>
> - Pelanggan datang → pesanan langsung **dibakar**
> - Tidak perlu menunggu 100 pelanggan kumpul dulu
> - Hasilnya langsung **disajikan** begitu matang
>
> Inilah cara kerja **stream processing** — setiap data yang masuk langsung diproses, hasilnya langsung tersedia.

```
┌───────────────────────────────────────────────────────────────────┐
│                  PEMROSESAN STREAMING                              │
│                                                                   │
│   Data masuk terus-menerus...                                     │
│   │     │     │     │     │     │     │     │                     │
│   ▼     ▼     ▼     ▼     ▼     ▼     ▼     ▼                     │
│   ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐  ┌─┐                      │
│   │d│→ │d│→ │d│→ │d│→ │d│→ │d│→ │d│→ │d│→  Hasil               │
│   │1│  │2│  │3│  │4│  │5│  │6│  │7│  │8│   langsung!            │
│   └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘  └─┘                      │
│     ↑                                                             │
│     │ Setiap data LANGSUNG diproses begitu masuk                 │
│                                                                   │
│   ⏱️ Latensi: Milidetik hingga Detik                             │
│   📦 Throughput: Sedang (per event/micro-batch)                   │
└───────────────────────────────────────────────────────────────────┘
```

### 2.2 Karakteristik Pemrosesan Streaming

| Karakteristik          | Detail                                                                  |
| ---------------------- | ----------------------------------------------------------------------- |
| **Waktu proses** | Data diproses**segera** saat masuk (event-by-event / micro-batch) |
| **Latensi**      | Sangat rendah (milidetik–detik)                                        |
| **Throughput**   | Per event — lebih rendah dibanding batch, tapi continuous              |
| **Data source**  | Data yang sedang bergerak (in motion / data in flight)                  |
| **Kompleksitas** | Lebih tinggi — harus handle out-of-order, late data, exactly-once      |
| **State**        | Perlu stateful processing untuk windowing dan aggregation               |

### 2.3 Konsep Penting dalam Stream Processing

#### ⏰ Windowing

Karena data streaming tidak memiliki "akhir", kita perlu membuat **jendela waktu (window)** untuk mengelompokkan data.

```
┌─────────────────────────────────────────────────────────────────┐
│                    JENIS-JENIS WINDOW                            │
│                                                                 │
│  1. TUMBLING WINDOW (jendela tetap, tidak overlap)               │
│     ┌─────────┐┌─────────┐┌─────────┐                          │
│     │ 0-5 min ││ 5-10 min││10-15 min│                          │
│     │ ●●●●●   ││ ●●●●    ││ ●●●●●●  │                          │
│     └─────────┘└─────────┘└─────────┘                          │
│                                                                 │
│  2. SLIDING WINDOW (jendela bergeser, bisa overlap)              │
│     ┌─────────────┐                                             │
│     │  0-5 min    │                                             │
│     └─────────────┘                                             │
│        ┌─────────────┐                                          │
│        │  2-7 min    │   ← overlap 3 menit                     │
│        └─────────────┘                                          │
│           ┌─────────────┐                                       │
│           │  4-9 min    │                                       │
│           └─────────────┘                                       │
│                                                                 │
│  3. SESSION WINDOW (berbasis aktivitas, ukuran dinamis)          │
│     ┌───────┐      ┌───────────────┐  ┌────┐                   │
│     │User A │      │   User A      │  │U.A │                   │
│     │●● ●   │ gap  │●●● ●● ●● ●●● │  │●●  │                   │
│     └───────┘      └───────────────┘  └────┘                   │
│     Session 1      Session 2          Session 3                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 🔄 Event Time vs. Processing Time

| Konsep                    | Penjelasan                                                    |
| ------------------------- | ------------------------------------------------------------- |
| **Event Time**      | Waktu kapan event**terjadi** (timestamp di sumber data) |
| **Processing Time** | Waktu kapan event**diproses** oleh sistem               |

> ⚠️ **Mengapa ini penting?**
> Bayangkan sensor IoT mengirim data pukul 10:00 (event time), tetapi karena jaringan lambat, data baru sampai pukul 10:05 (processing time). Sistem harus tahu waktu mana yang digunakan!

#### ✅ Delivery Guarantees

| Guarantee               | Artinya                      | Trade-off                        |
| ----------------------- | ---------------------------- | -------------------------------- |
| **At-most-once**  | Data diproses 0 atau 1 kali  | Cepat, tapi bisa kehilangan data |
| **At-least-once** | Data diproses minimal 1 kali | Aman, tapi bisa duplikat         |
| **Exactly-once**  | Data diproses tepat 1 kali   | Paling aman, tapi paling lambat  |

### 2.4 Teknologi Stream Processing

#### 📍 Apache Kafka Streams

**Kafka Streams** adalah library Java untuk membangun aplikasi streaming di atas Apache Kafka — ringan, tidak butuh cluster terpisah.

```
┌──────────────────────────────────────────────────────────────────┐
│                    KAFKA STREAMS TOPOLOGY                         │
│                                                                  │
│  ┌──────────┐     ┌──────────────────────────┐    ┌──────────┐  │
│  │  Kafka   │     │    KAFKA STREAMS APP     │    │  Kafka   │  │
│  │  Topic   │────▶│                          │───▶│  Topic   │  │
│  │  (input) │     │  Source → Process → Sink │    │ (output) │  │
│  └──────────┘     └──────────────────────────┘    └──────────┘  │
│                                                                  │
│  ✅ Tidak perlu cluster terpisah (embedded)                      │
│  ✅ Exactly-once semantics                                       │
│  ✅ Stateful & stateless operations                              │
│  ⚠️ Terikat pada ekosistem Kafka                                │
└──────────────────────────────────────────────────────────────────┘
```

#### 📍 Apache Flink 

**Apache Flink** adalah distributed stream processing engine dengan latensi sangat rendah dan fitur paling lengkap.

| Fitur                  | Detail                                                   |
| ---------------------- | -------------------------------------------------------- |
| **Paradigma**    | Stream-first (batch = bounded stream)                    |
| **Latensi**      | Sub-milidetik (true event-by-event)                      |
| **State**        | Large-scale stateful computation dengan checkpointing    |
| **Windowing**    | Tumbling, Sliding, Session, Custom                       |
| **Exactly-once** | Ya, via distributed snapshots (Chandy-Lamport algorithm) |

> 💡 Flink memperlakukan **semua data sebagai stream**. Batch processing hanyalah "stream yang ada ujungnya" (bounded stream).

#### 📍 Perbandingan Teknologi Streaming

| Aspek                | Kafka Streams          | Apache Flink             | Spark Structured Streaming |
| -------------------- | ---------------------- | ------------------------ | -------------------------- |
| **Model**      | Event-by-event         | Event-by-event           | Micro-batch                |
| **Latensi**    | Rendah (~ms)           | Sangat rendah (~sub-ms)  | Sedang (~100ms-detik)      |
| **Cluster**    | Tidak perlu (embedded) | Perlu cluster sendiri    | Shared dengan Spark        |
| **Complexity** | Rendah                 | Tinggi                   | Sedang                     |
| **Best for**   | Kafka-centric apps     | Complex event processing | Unified batch + stream     |

### 2.5 Use Case Streaming di Dunia Nyata

| No | Use Case                  | Contoh                                                     | Latensi Target |
| -- | ------------------------- | ---------------------------------------------------------- | -------------- |
| 1  | Fraud detection real-time | Setiap transaksi kartu kredit dicek dalam <100ms           | < 100 ms       |
| 2  | Monitoring infrastruktur  | Alert jika CPU server > 95% selama 30 detik                | < 1 detik      |
| 3  | Live dashboard            | Dashboard COVID-19 update setiap menit                     | < 1 menit      |
| 4  | Real-time recommendation  | YouTube: "Selanjutnya, tonton video ini..."                | < 500 ms       |
| 5  | IoT sensor processing     | Pabrik: deteksi anomali getaran mesin secara instan        | < 100 ms       |
| 6  | Social media trending     | Twitter/X: menghitung trending topic setiap beberapa detik | < 5 detik      |

> 🇮🇩 **Indonesia:** Gojek memproses **>3 juta event per menit** menggunakan Kafka + Flink untuk dynamic pricing, ETA estimation, dan fraud detection secara real-time.

---

## Bagian 3: Perbandingan Mendalam — Latensi, Throughput & Arsitektur (15 menit)

### 3.1 Latensi vs. Throughput

> 💡 Dua metrik paling penting dalam pemrosesan data:

```
┌─────────────────────────────────────────────────────────────────┐
│            LATENSI vs THROUGHPUT — Analogi Jalan Tol             │
│                                                                 │
│  🚗 LATENSI = Waktu tempuh SATU mobil dari Jakarta ke Bandung   │
│     "Berapa lama satu data diproses dari masuk sampai keluar?"  │
│                                                                 │
│  🚛 THROUGHPUT = Jumlah mobil yang lewat tol per jam             │
│     "Berapa banyak data yang bisa diproses per satuan waktu?"   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │   BATCH:    Throughput ████████████████ TINGGI           │    │
│  │             Latensi   ████████████████ TINGGI            │    │
│  │                                                         │    │
│  │   STREAM:   Throughput ████████         SEDANG           │    │
│  │             Latensi   ██               RENDAH ✅         │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ⚡ Trade-off: Sulit mendapat keduanya secara optimal!           │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Tabel Perbandingan Komprehensif: Batch vs. Streaming

| Dimensi                   | 📦 Batch Processing                | 🌊 Stream Processing                     |
| ------------------------- | ---------------------------------- | ---------------------------------------- |
| **Kapan diproses?** | Setelah data terkumpul             | Segera saat data masuk                   |
| **Latensi**         | Tinggi (menit–jam)                | Rendah (ms–detik)                       |
| **Throughput**      | Sangat tinggi                      | Sedang per event                         |
| **Data**            | Bounded (ada awal & akhir)         | Unbounded (terus-menerus)                |
| **Kompleksitas**    | Rendah – sedang                   | Tinggi (state, ordering, late data)      |
| **Fault tolerance** | Restart job dari awal              | Checkpoint & replay                      |
| **Cost**            | Lebih murah (bisa pakai off-peak)  | Lebih mahal (24/7 resources)             |
| **Hasil**           | Akurat & lengkap                   | Approximate, bisa di-refine              |
| **Debugging**       | Mudah (data statis, reproducible)  | Sulit (data bergerak, non-deterministic) |
| **Tools utama**     | MapReduce, Spark (batch), Hive     | Kafka Streams, Flink, Spark Streaming    |
| **Cocok untuk**     | Laporan, ETL, ML training, billing | Alert, monitoring, fraud detection       |

### 3.3 Kapan Menggunakan Batch vs. Streaming?

```
┌─────────────────────────────────────────────────────────────────┐
│              DECISION TREE: BATCH atau STREAMING?                │
│                                                                 │
│         Apakah kamu butuh hasil dalam DETIK?                    │
│                    │                                            │
│            ┌───────┴───────┐                                    │
│            │               │                                    │
│           YA             TIDAK                                  │
│            │               │                                    │
│            ▼               ▼                                    │
│     ┌──────────┐    Apakah data terus                           │
│     │ STREAMING│    mengalir tanpa henti?                       │
│     └──────────┘           │                                    │
│                    ┌───────┴───────┐                             │
│                    │               │                             │
│                   YA             TIDAK                           │
│                    │               │                             │
│                    ▼               ▼                             │
│             ┌──────────┐    ┌──────────┐                        │
│             │ STREAMING│    │  BATCH   │                        │
│             │ atau     │    └──────────┘                        │
│             │ HYBRID   │                                        │
│             └──────────┘                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4 Arsitektur Hybrid: Lambda & Kappa

Dalam praktiknya, banyak sistem menggunakan **kedua paradigma sekaligus**. Ada dua arsitektur populer:

#### 🔷 Lambda Architecture (Nathan Marz, 2011)

Menggabungkan **batch layer** (akurat, lambat) dan **speed layer** (cepat, approximate). Hasil digabungkan di **serving layer**.

```
┌─────────────────────────────────────────────────────────────────┐
│                   LAMBDA ARCHITECTURE                            │
│                                                                 │
│                     ┌── DATA SOURCE ──┐                         │
│                     │   (All Data)    │                         │
│                     └────────┬────────┘                         │
│                       ┌──────┴──────┐                           │
│                       │             │                           │
│                       ▼             ▼                           │
│           ┌───────────────┐  ┌───────────────┐                  │
│           │  BATCH LAYER  │  │  SPEED LAYER  │                  │
│           │  (Hadoop/     │  │  (Storm/Kafka │                  │
│           │   Spark)      │  │   Streams)    │                  │
│           │               │  │               │                  │
│           │ Akurat tapi   │  │ Cepat tapi    │                  │
│           │ lambat        │  │ approximate   │                  │
│           └───────┬───────┘  └───────┬───────┘                  │
│                   │                  │                           │
│                   ▼                  ▼                           │
│           ┌──────────────────────────────────┐                  │
│           │        SERVING LAYER             │                  │
│           │   Gabungkan batch + real-time     │                  │
│           │   → Sajikan ke user/dashboard    │                  │
│           └──────────────────────────────────┘                  │
│                                                                 │
│  ✅ Kelebihan: Akurat + real-time                               │
│  ⚠️ Kekurangan: Kompleks — maintenance 2 pipeline terpisah     │
└─────────────────────────────────────────────────────────────────┘
```

> 🇮🇩 **Contoh:** LinkedIn menggunakan Lambda Architecture — batch layer untuk menghitung koneksi mutual secara akurat, speed layer untuk "People You May Know" real-time.

#### 🔶 Kappa Architecture (Jay Kreps, 2014)

Menyederhanakan Lambda dengan **hanya menggunakan stream processing**. Jika butuh re-processing, cukup replay stream dari awal.

```
┌─────────────────────────────────────────────────────────────────┐
│                   KAPPA ARCHITECTURE                             │
│                                                                 │
│               ┌── DATA SOURCE ──┐                               │
│               │   (All Data)    │                               │
│               └────────┬────────┘                               │
│                        │                                        │
│                        ▼                                        │
│            ┌──────────────────────┐                              │
│            │   STREAM LAYER ONLY │                              │
│            │   (Kafka + Flink)   │                              │
│            │                     │                              │
│            │  Real-time +        │                              │
│            │  Replay jika perlu  │                              │
│            └──────────┬──────────┘                              │
│                       │                                         │
│                       ▼                                         │
│            ┌──────────────────────┐                              │
│            │    SERVING LAYER     │                              │
│            │  Dashboard / API     │                              │
│            └──────────────────────┘                              │
│                                                                 │
│  ✅ Kelebihan: Lebih sederhana, satu codebase                   │
│  ⚠️ Kekurangan: Replay bisa mahal, perlu Kafka retention lama  │
└─────────────────────────────────────────────────────────────────┘
```

#### Perbandingan Lambda vs. Kappa

| Aspek                   | Lambda Architecture             | Kappa Architecture              |
| ----------------------- | ------------------------------- | ------------------------------- |
| **Layer**         | Batch + Speed + Serving         | Stream + Serving                |
| **Kompleksitas**  | Tinggi (2 pipeline)             | Lebih rendah (1 pipeline)       |
| **Akurasi**       | Tinggi (batch layer mengoreksi) | Bergantung pada stream engine   |
| **Maintenance**   | Sulit (sync 2 codebase)         | Lebih mudah                     |
| **Re-process**    | Native (batch layer)            | Replay stream (butuh retention) |
| **Diadopsi oleh** | LinkedIn, Twitter (legacy)      | Uber, Netflix, Confluent        |

---

## 🎯 Aktivitas 1: "Batch or Stream?" Classification Challenge (20 menit)

### Tujuan

Melatih kemampuan mahasiswa mengklasifikasikan skenario dunia nyata ke paradigma pemrosesan yang tepat dan memberikan justifikasi.

### Instruksi (2 menit)

1. Setiap **kelompok** mendapat **2 skenario** dari daftar di bawah
2. Untuk setiap skenario, kelompok harus menentukan:
   - **Batch**, **Streaming**, atau **Hybrid** (keduanya)?
   - **Justifikasi** singkat (2–3 kalimat): mengapa?
   - **Teknologi** apa yang paling cocok?
3. Waktu kerja: **10 menit**
4. Presentasi kilat: **1 menit per kelompok**
5. Gunakan **https://its.id/whiteboard** template yang sudah disediakan

### Template Jawaban 

```
🏢 KELOMPOK [X] — SKENARIO [No]

📌 SKENARIO:
   [Deskripsi skenario]

🏷️ KLASIFIKASI:  □ BATCH  □ STREAMING  □ HYBRID

💡 JUSTIFIKASI (2-3 kalimat):
   _________________________________________________

🔧 TEKNOLOGI YANG DIPILIH:
   Ingest: ________
   Process: ________
   Store: ________
```

### 16 Skenario (2 per Kelompok)

#### Kelompok 1

| No | Skenario                                                                                                         |
| -- | ---------------------------------------------------------------------------------------------------------------- |
| 1  | **Bank BNI** ingin menghitung total transaksi seluruh cabang untuk laporan harian ke OJK setiap jam 23:00. |
| 2  | **GoPay** ingin memblokir transaksi mencurigakan secara otomatis sebelum uang terdebit.                    |

#### Kelompok 2

| No | Skenario                                                                                       |
| -- | ---------------------------------------------------------------------------------------------- |
| 3  | **Netflix** ingin melatih ulang model rekomendasi berdasarkan data tontonan minggu lalu. |
| 4  | **Tokopedia** ingin menampilkan "Produk Sedang Trending 🔥" yang update setiap 5 menit.  |

#### Kelompok 3

| No | Skenario                                                                                                    |
| -- | ----------------------------------------------------------------------------------------------------------- |
| 5  | **Telkomsel** menghitung tagihan bulanan 150 juta pelanggan berdasarkan log pemakaian.                |
| 6  | **Gojek** ingin menghitung harga surge pricing secara real-time berdasarkan demand & supply per zona. |

#### Kelompok 4

| No | Skenario                                                                                                                 |
| -- | ------------------------------------------------------------------------------------------------------------------------ |
| 7  | **Kemenkes** ingin menganalisis data vaksinasi COVID-19 seluruh Indonesia selama 3 tahun untuk laporan penelitian. |
| 8  | **RS Harapan Kita** ingin memonitor detak jantung pasien ICU dan alert dokter jika ada anomali.                    |

#### Kelompok 5

| No | Skenario                                                                                                |
| -- | ------------------------------------------------------------------------------------------------------- |
| 9  | **Spotify** menghasilkan "Spotify Wrapped" — rangkuman lagu yang sering didengar selama setahun. |
| 10 | **YouTube** ingin menghitung dan menampilkan jumlah view video secara live (counter real-time).   |

#### Kelompok 6

| No | Skenario                                                                                                               |
| -- | ---------------------------------------------------------------------------------------------------------------------- |
| 11 | **BMKG** ingin memproses data sensor gempa dari 200 stasiun dan mengirim peringaan tsunami dalam hitungan detik. |
| 12 | **BPS** ingin mengolah data Sensus Penduduk 2025 (270 juta record) untuk analisis demografi.                     |

#### Kelompok 7

| No | Skenario                                                                                                            |
| -- | ------------------------------------------------------------------------------------------------------------------- |
| 13 | **Shopee** ingin mendeteksi review palsu (fake review) dan menghapusnya secara otomatis saat review disubmit. |
| 14 | **Bank Mandiri** ingin membuat data warehouse terintegrasi dari 50 sistem legacy yang berbeda format.         |

#### Kelompok 8

| No | Skenario                                                                                                            |
| -- | ------------------------------------------------------------------------------------------------------------------- |
| 15 | **Grab** ingin menampilkan ETA (Estimated Time of Arrival) driver yang update setiap detik di layar pengguna. |
| 16 | **Traveloka** ingin menganalisis pola booking hotel selama 5 tahun untuk prediksi peak season tahun depan.    |

---

## 🎯 Aktivitas 2: "Arsitektur Pipeline Challenge" (15 menit)

### Tujuan

Setiap kelompok merancang **arsitektur pipeline hybrid** (batch + streaming) untuk skenario industri yang diberikan.

### Instruksi (2 menit)

1. Setiap kelompok mendapat **satu skenario** (berbeda dari Aktivitas 1)
2. Rancang arsitektur yang menjelaskan:
   - **Komponen batch** apa yang digunakan, dan untuk apa?
   - **Komponen streaming** apa yang digunakan, dan untuk apa?
   - **Mengapa perlu keduanya?** (Tidak bisa hanya salah satu)
3. Gambarkan pipeline di **Google Slides** menggunakan template
4. Waktu kerja: **10 menit**, presentasi: **3 menit per kelompok** (dipilih acak 2–3 kelompok)

### Template Arsitektur 

```
🏢 KELOMPOK [X]: [Nama Skenario]

┌─────────── STREAMING PATH ───────────┐
│ [Data Source] → [Ingest] → [Process] → [Output Real-time] │
│  __________    ________    ________    __________________ │
└──────────────────────────────────────┘

┌─────────── BATCH PATH ───────────────┐
│ [Data Store] → [Process] → [Output Batch]                 │
│  __________    ________    __________                     │
└──────────────────────────────────────┘

💡 MENGAPA BUTUH KEDUANYA?
   _________________________________________________
```

### 8 Skenario Hybrid (1 per Kelompok)

| Kelompok | Skenario                                                                                              |
| -------- | ----------------------------------------------------------------------------------------------------- |
| 1        | **E-Wallet "CashIn"**: Perlu fraud detection real-time + laporan keuangan harian ke regulator   |
| 2        | **RS Cerdas "MediTrack"**: Monitor vital sign pasien real-time + analisis tren penyakit bulanan |
| 3        | **Marketplace "BeliAja"**: Rekomendasi produk real-time + analisis perilaku pelanggan bulanan   |
| 4        | **Operator "SignalMax"**: Deteksi gangguan jaringan real-time + perencanaan kapasitas tahunan   |
| 5        | **Platform Belajar "EduFlow"**: Tracking progres siswa real-time + laporan akademik semester    |
| 6        | **Logistik "KirimCepat"**: Tracking paket real-time + optimasi rute bulanan                     |
| 7        | **Smart Factory "ProduksiMax"**: Deteksi anomali mesin real-time + laporan produksi mingguan    |
| 8        | **AgriTech "SawahPintar"**: Alert cuaca & kelembaban real-time + analisis hasil panen tahunan   |

---

## 🎯 Aktivitas 3: Debat — "Apakah Batch Processing Akan Punah?" (10 menit)

### Format Debat

> **Mosi:** _"Di era real-time, batch processing sudah tidak relevan dan akan punah dalam 10 tahun."_

| Peran                               | Kelompok            | Posisi                               |
| ----------------------------------- | ------------------- | ------------------------------------ |
| **TIM PRO** (setuju mosi)     | Kelompok 1, 3, 5, 7 | Batch akan punah, streaming superior |
| **TIM KONTRA** (menolak mosi) | Kelompok 2, 4, 6, 8 | Batch tetap relevan & dibutuhkan     |

### Aturan Debat

1. **Persiapan:** 3 menit (tiap tim diskusi internal)
2. **Opening statement TIM PRO:** 1 menit (1 juru bicara)
3. **Opening statement TIM KONTRA:** 1 menit (1 juru bicara)
4. **Sanggahan bebas:** 3 menit (siapa saja boleh angkat tangan)
5. **Closing:** Dosen merangkum + reveal jawaban

---

## Rangkuman Pertemuan 3

```
┌─────────────────────────────────────────────────────────────────┐
│                   RANGKUMAN HARI INI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. BATCH PROCESSING                                             │
│     • Data dikumpulkan dulu, diproses sekaligus                  │
│     • Latensi tinggi, throughput tinggi                           │
│     • Tools: MapReduce, Spark (batch), Hive                      │
│     • Cocok: laporan, ETL, ML training, billing                  │
│                                                                 │
│  2. STREAM PROCESSING                                            │
│     • Data diproses saat masuk, real-time                        │
│     • Latensi rendah, per event                                  │
│     • Tools: Kafka Streams, Apache Flink, Spark Streaming        │
│     • Cocok: fraud detection, monitoring, real-time dashboard    │
│                                                                 │
│  3. KONSEP PENTING                                               │
│     • Latensi vs Throughput = trade-off                          │
│     • Windowing: Tumbling, Sliding, Session                      │
│     • Event Time vs Processing Time                              │
│     • Delivery Guarantees: at-most, at-least, exactly-once       │
│                                                                 │
│  4. ARSITEKTUR HYBRID                                            │
│     • Lambda = Batch + Speed + Serving (kompleks tapi akurat)    │
│     • Kappa = Stream only + Replay (sederhana tapi perlu Kafka)  │
│                                                                 │
│  5. KEY TAKEAWAY                                                 │
│     ⚡ Batch & Streaming = KOMPLEMEN, bukan kompetisi!           │
│     🎯 Pilih sesuai USE CASE, bukan sesuai hype!                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Preview Pertemuan 4

- **Topik:** Arsitektur dan Komponen Apache Hadoop
- Kita akan deep-dive ke **HDFS**, **YARN**, dan **MapReduce**
- Akan ada **hands-on**: Mengonfigurasi Hadoop single-node cluster dan menjalankan job MapReduce sederhana
- **Persiapkan:** Install VirtualBox/Docker di laptop masing-masing!

---

## Tugas Pertemuan 3

> **Jenis:** Kelompok (sesuai pembagian kelompok yang sudah ditentukan)
> **Deadline:** Sebelum Pertemuan 4 (via LMS)

### Tugas Utama: "Batch vs. Streaming Audit Report"

Pilih **satu perusahaan teknologi** (lokal atau global) dan buat **laporan audit** (format presentasi Google Slides, 10–15 slide) yang menganalisis:

1. **Profil Singkat** perusahaan (industri, skala, jumlah data yang dikelola)
2. **Identifikasi** minimal 3 proses data yang dilakukan perusahaan tersebut
3. **Klasifikasikan** setiap proses: Batch, Streaming, atau Hybrid — dengan **justifikasi**
4. **Gambarkan arsitektur** data pipeline perusahaan tersebut (boleh estimasi berdasarkan riset)
5. **Rekomendasikan** apakah perusahaan perlu mengadopsi Lambda atau Kappa Architecture, dan mengapa
6. **Tantangan:** Identifikasi minimal 2 tantangan jika perusahaan tersebut ingin migrasi dari batch ke streaming

### Contoh Perusahaan yang Bisa Dipilih

| Lokal 🇮🇩                 | Global 🌍                   |
| -------------------------- | --------------------------- |
| Gojek / Tokopedia / Shopee | Netflix / Spotify / YouTube |
| Traveloka / Tiket.com      | Uber / Airbnb               |
| Bank Digital (Jago, Blu)   | Stripe / Square             |
| Telkomsel / XL Axiata      | LinkedIn / Twitter/X        |
| BPJS Kesehatan             | Alibaba / Amazon            |

### Kriteria Penilaian

| Kriteria                                         | Bobot |
| ------------------------------------------------ | ----- |
| Kedalaman riset dan pemahaman perusahaan         | 20%   |
| Ketepatan klasifikasi batch/streaming/hybrid     | 25%   |
| Kualitas arsitektur pipeline yang digambarkan    | 25%   |
| Kualitas rekomendasi Lambda/Kappa dan argumennya | 20%   |
| Kualitas presentasi dan visual                   | 10%   |

---

## Referensi

1. Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media. — Chapter 11: Stream Processing.
2. Marz, N., & Warren, J. (2015). *Big Data: Principles and Best Practices of Scalable Realtime Data Systems*. Manning. — Lambda Architecture.
3. Kreps, J. (2014). "Questioning the Lambda Architecture." *O'Reilly Blog*. — Kappa Architecture proposal.
4. Zaharia, M., et al. (2018). *Learning Spark: Lightning-Fast Data Analytics* (2nd ed.). O'Reilly Media. — Structured Streaming.
5. Hueske, F., & Kalavri, V. (2019). *Stream Processing with Apache Flink*. O'Reilly Media.
6. Narkhede, N., Shapira, G., & Palino, T. (2017). *Kafka: The Definitive Guide*. O'Reilly Media. — Kafka Streams.
7. Dean, J., & Ghemawat, S. (2004). "MapReduce: Simplified Data Processing on Large Clusters." *OSDI '04*.
8. Akidau, T., et al. (2015). "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing." *VLDB*.
9. Gojek Engineering Blog. (2023). "Real-Time Data Processing at Scale."
10. Confluent. (2024). "Kafka vs. Flink: When to Use What."
