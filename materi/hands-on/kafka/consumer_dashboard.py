"""
consumer_dashboard.py
=====================
Lab 2 Pertemuan 8: Dashboard Cuaca Real-Time
Consumer Group: "dashboard-publik"
Tampilkan suhu terkini per kota + peringatan cuaca ekstrem.
"""

import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "cuaca-sensor",
    bootstrap_servers=["localhost:9092"],
    group_id="dashboard-publik",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    key_deserializer=lambda k: k.decode("utf-8") if k else None,
)

suhu_terkini = {}
alert_count = 0

def cetak_dashboard():
    print("\n" + "═" * 60)
    print("  🌡️  DASHBOARD CUACA JAWA TIMUR — REAL-TIME  ")
    print("═" * 60)
    for kode in sorted(suhu_terkini):
        d = suhu_terkini[kode]
        icon = "⛈️" if "Hujan" in d["kondisi"] else ("🌥️" if "Mendung" in d["kondisi"] else "☀️")
        print(
            f"  {icon} {d['nama']:12s} | "
            f"Suhu: {d['suhu']:5.1f}°C | "
            f"💧{d['lembab']:5.1f}% | "
            f"🌬️{d['angin']:5.1f}km/h | "
            f"{d['kondisi']}"
        )
    print("═" * 60 + "\n")

print("📺 Dashboard Cuaca — Consumer Group: dashboard-publik")
print("   Menunggu data sensor (auto_offset_reset=latest)...\n")

n = 0
try:
    for msg in consumer:
        d = msg.value
        kode = d["kode_kota"]
        suhu_terkini[kode] = {
            "nama": d["nama_kota"],
            "suhu": d["suhu_celsius"],
            "lembab": d["kelembaban_persen"],
            "angin": d["kecepatan_angin_kmh"],
            "kondisi": d["kondisi"],
        }

        if d["suhu_celsius"] >= 35:
            alert_count += 1
            print(f"🔴 HEAT ALERT #{alert_count}: {d['nama_kota']} → {d['suhu_celsius']}°C!")
        if d["kecepatan_angin_kmh"] >= 35:
            alert_count += 1
            print(f"🌪️  WIND ALERT #{alert_count}: {d['nama_kota']} → {d['kecepatan_angin_kmh']} km/h!")

        n += 1
        if n % 10 == 0:
            cetak_dashboard()

except KeyboardInterrupt:
    print(f"\n✋ Dashboard dihentikan. Total alert: {alert_count}")
finally:
    consumer.close()
    print("📌 Koneksi consumer ditutup.")
