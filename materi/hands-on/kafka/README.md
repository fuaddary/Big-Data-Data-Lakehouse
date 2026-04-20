# Hands-On Lab: Apache Kafka (Pertemuan 7)

Folder ini berisi semua file yang diperlukan untuk lab Apache Kafka.

## Struktur File

```
kafka/
├── docker-compose.yml          # Setup Apache Kafka (mode KRaft, tanpa ZooKeeper)
├── producer_transaksi.py       # Lab 3: Producer simulasi transaksi pembayaran
├── consumer_transaksi.py       # Lab 3: Consumer analitik statistik real-time
├── consumer_fraud_detector.py  # Lab 3: Consumer fraud detection (group berbeda)
└── README.md                   # Panduan ini
```

## Prasyarat

- Docker Desktop terinstall dan berjalan
- Python 3.8+ terinstall
- Library `kafka-python`: `pip install kafka-python`

## Cara Menjalankan

### Step 1: Jalankan Kafka

```bash
cd materi/hands-on/kafka
docker compose up -d
```

Tunggu ~20 detik lalu verifikasi:

```bash
docker compose ps       # Harus ada kafka-broker dengan status running
docker compose logs kafka | tail -10   # Cek log
```

### Step 2: Masuk ke Container & Buat Topic

```bash
docker exec -it kafka-broker bash

# Buat topic transaksi (3 partisi)
kafka-topics.sh --create --topic transaksi --partitions 3 \
  --replication-factor 1 --bootstrap-server localhost:9092

# Buat topic sensor-suhu (2 partisi)
kafka-topics.sh --create --topic sensor-suhu --partitions 2 \
  --replication-factor 1 --bootstrap-server localhost:9092

# Verifikasi
kafka-topics.sh --list --bootstrap-server localhost:9092

exit
```

### Step 3: Jalankan Lab (3 Terminal Berbeda)

**Terminal 1 — Producer:**
```bash
python producer_transaksi.py
```

**Terminal 2 — Consumer Analitik:**
```bash
python consumer_transaksi.py
```

**Terminal 3 — Fraud Detector:**
```bash
python consumer_fraud_detector.py
```

### Step 4: Matikan Kafka (Setelah Selesai)

```bash
docker compose down
```

## Web UI

Kafka mode KRaft tidak memiliki Web UI bawaan. Untuk monitoring, gunakan:
- `kafka-topics.sh --describe` di dalam container
- `kafka-consumer-groups.sh --describe` di dalam container

## Tips

- Setiap consumer menggunakan **consumer group berbeda** → masing-masing menerima semua pesan
- Offset per consumer group disimpan otomatis → bisa dilanjutkan meski consumer restart
- Gunakan `Ctrl+C` untuk menghentikan producer/consumer dengan bersih
