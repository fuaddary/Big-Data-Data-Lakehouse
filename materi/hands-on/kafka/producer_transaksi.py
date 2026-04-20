"""
producer_transaksi.py
=====================
Producer Kafka untuk Lab 3 Pertemuan 7: Apache Kafka
Mensimulasikan transaksi pembayaran real-time dari berbagai pengguna.

Penggunaan:
    pip install kafka-python
    python producer_transaksi.py

Pastikan Kafka sudah berjalan (docker compose up -d)
"""

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# ─── Konfigurasi ────────────────────────────────────────────────────────
BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC = 'transaksi'
SEND_INTERVAL = 0.5  # detik antara setiap pesan

# ─── Data Simulasi ───────────────────────────────────────────────────────
USERS = ['user001', 'user002', 'user003', 'user004', 'user005']
ACTIONS = ['transfer', 'topup', 'payment', 'withdrawal', 'purchase']
MERCHANTS = ['Tokopedia', 'Shopee', 'GoPay', 'OVO', 'Indomaret', 'Alfamart']
STATUSES = ['success', 'success', 'success', 'failed', 'pending']  # 60% success


def generate_transaction():
    """Membuat data transaksi acak."""
    user = random.choice(USERS)
    amount = random.randint(5000, 2_000_000)
    return {
        'transaction_id': f"TX{random.randint(10000, 99999)}",
        'user_id': user,
        'action': random.choice(ACTIONS),
        'amount': amount,
        'merchant': random.choice(MERCHANTS),
        'timestamp': datetime.now().isoformat(),
        'status': random.choice(STATUSES),
        'risk_score': (
            'HIGH' if amount > 1_000_000
            else 'MEDIUM' if amount > 500_000
            else 'LOW'
        )
    }


def main():
    # Inisialisasi Producer
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        # Pengaturan reliabilitas
        acks='all',          # Tunggu konfirmasi dari semua replika
        retries=3,           # Coba kirim ulang 3 kali jika gagal
        linger_ms=5,         # Buffer 5ms sebelum kirim (batching kecil)
    )

    print("=" * 60)
    print("🚀 Kafka Transaction Producer dimulai")
    print(f"   Topic    : {TOPIC}")
    print(f"   Server   : {BOOTSTRAP_SERVERS}")
    print(f"   Interval : {SEND_INTERVAL}s/pesan")
    print("   Tekan Ctrl+C untuk berhenti")
    print("=" * 60 + "\n")

    count = 0
    try:
        while True:
            tx = generate_transaction()

            # Key = user_id → Semua transaksi user yang sama → partisi yang sama
            future = producer.send(
                topic=TOPIC,
                key=tx['user_id'],
                value=tx
            )

            metadata = future.get(timeout=10)
            count += 1

            risk_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(tx['risk_score'], "⚪")
            status_icon = "✅" if tx['status'] == "success" else ("❌" if tx['status'] == "failed" else "⏳")

            print(
                f"[{count:04d}] {status_icon} {risk_icon} "
                f"P{metadata.partition}:O{metadata.offset} | "
                f"{tx['user_id']} → {tx['action']} "
                f"Rp{tx['amount']:>10,.0f} | {tx['merchant']}"
            )

            time.sleep(SEND_INTERVAL)

    except KeyboardInterrupt:
        print(f"\n✋ Producer dihentikan. Total terkirim: {count} pesan")
    finally:
        producer.flush()
        producer.close()
        print("📌 Koneksi producer ditutup.")


if __name__ == '__main__':
    main()
