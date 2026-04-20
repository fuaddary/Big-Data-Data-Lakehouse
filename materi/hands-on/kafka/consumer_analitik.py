"""
consumer_analitik.py
====================
Lab 2 Pertemuan 8: Analitik Statistik Cuaca
Consumer Group: "tim-analitik-bmkg"

BERBEDA dari dashboard-publik → membaca semua pesan secara independen.
Menggunakan manual offset commit (enable_auto_commit=False).
Hitung statistik rolling: min, max, avg suhu per kota.
"""

import json
from collections import defaultdict
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "cuaca-sensor",
    bootstrap_servers=["localhost:9092"],
    group_id="tim-analitik-bmkg",
    auto_offset_reset="earliest",   # Baca dari awal log!
    enable_auto_commit=False,        # Manual commit untuk kontrol penuh
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    key_deserializer=lambda k: k.decode("utf-8") if k else None,
    max_poll_records=100,
)

stats = defaultdict(lambda: {
    "count": 0,
    "sum_suhu": 0.0, "min_suhu": 999.0, "max_suhu": -999.0,
    "sum_lembab": 0.0, "min_lembab": 999.0, "max_lembab": -999.0,
    "kondisi_freq": defaultdict(int),
    "nama": "",
})

print("📊 Analitik BMKG — Consumer Group: tim-analitik-bmkg")
print("   auto_offset_reset=earliest → membaca semua data historis\n")

n = 0
try:
    for msg in consumer:
        d = msg.value
        k = d["kode_kota"]
        s = stats[k]

        s["nama"] = d["nama_kota"]
        s["count"] += 1
        s["sum_suhu"] += d["suhu_celsius"]
        s["min_suhu"] = min(s["min_suhu"], d["suhu_celsius"])
        s["max_suhu"] = max(s["max_suhu"], d["suhu_celsius"])
        s["sum_lembab"] += d["kelembaban_persen"]
        s["min_lembab"] = min(s["min_lembab"], d["kelembaban_persen"])
        s["max_lembab"] = max(s["max_lembab"], d["kelembaban_persen"])
        s["kondisi_freq"][d["kondisi"]] += 1

        n += 1

        # Manual commit setiap 50 pesan
        if n % 50 == 0:
            consumer.commit()

        # Laporan setiap 100 pesan
        if n % 100 == 0:
            print(f"\n📈 LAPORAN STATISTIK ({n} pembacaan diproses)\n" + "─" * 65)
            for kd in sorted(stats):
                sd = stats[kd]
                if sd["count"] == 0:
                    continue
                avg_suhu = sd["sum_suhu"] / sd["count"]
                kondisi_dominan = max(sd["kondisi_freq"], key=sd["kondisi_freq"].get)
                print(
                    f"  {kd} ({sd['nama']:12s}) | N={sd['count']:5d} | "
                    f"Suhu: {sd['min_suhu']:.1f}~{sd['max_suhu']:.1f}°C "
                    f"(avg={avg_suhu:.1f}) | Dominan: {kondisi_dominan}"
                )
            print()

except KeyboardInterrupt:
    consumer.commit()  # Commit offset terakhir sebelum shutdown
    print(f"\n✋ Analitik dihentikan (total {n} pembacaan diproses)")
finally:
    consumer.close()
    print("📌 Koneksi consumer ditutup.")
