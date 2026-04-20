"""
consumer_fraud_detector.py
==========================
Consumer Kafka untuk Lab 3 Pertemuan 7: Apache Kafka
Engine deteksi fraud sederhana berbasis aturan (rule-based).

Consumer ini berjalan dalam GROUP BERBEDA dari consumer_transaksi.py,
sehingga menerima semua pesan yang sama secara terpisah.

Penggunaan:
    pip install kafka-python
    python consumer_fraud_detector.py

Jalankan di terminal ketiga (bersamaan dengan producer dan consumer lain).
"""

import json
from collections import defaultdict
from kafka import KafkaConsumer

# ─── Konfigurasi ────────────────────────────────────────────────────────
BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC = 'transaksi'
GROUP_ID = 'fraud-detection-engine'   # Consumer Group BERBEDA!

# ─── Aturan Deteksi Fraud ────────────────────────────────────────────────
HIGH_AMOUNT_THRESHOLD = 1_000_000    # Rp 1 juta → HIGH risk
RAPID_TX_THRESHOLD = 3               # >3 transaksi beruntun = suspect
FAILED_TX_THRESHOLD = 3              # 3 gagal berturut-turut = suspect


def format_amount(amount):
    return f"Rp{amount:,.0f}"


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )

    print("=" * 60)
    print("🔍 Kafka Fraud Detection Engine")
    print(f"   Topic    : {TOPIC}")
    print(f"   Group    : {GROUP_ID}")
    print(f"   Server   : {BOOTSTRAP_SERVERS}")
    print("   Tekan Ctrl+C untuk berhenti")
    print("=" * 60)
    print(f"\n📋 Aturan Aktif:")
    print(f"   🔴 ATURAN 1: Nominal ≥ {format_amount(HIGH_AMOUNT_THRESHOLD)}")
    print(f"   🔴 ATURAN 2: Lebih dari {RAPID_TX_THRESHOLD} transaksi beruntun dari user yang sama")
    print(f"   🔴 ATURAN 3: {FAILED_TX_THRESHOLD} transaksi GAGAL berturut-turut\n")

    # State per user
    user_tx_history = defaultdict(list)   # Semua transaksi per user
    alert_count = 0

    try:
        for message in consumer:
            tx = message.value
            user = tx.get('user_id', 'unknown')
            amount = tx.get('amount', 0)
            status = tx.get('status', 'unknown')

            # Simpan ke history
            user_tx_history[user].append(tx)

            # ── Aturan 1: Nominal sangat besar ──────────────────────────────
            if amount >= HIGH_AMOUNT_THRESHOLD:
                alert_count += 1
                print(
                    f"🚨 ALERT #{alert_count} [Nominal Besar]  "
                    f"{user} → {tx.get('action')} {format_amount(amount)} "
                    f"di {tx.get('merchant', '?')}"
                )

            # ── Aturan 2: Rapid transactions ─────────────────────────────────
            history = user_tx_history[user]
            if len(history) > RAPID_TX_THRESHOLD:
                alert_count += 1
                print(
                    f"🚨 ALERT #{alert_count} [Rapid Tx]      "
                    f"{user} → {len(history)} transaksi beruntun "
                    f"(total: {format_amount(sum(t['amount'] for t in history))})"
                )
                user_tx_history[user] = []  # Reset setelah alert

            # ── Aturan 3: Consecutive failures ───────────────────────────────
            recent_3 = user_tx_history[user][-FAILED_TX_THRESHOLD:]
            if (len(recent_3) == FAILED_TX_THRESHOLD
                    and all(t.get('status') == 'failed' for t in recent_3)):
                alert_count += 1
                print(
                    f"🚨 ALERT #{alert_count} [Repeated Fail] "
                    f"{user} → {FAILED_TX_THRESHOLD} kali gagal berturut-turut!"
                )
                user_tx_history[user] = []  # Reset

            # Tampilkan pesan biasa (non-alert) dengan lebih ringkas
            if amount < HIGH_AMOUNT_THRESHOLD:
                status_icon = "✅" if status == "success" else ("❌" if status == "failed" else "⏳")
                print(
                    f"   {status_icon} Monitoring: {user} | {tx.get('action')} | "
                    f"{format_amount(amount)}"
                )

    except KeyboardInterrupt:
        print(f"\n✋ Fraud Detector dihentikan.")
        print(f"📊 Total alert yang dibangkitkan: {alert_count}")
    finally:
        consumer.close()
        print("📌 Koneksi consumer ditutup.")


if __name__ == '__main__':
    main()
