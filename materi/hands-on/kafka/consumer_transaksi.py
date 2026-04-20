"""
consumer_transaksi.py
=====================
Consumer Kafka untuk Lab 3 Pertemuan 7: Apache Kafka
Membaca transaksi real-time dan menampilkan statistik per 10 pesan.

Penggunaan:
    pip install kafka-python
    python consumer_transaksi.py

Jalankan bersamaan dengan producer_transaksi.py di terminal lain.
"""

import json
from collections import defaultdict
from kafka import KafkaConsumer

# ─── Konfigurasi ────────────────────────────────────────────────────────
BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC = 'transaksi'
GROUP_ID = 'kelompok-analitik'   # Consumer Group ID
STATS_INTERVAL = 10              # Tampilkan statistik setiap N pesan


def print_stats(stats):
    """Tampilkan ringkasan statistik."""
    total = stats['total']
    if total == 0:
        return
    print("\n" + "─" * 55)
    print(f"  📊 STATISTIK REAL-TIME (Total: {total} pesan)")
    print(f"  ✅ Sukses  : {stats['success']:>4} ({stats['success']/total*100:.1f}%)")
    print(f"  ❌ Failed  : {stats['failed']:>4} ({stats['failed']/total*100:.1f}%)")
    print(f"  ⏳ Pending : {stats['pending']:>4} ({stats['pending']/total*100:.1f}%)")
    print(f"  💰 Total Amount : Rp{stats['total_amount']:>15,.0f}")
    print(f"  📈 Terbesar     : Rp{stats['max_amount']:>15,.0f}")
    print(f"  📉 Terkecil     : Rp{stats['min_amount']:>15,.0f}")
    print("─" * 55 + "\n")


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset='latest',      # Baca dari pesan terbaru saja
        enable_auto_commit=True,          # Simpan offset otomatis
        auto_commit_interval_ms=1000,     # Commit setiap 1 detik
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
    )

    print("=" * 60)
    print("👂 Kafka Transaction Consumer - Analitik")
    print(f"   Topic    : {TOPIC}")
    print(f"   Group    : {GROUP_ID}")
    print(f"   Server   : {BOOTSTRAP_SERVERS}")
    print("   Tekan Ctrl+C untuk berhenti")
    print("=" * 60 + "\n")

    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'pending': 0,
        'total_amount': 0,
        'max_amount': 0,
        'min_amount': float('inf'),
    }

    try:
        for message in consumer:
            tx = message.value
            stats['total'] += 1
            stats['total_amount'] += tx.get('amount', 0)
            stats['max_amount'] = max(stats['max_amount'], tx.get('amount', 0))
            stats['min_amount'] = min(stats['min_amount'], tx.get('amount', 0))

            status = tx.get('status', 'unknown')
            if status == 'success':
                stats['success'] += 1
                icon = "✅"
            elif status == 'failed':
                stats['failed'] += 1
                icon = "❌"
            else:
                stats['pending'] += 1
                icon = "⏳"

            risk_icon = {
                'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'
            }.get(tx.get('risk_score', ''), '⚪')

            print(
                f"{icon}{risk_icon} [P{message.partition}:O{message.offset}] "
                f"{tx.get('user_id', '?')} | {tx.get('action', '?')} | "
                f"Rp{tx.get('amount', 0):>10,.0f} | {tx.get('merchant', '?')}"
            )

            if stats['total'] % STATS_INTERVAL == 0:
                print_stats(stats)

    except KeyboardInterrupt:
        print("\n✋ Consumer dihentikan.")
        print_stats(stats)
    finally:
        consumer.close()
        print("📌 Koneksi consumer ditutup.")


if __name__ == '__main__':
    main()
