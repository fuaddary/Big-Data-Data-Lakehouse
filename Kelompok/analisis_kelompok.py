#!/usr/bin/env python3
"""
Analisis Data Preferensi & Pembentukan Kelompok Adil
Mata Kuliah: Big Data dan Data Lakehouse - Kelas C
"""

import csv
import statistics
from collections import Counter, defaultdict
from itertools import combinations

# ============================================================
# BAGIAN 1: PARSING DATA
# ============================================================

def parse_data(filepath):
    students = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)  # skip header
        for row in reader:
            if len(row) < 16 or not row[1].strip():
                continue
            
            # Parse waktu kontribusi ke skor
            jam_raw = row[4].strip()
            if '> 6' in jam_raw or '>6' in jam_raw:
                jam_skor = 4
            elif '4–6' in jam_raw or '4-6' in jam_raw:
                jam_skor = 3
            elif '2–4' in jam_raw or '2-4' in jam_raw:
                jam_skor = 2
            elif '< 2' in jam_raw or '<2' in jam_raw:
                jam_skor = 1
            else:
                jam_skor = 2
            
            # Parse skills
            skills_raw = row[10].strip()
            has_programming = 'Programming' in skills_raw or 'programming' in skills_raw
            has_uiux = 'UI/UX' in skills_raw
            has_analisis = 'Analisis' in skills_raw or 'analisis' in skills_raw
            has_testing = 'Testing' in skills_raw or 'testing' in skills_raw
            has_dokumentasi = 'Dokumentasi' in skills_raw or 'dokumentasi' in skills_raw
            has_presentasi = 'Presentasi' in skills_raw or 'presentasi' in skills_raw
            has_nothing_dominant = 'Tidak ada yang dominan' in skills_raw
            
            # Parse friend preference
            friend_raw = row[12].strip() if len(row) > 12 else '-'
            friend_clean = friend_raw.strip()
            if friend_clean in ['-', 'tidak', 'tidak ada', 'siapapun yang bisa', '']:
                friend_clean = None
            elif friend_clean.startswith('iya') or friend_clean.startswith('Iya'):
                # e.g. "iya betul pak (Nadia Kirana)" -> extract name
                if '(' in friend_clean and ')' in friend_clean:
                    friend_clean = friend_clean[friend_clean.index('(')+1:friend_clean.index(')')]
                else:
                    friend_clean = friend_clean.replace('iya betul pak ', '').replace('Iya', '').strip()
            
            student = {
                'nama': row[1].strip(),
                'nrp': row[2].strip(),
                'jam_kontribusi': jam_raw,
                'jam_skor': jam_skor,
                'waktu_meeting': row[5].strip(),
                'responsif': int(row[6].strip()) if row[6].strip().isdigit() else 3,
                'peran': row[7].strip(),
                'kontribusi_walau_lain_pasif': int(row[8].strip()) if row[8].strip().isdigit() else 3,
                'penanganan_konflik': row[9].strip(),
                'skills_raw': skills_raw,
                'has_programming': has_programming,
                'has_uiux': has_uiux,
                'has_analisis': has_analisis,
                'has_testing': has_testing,
                'has_dokumentasi': has_dokumentasi,
                'has_presentasi': has_presentasi,
                'has_nothing_dominant': has_nothing_dominant,
                'level_teknis': int(row[11].strip()) if row[11].strip().isdigit() else 2,
                'teman_pilihan': friend_clean,
                'preferensi_tim': row[13].strip() if len(row) > 13 else '',
                'deadline_discipline': int(row[14].strip()) if len(row) > 14 and row[14].strip().isdigit() else 3,
                'quality_standard': int(row[15].strip()) if len(row) > 15 and row[15].strip().isdigit() else 3,
            }
            
            # Hitung skor komitmen (rata-rata dari beberapa indikator)
            student['skor_komitmen'] = round(
                (student['jam_skor'] / 4 * 5 +  # normalisasi ke skala 5
                 student['responsif'] + 
                 student['kontribusi_walau_lain_pasif'] + 
                 student['deadline_discipline'] + 
                 student['quality_standard']) / 5, 2
            )
            
            # Hitung skill diversity score (jumlah skill berbeda)
            student['skill_count'] = sum([
                has_programming, has_uiux, has_analisis, 
                has_testing, has_dokumentasi, has_presentasi
            ])
            
            students.append(student)
    
    return students

# ============================================================
# BAGIAN 2: ANALISIS STATISTIK
# ============================================================

def print_analysis(students):
    print("=" * 70)
    print("ANALISIS DATA PREFERENSI KELOMPOK - KELAS C")
    print(f"Total Mahasiswa: {len(students)}")
    print("=" * 70)
    
    # --- Distribusi Peran ---
    print("\n📊 DISTRIBUSI PERAN YANG BIASA DIAMBIL:")
    peran_count = Counter(s['peran'] for s in students)
    for peran, count in peran_count.most_common():
        bar = '█' * count
        print(f"  {peran:35s} : {count:2d} ({count/len(students)*100:.0f}%) {bar}")
    
    # --- Distribusi Level Teknis ---
    print("\n📊 DISTRIBUSI LEVEL TEKNIS (1=pemula, 4=mahir):")
    level_count = Counter(s['level_teknis'] for s in students)
    for level in sorted(level_count.keys()):
        count = level_count[level]
        bar = '█' * count
        label = {1: 'Pemula', 2: 'Dasar', 3: 'Menengah', 4: 'Mahir'}.get(level, '?')
        print(f"  Level {level} ({label:10s}) : {count:2d} ({count/len(students)*100:.0f}%) {bar}")
    
    # --- Distribusi Skills ---
    print("\n📊 DISTRIBUSI KEMAMPUAN TEKNIS:")
    skill_labels = [
        ('has_programming', 'Programming'),
        ('has_uiux', 'UI/UX'),
        ('has_analisis', 'Analisis Kebutuhan'),
        ('has_testing', 'Testing'),
        ('has_dokumentasi', 'Dokumentasi'),
        ('has_presentasi', 'Presentasi'),
        ('has_nothing_dominant', 'Tidak ada dominan'),
    ]
    for key, label in skill_labels:
        count = sum(1 for s in students if s[key])
        bar = '█' * count
        print(f"  {label:25s} : {count:2d} ({count/len(students)*100:.0f}%) {bar}")
    
    # --- Distribusi Jam Kontribusi ---
    print("\n📊 DISTRIBUSI JAM KONTRIBUSI PER MINGGU:")
    jam_count = Counter(s['jam_kontribusi'] for s in students)
    for jam, count in sorted(jam_count.items()):
        bar = '█' * count
        print(f"  {jam:15s} : {count:2d} ({count/len(students)*100:.0f}%) {bar}")
    
    # --- Distribusi Preferensi Tim ---
    print("\n📊 DISTRIBUSI PREFERENSI TIPE TIM:")
    pref_count = Counter(s['preferensi_tim'] for s in students)
    for pref, count in pref_count.most_common():
        bar = '█' * count
        print(f"  {pref:35s} : {count:2d} ({count/len(students)*100:.0f}%) {bar}")
    
    # --- Skor Komitmen ---
    komitmen_scores = [s['skor_komitmen'] for s in students]
    print(f"\n📊 SKOR KOMITMEN (gabungan jam+responsif+kontribusi+deadline+quality):")
    print(f"  Rata-rata : {statistics.mean(komitmen_scores):.2f}")
    print(f"  Median    : {statistics.median(komitmen_scores):.2f}")
    print(f"  Min       : {min(komitmen_scores):.2f}")
    print(f"  Max       : {max(komitmen_scores):.2f}")
    print(f"  Std Dev   : {statistics.stdev(komitmen_scores):.2f}")
    
    # --- Pasangan Teman yang MUTUAL ---
    print("\n🤝 PASANGAN TEMAN YANG SALING MEMILIH (MUTUAL):")
    mutual_pairs = find_mutual_pairs(students)
    if mutual_pairs:
        for a, b in mutual_pairs:
            print(f"  ✅ {a} ↔ {b}")
    else:
        print("  (tidak ada)")
    
    # --- Teman satu arah ---
    print("\n➡️  PERMINTAAN TEMAN (SATU ARAH):")
    for s in students:
        if s['teman_pilihan']:
            target_name = s['teman_pilihan']
            # Check if mutual
            is_mutual = any(
                (a == s['nama'] and b_name_matches(target_name, b, students)) or 
                (b_name_matches(s['nama'], a, students) and b == target_name)
                for a, b in mutual_pairs
            ) if mutual_pairs else False
            if not is_mutual:
                print(f"  {s['nama']:40s} → {target_name}")
    
    print("\n" + "=" * 70)
    return mutual_pairs


def b_name_matches(name1, name2, students):
    """Fuzzy name matching"""
    n1 = name1.lower().strip()
    n2 = name2.lower().strip()
    return n1 == n2 or n1 in n2 or n2 in n1


def find_mutual_pairs(students):
    """Temukan pasangan yang saling memilih."""
    pairs = []
    for s in students:
        if not s['teman_pilihan']:
            continue
        target = s['teman_pilihan'].lower().strip()
        for other in students:
            if other['nama'] == s['nama']:
                continue
            if not other['teman_pilihan']:
                continue
            # Check if other's name matches target AND other chose s
            other_name_lower = other['nama'].lower().strip()
            other_target_lower = other['teman_pilihan'].lower().strip()
            
            name_match = (target in other_name_lower or other_name_lower in target or
                         any(w in other_name_lower for w in target.split() if len(w) > 3))
            reverse_match = (other_target_lower in s['nama'].lower() or 
                            s['nama'].lower() in other_target_lower or
                            any(w in s['nama'].lower() for w in other_target_lower.split() if len(w) > 3))
            
            if name_match and reverse_match:
                pair = tuple(sorted([s['nama'], other['nama']]))
                if pair not in pairs:
                    pairs.append(pair)
    return pairs


# ============================================================
# BAGIAN 3: ALGORITMA PEMBENTUKAN KELOMPOK
# ============================================================

def form_groups(students, mutual_pairs, num_groups=8):
    """
    Algoritma pembentukan kelompok FAIR:
    
    Strategi utama:
    - Kelompok kecil (4 orang) DIISI DULUAN dengan mahasiswa terkuat
      agar mampu bersaing dengan kelompok 5 orang.
    - Pasangan mutual friend tetap dijaga bersama.
    - Distribusi programmer, leader, dan skill merata.
    - Serpentine draft untuk sisa mahasiswa agar keseimbangan terjaga.
    """
    
    n = len(students)
    base_size = n // num_groups
    remainder = n % num_groups  # banyaknya kelompok berukuran (base_size+1)
    num_small = num_groups - remainder  # banyaknya kelompok berukuran base_size
    
    print(f"\n🎯 PEMBENTUKAN KELOMPOK (FAIRNESS-FIRST)")
    print(f"   Total mahasiswa: {n}")
    print(f"   Jumlah kelompok: {num_groups}")
    print(f"   Kelompok besar ({base_size+1} anggota): {remainder}")
    print(f"   Kelompok kecil ({base_size} anggota): {num_small}")
    print(f"   ⚖️ Strategi: Kelompok kecil diisi mahasiswa terkuat untuk kompensasi")
    
    assigned = set()
    # Index 0..(remainder-1) = kelompok besar, remainder..(num_groups-1) = kelompok kecil
    groups = [[] for _ in range(num_groups)]
    
    # ============================================================
    # STEP 1: Bangun kelompok kecil TERLEBIH DAHULU
    #         dengan mahasiswa terkuat (level tinggi, komitmen tinggi,
    #         skill beragam, ada programmer)
    # ============================================================
    
    # Urutkan semua mahasiswa berdasarkan "kekuatan gabungan"
    def student_strength(s):
        return (
            s['level_teknis'] * 2 +     # level teknis paling penting
            s['skor_komitmen'] +          # komitmen
            s['skill_count'] * 0.5 +      # keragaman skill
            (1 if s['has_programming'] else 0) * 2 +  # bonus programmer
            (1 if s['peran'] == 'Koordinator / Leader' else 0)  # bonus leader
        )
    
    all_sorted = sorted(students, key=student_strength, reverse=True)
    
    # Indeks kelompok kecil: dari remainder sampai num_groups-1
    small_group_indices = list(range(remainder, num_groups))
    
    # Ambil mahasiswa terkuat yang BUKAN pasangan mutual untuk kelompok kecil
    # (pasangan mutual akan ditangani terpisah)
    mutual_names = set()
    for a, b in mutual_pairs:
        mutual_names.add(a)
        mutual_names.add(b)
    
    # Kumpulkan kandidat terkuat yang bukan bagian dari pasangan mutual
    non_mutual_sorted = [s for s in all_sorted if s['nama'] not in mutual_names]
    
    # Isi kelompok kecil dengan top students — pastikan ada programmer & skill beragam
    for sg_idx in small_group_indices:
        target_size = base_size  # ukuran kelompok kecil
        
        while len(groups[sg_idx]) < target_size and non_mutual_sorted:
            # Cari kandidat terbaik berikutnya yang melengkapi kelompok ini
            best_candidate = None
            best_score = -1
            
            for candidate in non_mutual_sorted:
                if candidate['nama'] in assigned:
                    continue
                
                # Skor prioritas: seberapa dibutuhkan mahasiswa ini di kelompok ini
                score = student_strength(candidate)
                
                # Bonus jika kelompok belum punya programmer dan kandidat bisa
                if not any(s['has_programming'] for s in groups[sg_idx]) and candidate['has_programming']:
                    score += 5
                
                # Bonus jika kelompok belum punya leader
                if not any(s['peran'] == 'Koordinator / Leader' for s in groups[sg_idx]) \
                   and candidate['peran'] == 'Koordinator / Leader':
                    score += 3
                
                # Bonus keragaman peran
                existing_roles = set(s['peran'] for s in groups[sg_idx])
                if candidate['peran'] not in existing_roles:
                    score += 1
                
                # Bonus keragaman skill
                score += group_needs_skill(groups[sg_idx], candidate) * 0.5
                
                if score > best_score:
                    best_score = score
                    best_candidate = candidate
            
            if best_candidate:
                groups[sg_idx].append(best_candidate)
                assigned.add(best_candidate['nama'])
                non_mutual_sorted = [s for s in non_mutual_sorted if s['nama'] != best_candidate['nama']]
            else:
                break
    
    # ============================================================
    # STEP 2: Tempatkan pasangan mutual ke kelompok besar
    # ============================================================
    big_group_indices = list(range(remainder))
    bg_idx = 0
    for a_name, b_name in mutual_pairs:
        a = next((s for s in students if s['nama'] == a_name), None)
        b = next((s for s in students if s['nama'] == b_name), None)
        if a and b and a['nama'] not in assigned and b['nama'] not in assigned:
            target_gi = big_group_indices[bg_idx % len(big_group_indices)]
            groups[target_gi].append(a)
            groups[target_gi].append(b)
            assigned.add(a['nama'])
            assigned.add(b['nama'])
            bg_idx += 1
    
    # ============================================================
    # STEP 3: Sisa mahasiswa didistribusikan dengan serpentine draft
    #         Prioritas: isi kelompok yang belum penuh, seimbangkan skills
    # ============================================================
    remaining = [s for s in all_sorted if s['nama'] not in assigned]
    
    for student in remaining:
        candidates = list(range(num_groups))
        candidates.sort(key=lambda i: (
            # Prioritas 1: kelompok yang belum penuh
            0 if len(groups[i]) < (base_size + (1 if i < remainder else 0)) else 1,
            # Prioritas 2: kelompok yang paling butuh skill student ini
            -group_needs_skill(groups[i], student),
            # Prioritas 3: kelompok dengan total komitmen terendah (balance)
            sum(s['skor_komitmen'] for s in groups[i]) / max(len(groups[i]), 1),
            # Prioritas 4: kelompok dengan avg level terendah (balance)
            sum(s['level_teknis'] for s in groups[i]) / max(len(groups[i]), 1),
        ))
        
        for target in candidates:
            max_size = base_size + (1 if target < remainder else 0)
            if len(groups[target]) < max_size:
                groups[target].append(student)
                assigned.add(student['nama'])
                break
    
    # ============================================================
    # STEP 4: Post-optimization — cek kelompok tanpa programmer,
    #         coba swap dengan kelompok yang punya 2 programmer
    # ============================================================
    print("\n   🔄 Post-optimization: menyeimbangkan programmer...")
    
    no_prog_groups = [i for i in range(num_groups) if not any(s['has_programming'] for s in groups[i])]
    multi_prog_groups = [i for i in range(num_groups) 
                         if sum(1 for s in groups[i] if s['has_programming']) >= 2]
    
    for np_gi in no_prog_groups:
        if not multi_prog_groups:
            break
        mp_gi = multi_prog_groups[0]
        
        # Cari programmer di multi_prog group yang bisa di-swap
        prog_in_mp = [s for s in groups[mp_gi] if s['has_programming']]
        non_prog_in_np = [s for s in groups[np_gi] if not s['has_programming']]
        
        if prog_in_mp and non_prog_in_np:
            # Swap mahasiswa dengan strength paling mirip
            swap_from = prog_in_mp[-1]  # programmer terlemah dari multi-prog group
            swap_to = max(non_prog_in_np, key=student_strength)  # terkuat dari no-prog group
            
            groups[mp_gi].remove(swap_from)
            groups[np_gi].remove(swap_to)
            groups[mp_gi].append(swap_to)
            groups[np_gi].append(swap_from)
            
            print(f"      Swap: {swap_from['nama']} (Prog) → Kel {np_gi+1}, "
                  f"{swap_to['nama']} → Kel {mp_gi+1}")
            
            # Update multi_prog_groups
            if sum(1 for s in groups[mp_gi] if s['has_programming']) < 2:
                multi_prog_groups.remove(mp_gi)
    
    return groups


def group_needs_skill(group, student):
    """Skor seberapa besar grup butuh skills dari student ini."""
    score = 0
    # If group has no programmer and student has programming
    group_has_prog = any(s['has_programming'] for s in group)
    if not group_has_prog and student['has_programming']:
        score += 3
    
    # If group has no leader and student is leader
    group_has_leader = any(s['peran'] == 'Koordinator / Leader' for s in group)
    if not group_has_leader and student['peran'] == 'Koordinator / Leader':
        score += 2
    
    # If group has no dokumentasi person
    group_has_doc = any(s['has_dokumentasi'] for s in group)
    if not group_has_doc and student['has_dokumentasi']:
        score += 1
    
    # If group has no presentasi person
    group_has_pres = any(s['has_presentasi'] for s in group)
    if not group_has_pres and student['has_presentasi']:
        score += 1
    
    # Role diversity bonus
    existing_roles = set(s['peran'] for s in group)
    if student['peran'] not in existing_roles:
        score += 1
    
    return score


def print_groups(groups):
    """Print hasil kelompok dengan detail."""
    print("\n" + "=" * 70)
    print("📋 HASIL PEMBENTUKAN KELOMPOK")
    print("=" * 70)
    
    all_group_scores = []
    
    for i, group in enumerate(groups):
        print(f"\n{'─' * 70}")
        print(f"  KELOMPOK {i+1} ({len(group)} anggota)")
        print(f"{'─' * 70}")
        
        # Print members
        for j, s in enumerate(group):
            print(f"  {j+1}. {s['nama']:40s} | Level: {s['level_teknis']} | Peran: {s['peran']}")
            print(f"     NRP: {s['nrp']} | Skills: {s['skills_raw']}")
        
        # Group stats
        avg_komitmen = statistics.mean(s['skor_komitmen'] for s in group)
        avg_level = statistics.mean(s['level_teknis'] for s in group)
        has_prog = any(s['has_programming'] for s in group)
        has_leader = any(s['peran'] == 'Koordinator / Leader' for s in group)
        roles = set(s['peran'] for s in group)
        all_skills = set()
        for s in group:
            if s['has_programming']: all_skills.add('Prog')
            if s['has_uiux']: all_skills.add('UI/UX')
            if s['has_analisis']: all_skills.add('Analisis')
            if s['has_testing']: all_skills.add('Testing')
            if s['has_dokumentasi']: all_skills.add('Dok')
            if s['has_presentasi']: all_skills.add('Pres')
        
        print(f"\n  📈 Statistik Kelompok:")
        print(f"     Avg Skor Komitmen : {avg_komitmen:.2f}")
        print(f"     Avg Level Teknis  : {avg_level:.1f}")
        print(f"     Ada Programmer?   : {'✅ Ya' if has_prog else '❌ Tidak'}")
        print(f"     Ada Leader?       : {'✅ Ya' if has_leader else '⚠️ Tidak (perlu ditunjuk)'}")
        print(f"     Keragaman Peran   : {len(roles)} jenis — {', '.join(roles)}")
        print(f"     Coverage Skills   : {len(all_skills)}/6 — {', '.join(sorted(all_skills))}")
        
        all_group_scores.append({
            'group': i+1,
            'size': len(group),
            'avg_komitmen': avg_komitmen,
            'avg_level': avg_level,
            'has_prog': has_prog,
            'has_leader': has_leader,
            'role_diversity': len(roles),
            'skill_coverage': len(all_skills),
        })
    
    # Summary comparison
    print(f"\n{'=' * 70}")
    print("📊 PERBANDINGAN ANTAR KELOMPOK (Fairness Check)")
    print(f"{'=' * 70}")
    print(f"  {'Kel':>4s} | {'Size':>4s} | {'Komitmen':>8s} | {'Level':>5s} | {'Prog':>4s} | {'Leader':>6s} | {'Peran':>5s} | {'Skill':>5s}")
    print(f"  {'─'*4} | {'─'*4} | {'─'*8} | {'─'*5} | {'─'*4} | {'─'*6} | {'─'*5} | {'─'*5}")
    for gs in all_group_scores:
        prog_icon = '✅' if gs['has_prog'] else '❌'
        leader_icon = '✅' if gs['has_leader'] else '⚠️'
        print(f"  {gs['group']:>4d} | {gs['size']:>4d} | {gs['avg_komitmen']:>8.2f} | {gs['avg_level']:>5.1f} | {prog_icon:>4s} | {leader_icon:>6s} | {gs['role_diversity']:>5d} | {gs['skill_coverage']:>5d}")
    
    # Fairness metrics
    komitmen_values = [gs['avg_komitmen'] for gs in all_group_scores]
    level_values = [gs['avg_level'] for gs in all_group_scores]
    print(f"\n  Fairness Metrics:")
    print(f"  Rentang Komitmen : {min(komitmen_values):.2f} – {max(komitmen_values):.2f} (selisih: {max(komitmen_values)-min(komitmen_values):.2f})")
    print(f"  Rentang Level    : {min(level_values):.1f} – {max(level_values):.1f} (selisih: {max(level_values)-min(level_values):.1f})")
    
    all_have_prog = all(gs['has_prog'] for gs in all_group_scores)
    all_have_leader = all(gs['has_leader'] for gs in all_group_scores)
    print(f"  Semua punya Programmer? : {'✅ Ya' if all_have_prog else '❌ Tidak — perlu adjustment manual'}")
    print(f"  Semua punya Leader?     : {'✅ Ya' if all_have_leader else '⚠️ Tidak — beberapa kelompok perlu menunjuk leader'}")


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    import os
    import sys
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Accept class name as command-line argument
    kelas = sys.argv[1] if len(sys.argv) > 1 else 'Kelas C'
    filepath = os.path.join(script_dir, kelas)
    
    print(f"Membaca data dari: {filepath}")
    students = parse_data(filepath)
    print(f"Berhasil parse {len(students)} mahasiswa\n")
    
    # Analisis
    mutual_pairs = print_analysis(students)
    
    # Pembentukan kelompok
    groups = form_groups(students, mutual_pairs, num_groups=8)
    print_groups(groups)
    
    print(f"\n{'=' * 70}")
    print("✅ Selesai!")
    print("=" * 70)

