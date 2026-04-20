"""
producer_cuaca.py
==================
Lab 2 Pertemuan 8: Pipeline Cuaca IoT Real-Time
Simulasi jaringan sensor cuaca 5 kota Jawa Timur.

Key = kode kota → semua data kota yang sama ke partisi yang sama.
Menggunakan idempotent producer (acks=all, enable_idempotence=True).

Setup:
    pip install kafka-python
    docker compose up -d
    # Buat topic dulu:
    docker exec -it kafka-broker \
      kafka-topics.sh --create --topic cuaca-sensor \
      --partitions 5 --replication-factor 1 \
      --config retention.ms=3600000 \
      --bootstrap-server localhost:9092
"""

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

KOTA = {
    "SBY": {"nama": "Surabaya",   "lat": -7.2575, "lon": 112.7521, "base_temp": 30},
    "MLG": {"nama": "Malang",     "lat": -7.9797, "lon": 112.6304, "base_temp": 24},
    "MDN": {"nama": "Madiun",     "lat": -7.6299, "lon": 111.5238, "base_temp": 27},
    "JMB": {"nama": "Jember",     "lat": -8.1845, "lon": 113.6683, "base_temp": 28},
    "BNY": {"nama": "Banyuwangi", "lat": -8.2191, "lon": 114.3691, "base_temp": 29},
}

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8"),
    acks="all",
    enable_idempotence=True,
    linger_ms=10,
    compression_type="lz4",
)

print("🌤️  Sensor Cuaca Jawa Timur — Producer Aktif")
print("   Mengirim data setiap ~0.2 detik | Ctrl+C untuk berhenti\n")

count = 0
try:
    while True:
        for kode, info in KOTA.items():
            jam = datetime.now().hour
            siklus_harian = 3 * (1 - abs(jam - 14) / 14)
            suhu = round(info["base_temp"] + siklus_harian + random.uniform(-1.5, 1.5), 1)
            kelembaban = round(random.uniform(55, 95), 1)
            kecepatan_angin = round(random.uniform(0, 40), 1)
            tekanan = round(random.uniform(1008, 1020), 1)

            if kelembaban > 85:
                kondisi = random.choice(["Hujan Ringan", "Hujan Lebat", "Mendung"])
            elif kelembaban > 70:
                kondisi = random.choice(["Berawan", "Mendung", "Cerah"])
            else:
                kondisi = random.choice(["Cerah", "Berawan"])

            reading = {
                "kode_kota": kode,
                "nama_kota": info["nama"],
                "latitude": info["lat"],
                "longitude": info["lon"],
                "suhu_celsius": suhu,
                "kelembaban_persen": kelembaban,
                "kecepatan_angin_kmh": kecepatan_angin,
                "tekanan_hpa": tekanan,
                "kondisi": kondisi,
                "timestamp": datetime.now().isoformat(),
                "sensor_id": f"BMKG-{kode}-001",
            }

            producer.send(topic="cuaca-sensor", key=kode, value=reading)
            count += 1

        if count % 25 == 0:
            producer.flush()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {count} pembacaan terkirim")

        time.sleep(0.2)

except KeyboardInterrupt:
    print(f"\n✋ Producer dihentikan. Total terkirim: {count} pembacaan sensor")
finally:
    producer.flush()
    producer.close()
    print("📌 Koneksi producer ditutup.")
