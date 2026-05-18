import csv
import random
from datetime import datetime, timedelta

def generate_dummy_data(filename, num_records):
    headers = ['transaction_id', 'user_id', 'product_id', 'amount', 'status', 'transaction_date']
    
    # Simulasikan data kotor: null values, format salah
    statuses = ['COMPLETED', 'FAILED', 'PENDING', None, '']
    
    base_date = datetime(2023, 10, 1)
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(1, num_records + 1):
            user_id = random.randint(100, 150)
            product_id = random.randint(1, 20)
            
            # Simulasi harga kotor (kadang string kosong atau null)
            if random.random() < 0.05:
                amount = ""
            else:
                amount = round(random.uniform(10.0, 500.0), 2)
                
            status = random.choice(statuses)
            
            # Rentang tanggal acak dalam 30 hari
            days_offset = random.randint(0, 30)
            tx_date = base_date + timedelta(days=days_offset)
            date_str = tx_date.strftime('%Y-%m-%d %H:%M:%S')
            
            writer.writerow([i, user_id, product_id, amount, status, date_str])
            
            # Simulasikan duplikasi (5% peluang data ditulis dua kali)
            if random.random() < 0.05:
                writer.writerow([i, user_id, product_id, amount, status, date_str])

if __name__ == '__main__':
    generate_dummy_data('raw_transactions.csv', 1000)
    print("Berhasil men-generate raw_transactions.csv dengan 1000 baris (ditambah sedikit baris duplikat).")
