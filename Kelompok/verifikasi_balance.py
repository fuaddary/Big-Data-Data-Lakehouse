#!/usr/bin/env python3
"""
Verifikasi balance kelompok yang sudah di-adjust manual oleh dosen.
Membaca NRP dari pembagian_kelompok_kelas_C.md, lalu cross-reference ke data survey.
"""

import csv
import re
import statistics
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 1. Parse data survey
# ============================================================
def parse_survey(filepath):
    students = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            if len(row) < 16 or not row[1].strip():
                continue
            nrp = row[2].strip()
            
            jam_raw = row[4].strip()
            if '> 6' in jam_raw: jam_skor = 4
            elif '4–6' in jam_raw or '4-6' in jam_raw: jam_skor = 3
            elif '2–4' in jam_raw or '2-4' in jam_raw: jam_skor = 2
            else: jam_skor = 1
            
            skills_raw = row[10].strip()
            has_prog = 'Programming' in skills_raw
            has_uiux = 'UI/UX' in skills_raw
            has_analisis = 'Analisis' in skills_raw
            has_testing = 'Testing' in skills_raw
            has_dok = 'Dokumentasi' in skills_raw
            has_pres = 'Presentasi' in skills_raw
            
            responsif = int(row[6]) if row[6].strip().isdigit() else 3
            kontribusi = int(row[8]) if row[8].strip().isdigit() else 3
            deadline = int(row[14]) if len(row) > 14 and row[14].strip().isdigit() else 3
            quality = int(row[15]) if len(row) > 15 and row[15].strip().isdigit() else 3
            level = int(row[11]) if row[11].strip().isdigit() else 2
            
            skor_komitmen = round((jam_skor/4*5 + responsif + kontribusi + deadline + quality) / 5, 2)
            skill_count = sum([has_prog, has_uiux, has_analisis, has_testing, has_dok, has_pres])
            
            students[nrp] = {
                'nama': row[1].strip(),
                'nrp': nrp,
                'level': level,
                'peran': row[7].strip(),
                'skor_komitmen': skor_komitmen,
                'has_prog': has_prog,
                'has_uiux': has_uiux,
                'has_analisis': has_analisis,
                'has_testing': has_testing,
                'has_dok': has_dok,
                'has_pres': has_pres,
                'skill_count': skill_count,
                'skills_raw': skills_raw,
            }
    return students

# ============================================================
# 2. Parse kelompok dari markdown
# ============================================================
def parse_groups_md(filepath):
    groups = []
    current_group = None
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'## Kelompok (\d+)', line)
            if m:
                current_group = {'id': int(m.group(1)), 'nrps': []}
                groups.append(current_group)
                continue
            if current_group is not None:
                # Match table row with NRP
                m2 = re.search(r'\|\s*\d+\s*\|.*?\|\s*(502\d+)\s*\|', line)
                if m2:
                    current_group['nrps'].append(m2.group(1).strip())
    return groups

# ============================================================
# 3. Analisis
# ============================================================
survey = parse_survey(os.path.join(script_dir, 'Kelas C'))
groups = parse_groups_md(os.path.join(script_dir, 'pembagian_kelompok_kelas_C.md'))

# Crosscheck: semua mahasiswa masuk?
all_nrps_in_groups = set()
for g in groups:
    for nrp in g['nrps']:
        all_nrps_in_groups.add(nrp)

all_nrps_in_survey = set(survey.keys())
missing_from_groups = all_nrps_in_survey - all_nrps_in_groups
extra_in_groups = all_nrps_in_groups - all_nrps_in_survey

print("=" * 75)
print("VERIFIKASI BALANCE KELOMPOK (SETELAH ADJUSTMENT DOSEN)")
print("=" * 75)

if missing_from_groups:
    print(f"\n⚠️  MAHASISWA BELUM MASUK KELOMPOK ({len(missing_from_groups)}):")
    for nrp in missing_from_groups:
        s = survey[nrp]
        print(f"   {s['nama']:40s} | {nrp} | Level {s['level']} | {s['peran']}")
if extra_in_groups:
    print(f"\n⚠️  NRP DI KELOMPOK TAPI TIDAK ADA DI SURVEY: {extra_in_groups}")
if not missing_from_groups and not extra_in_groups:
    print("\n✅ Semua 39 mahasiswa sudah masuk kelompok, tidak ada duplikat.")

# Check for duplicates
all_nrps_list = []
for g in groups:
    all_nrps_list.extend(g['nrps'])
if len(all_nrps_list) != len(set(all_nrps_list)):
    from collections import Counter
    dupes = [nrp for nrp, cnt in Counter(all_nrps_list).items() if cnt > 1]
    print(f"\n⚠️  NRP DUPLIKAT (muncul di >1 kelompok): {dupes}")
    for d in dupes:
        for g in groups:
            if d in g['nrps']:
                print(f"     {d} → Kelompok {g['id']}")

print(f"\nTotal mahasiswa dalam kelompok: {len(all_nrps_list)}")
print(f"Total mahasiswa dalam survey: {len(survey)}")

# Per-group analysis
print(f"\n{'=' * 75}")
print(f"{'Kel':>4s} | {'Size':>4s} | {'Komit':>6s} | {'Level':>5s} | {'Prog':>5s} | {'Leader':>6s} | {'Skill':>6s} | {'SkDiv':>5s}")
print(f"{'─'*4:>4s} | {'─'*4:>4s} | {'─'*6:>6s} | {'─'*5:>5s} | {'─'*5:>5s} | {'─'*6:>6s} | {'─'*6:>6s} | {'─'*5:>5s}")

group_stats = []
for g in groups:
    members = [survey[nrp] for nrp in g['nrps'] if nrp in survey]
    if not members:
        continue
    
    avg_komitmen = statistics.mean(m['skor_komitmen'] for m in members)
    avg_level = statistics.mean(m['level'] for m in members)
    has_prog = any(m['has_prog'] for m in members)
    has_leader = any(m['peran'] == 'Koordinator / Leader' for m in members)
    
    all_skills = set()
    for m in members:
        if m['has_prog']: all_skills.add('Prog')
        if m['has_uiux']: all_skills.add('UI/UX')
        if m['has_analisis']: all_skills.add('Analisis')
        if m['has_testing']: all_skills.add('Testing')
        if m['has_dok']: all_skills.add('Dok')
        if m['has_pres']: all_skills.add('Pres')
    
    roles = set(m['peran'] for m in members)
    
    prog_icon = '✅' if has_prog else '❌'
    leader_icon = '✅' if has_leader else '⚠️'
    
    print(f"{g['id']:>4d} | {len(members):>4d} | {avg_komitmen:>6.2f} | {avg_level:>5.1f} | {prog_icon:>5s} | {leader_icon:>6s} | {len(all_skills):>4d}/6 | {len(roles):>5d}")
    
    group_stats.append({
        'id': g['id'], 'size': len(members),
        'avg_komitmen': avg_komitmen, 'avg_level': avg_level,
        'has_prog': has_prog, 'has_leader': has_leader,
        'skill_cov': len(all_skills), 'role_div': len(roles),
        'members': members, 'all_skills': all_skills, 'roles': roles,
    })

# Fairness summary
print(f"\n{'=' * 75}")
print("⚖️  FAIRNESS METRICS")
print(f"{'=' * 75}")

komitmens = [gs['avg_komitmen'] for gs in group_stats]
levels = [gs['avg_level'] for gs in group_stats]
skills = [gs['skill_cov'] for gs in group_stats]

print(f"  Komitmen  | min: {min(komitmens):.2f} | max: {max(komitmens):.2f} | selisih: {max(komitmens)-min(komitmens):.2f} | stdev: {statistics.stdev(komitmens):.2f}")
print(f"  Level     | min: {min(levels):.1f}  | max: {max(levels):.1f}  | selisih: {max(levels)-min(levels):.1f}  | stdev: {statistics.stdev(levels):.2f}")
print(f"  Skill Cov | min: {min(skills)}      | max: {max(skills)}      | selisih: {max(skills)-min(skills)}")

prog_count = sum(1 for gs in group_stats if gs['has_prog'])
leader_count = sum(1 for gs in group_stats if gs['has_leader'])
print(f"\n  Kelompok dengan Programmer : {prog_count}/{len(group_stats)}")
print(f"  Kelompok dengan Leader     : {leader_count}/{len(group_stats)}")

# Detail per kelompok  
print(f"\n{'=' * 75}")
print("📋 DETAIL PER KELOMPOK")
print(f"{'=' * 75}")

for gs in group_stats:
    print(f"\n── Kelompok {gs['id']} ({gs['size']} anggota) ──")
    for m in gs['members']:
        prog_tag = ' [PROG]' if m['has_prog'] else ''
        leader_tag = ' [LEADER]' if m['peran'] == 'Koordinator / Leader' else ''
        print(f"   {m['nama']:40s} | Lv.{m['level']} | Komit:{m['skor_komitmen']:.1f} | {m['peran']}{prog_tag}{leader_tag}")
    
    issues = []
    if not gs['has_prog']: issues.append('❌ Tanpa programmer')
    if not gs['has_leader']: issues.append('⚠️ Tanpa natural leader')
    if gs['skill_cov'] < 4: issues.append(f'⚠️ Skill coverage rendah ({gs["skill_cov"]}/6)')
    if gs['avg_komitmen'] < 3.5: issues.append(f'⚠️ Komitmen rendah ({gs["avg_komitmen"]:.2f})')
    if gs['role_div'] <= 2: issues.append(f'⚠️ Keragaman peran rendah ({gs["role_div"]} jenis)')
    
    if issues:
        for issue in issues:
            print(f"   {issue}")
    else:
        print(f"   ✅ Balanced!")
    
    print(f"   Skills: {', '.join(sorted(gs['all_skills']))}")
    print(f"   Peran: {', '.join(sorted(gs['roles']))}")

# Kelompok kecil vs besar comparison
print(f"\n{'=' * 75}")
print("⚖️  KELOMPOK KECIL vs KELOMPOK BESAR")
print(f"{'=' * 75}")

small_groups = [gs for gs in group_stats if gs['size'] == 4]
big_groups = [gs for gs in group_stats if gs['size'] == 5]

if small_groups and big_groups:
    sg = small_groups[0]
    bg_avg_k = statistics.mean(gs['avg_komitmen'] for gs in big_groups)
    bg_avg_l = statistics.mean(gs['avg_level'] for gs in big_groups)
    
    sg_label = f"Kel Kecil (Kel {sg['id']})"
    print(f"  {'Metrik':<20s} | {sg_label:>20s} | {'Rata-rata Kel Besar':>20s} | {'Status':>10s}")
    print(f"  {'─'*20} | {'─'*20} | {'─'*20} | {'─'*10}")
    
    k_status = '✅ FAIR' if sg['avg_komitmen'] >= bg_avg_k else '⚠️ RENDAH'
    l_status = '✅ FAIR' if sg['avg_level'] >= bg_avg_l else '⚠️ RENDAH'
    s_status = '✅ FAIR' if sg['skill_cov'] >= 5 else '⚠️'
    bg_avg_skill = statistics.mean(gs['skill_cov'] for gs in big_groups)
    bg_prog_count = sum(1 for gs in big_groups if gs['has_prog'])
    bg_leader_count = sum(1 for gs in big_groups if gs['has_leader'])
    
    prog_label = '✅ Ya' if sg['has_prog'] else '❌ Tidak'
    leader_label = '✅ Ya' if sg['has_leader'] else '⚠️ Tidak'
    bg_prog_label = f"{bg_prog_count}/{len(big_groups)} punya"
    bg_leader_label = f"{bg_leader_count}/{len(big_groups)} punya"
    
    print(f"  {'Avg Komitmen':<20s} | {sg['avg_komitmen']:>20.2f} | {bg_avg_k:>20.2f} | {k_status:>10s}")
    print(f"  {'Avg Level':<20s} | {sg['avg_level']:>20.1f} | {bg_avg_l:>20.1f} | {l_status:>10s}")
    print(f"  {'Skill Coverage':<20s} | {sg['skill_cov']:>18d}/6 | {bg_avg_skill:>18.1f}/6 | {s_status:>10s}")
    print(f"  {'Ada Programmer':<20s} | {prog_label:>20s} | {bg_prog_label:>20s} |")
    print(f"  {'Ada Leader':<20s} | {leader_label:>20s} | {bg_leader_label:>20s} |")

print(f"\n{'=' * 75}")
print("✅ Verifikasi selesai!")
print(f"{'=' * 75}")
