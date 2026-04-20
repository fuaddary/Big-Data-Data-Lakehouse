"""
consumer_hitung_transfer.py
===========================
Lab 3 Pertemuan 8: Hitung jumlah record transfer di Kafka.
Deteksi apakah ada duplikat (at-least-once) atau tidak (exactly-once).

Jalankan setelah producer_transfer.py untuk membandingkan kedua mode.
"""

import json
from collections import defaultdict
from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer(
    bootstrap_servers=["localhost:9092"],
    group_id=None,                         # Tanpa group — assign manual
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    key_deserializer=lambda k: k.decode("utf-8") if k else None,
    consumer_timeout_ms=3000,
)

# Assign ke partition 0 dan baca dari awal
consumer.assign([TopicPartition("transfer-bank", 0)])
consumer.seek_to_beginning()

records = []
for msg in consumer:
    records.append(msg.value)
consumer.close()

# ─── Analisis ────────────────────────────────────────────────────
print(f"\n📊 HASIL ANALISIS TRANSFER BANK")
print(f"{'═' * 60}")
print(f"  Total record di Kafka    : {len(records)}")
print(f"  Seharusnya (5 transfer)  : 5 record")
print(f"  Status                   : {'✅ OK — tidak ada duplikat!' if len(records) == 5 else f'⚠️  ADA DUPLIKAT! ({len(records) - 5} ekstra)'}")
print()

id_counts = defaultdict(list)
for r in records:
    id_counts[r["id"]].append(r)

print(f"  {'Transfer ID':15s} | {'Muncul':>6s} | {'Nominal':>15s} | Status")
print(f"  {'─'*58}")
total_nominal_broker = 0
for tid in sorted(id_counts):
    cnt = len(id_counts[tid])
    nominal = id_counts[tid][0]["nominal"]
    total_nominal_broker += nominal * cnt
    status = "✅ OK" if cnt == 1 else f"⚠️  DUPLIKAT! ({cnt}×)"
    print(f"  {tid:15s} | {cnt:6d} | Rp{nominal:>12,.0f} | {status}")

seharusnya = sum(r["nominal"] for r in records[:5]) if records else 0
print(f"\n  Total nominal BENAR      : Rp{500_000+1_200_000+75_000+3_000_000+250_000:>12,.0f}")
print(f"  Total nominal di broker  : Rp{total_nominal_broker:>12,.0f}")
if total_nominal_broker != 5_025_000:
    print(f"  ⚠️  SELISIH              : Rp{total_nominal_broker - 5_025_000:>12,.0f} (akibat duplikat!)")
print()
