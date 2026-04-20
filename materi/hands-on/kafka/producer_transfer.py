"""
producer_transfer.py
====================
Lab 3 Pertemuan 8: Exactly-Once & Idempotent Producer
Simulasi transfer bank dengan dua mode delivery semantics.

Penggunaan:
    python producer_transfer.py at-least-once
    python producer_transfer.py exactly-once

Bandingkan jumlah record di Kafka dengan consumer_hitung_transfer.py!
"""

import json
import time
import sys
from kafka import KafkaProducer
from kafka.errors import KafkaError

MODE = sys.argv[1] if len(sys.argv) > 1 else "at-least-once"

TRANSFERS = [
    {"id": "TXF-001", "dari": "ACC-1001", "ke": "ACC-2001", "nominal": 500_000},
    {"id": "TXF-002", "dari": "ACC-1002", "ke": "ACC-2002", "nominal": 1_200_000},
    {"id": "TXF-003", "dari": "ACC-1003", "ke": "ACC-2003", "nominal": 75_000},
    {"id": "TXF-004", "dari": "ACC-1004", "ke": "ACC-2004", "nominal": 3_000_000},
    {"id": "TXF-005", "dari": "ACC-1005", "ke": "ACC-2005", "nominal": 250_000},
]

if MODE == "at-least-once":
    print("⚠️  MODE: AT-LEAST-ONCE (retries aktif, duplikat MUNGKIN terjadi)")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
        acks="all",
        retries=5,
        enable_idempotence=False,   # Idempotence OFF → duplikat bisa terjadi!
    )
elif MODE == "exactly-once":
    print("✅  MODE: EXACTLY-ONCE (idempotent producer, duplikat TIDAK mungkin)")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
        acks="all",
        enable_idempotence=True,    # Broker assign PID + seq number
        max_in_flight_requests_per_connection=5,
    )
else:
    print(f"❌ Unknown mode: {MODE}. Gunakan: python producer_transfer.py at-least-once")
    sys.exit(1)

print(f"\n💸 Mengirim {len(TRANSFERS)} transfer (masing-masing 2 kali — simulasi retry)...\n")

for tx in TRANSFERS:
    try:
        # Pengiriman pertama
        future = producer.send(
            topic="transfer-bank",
            key=tx["id"],
            value={**tx, "attempt": 1}
        )
        future.get(timeout=5)
        print(f"  ✅ SENT (attempt 1): {tx['id']} — Rp{tx['nominal']:,}")

        time.sleep(0.05)

        # Simulasi RETRY (network blip menyebabkan producer kirim ulang)
        future2 = producer.send(
            topic="transfer-bank",
            key=tx["id"],
            value={**tx, "attempt": 2, "note": "RETRY setelah network blip"}
        )
        future2.get(timeout=5)
        print(f"  🔄 RETRY (attempt 2): {tx['id']}")

    except KafkaError as e:
        print(f"  ❌ Error: {e}")

producer.flush()
producer.close()
print(f"\n✅ Selesai. Jalankan consumer_hitung_transfer.py untuk cek hasilnya!")
