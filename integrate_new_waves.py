import csv
import os
import re

WORKSPACE = r'e:\DCCBC'

all_master_file = os.path.join(WORKSPACE, 'all_companies_strictly_verified.csv')
sponsor_master_file = os.path.join(WORKSPACE, 'sponsor_company_list_strictly_verified.csv')
org_list_file = os.path.join(WORKSPACE, 'organisation_list.csv')

# 1. Read existing all_companies_strictly_verified
existing_rows = []
seen_keys = set()

if os.path.exists(all_master_file):
    with open(all_master_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            existing_rows.append(r)
            key = (r['Company Name'].strip().lower(), r['Host Organization Name'].strip().lower(), r['Event Name'].strip().lower())
            seen_keys.add(key)

print(f"Initial strictly verified records: {len(existing_rows)}")

# 2. Ingest colleges_verified_sponsors.csv
colleges_file = os.path.join(WORKSPACE, 'colleges_verified_sponsors.csv')
added_colleges = 0
if os.path.exists(colleges_file):
    with open(colleges_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            cname = r.get('Company Name', '').strip()
            org = r.get('Host Organization Name', '').strip()
            ev = r.get('Event Name', '').strip()
            link = r.get('Direct Proof Link', '').strip()
            tier = r.get('Sponsorship Tier', 'Corporate Sponsor').strip()
            sec = r.get('Industry Sector', 'Corporate Partner').strip()
            
            if not cname or not ev:
                continue
            key = (cname.lower(), org.lower(), ev.lower())
            if key not in seen_keys:
                seen_keys.add(key)
                existing_rows.append({
                    'SL No': str(len(existing_rows) + 1),
                    'Company Name': cname,
                    'Industry Sector': sec,
                    'Sponsorship Tier': tier,
                    'Host Organization Name': org,
                    'Event Name': ev,
                    'Direct Proof Link': link
                })
                added_colleges += 1

print(f"Added {added_colleges} records from colleges_verified_sponsors.csv")

# 3. Ingest public_univs_verified_sponsors.csv
univs_file = os.path.join(WORKSPACE, 'public_univs_verified_sponsors.csv')
added_univs = 0
if os.path.exists(univs_file):
    with open(univs_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            cname = r.get('Sponsor / Partner Name', '').strip()
            org = r.get('Host Club Name', '').strip()
            inst = r.get('Institution', '').strip()
            full_org = f"{org} - {inst}" if inst and org not in inst else org
            ev = r.get('Event Name', '').strip()
            link = r.get('Exact Proof Permalink', '').strip()
            if not link or 'facebook.com' not in link:
                link = r.get('Individual Event URL', '').strip()
            tier = r.get('Sponsorship Tier', 'Corporate Sponsor').strip()
            sec = 'Corporate Partner / Industry Sponsor'
            
            # Simple sector inferences
            c_low = cname.lower()
            if any(w in c_low for w in ['bank', 'finance', 'ipdc', 'idlc', 'ebl', 'brac bank', 'ucb', 'scb']):
                sec = 'Banking & Financial Services'
            elif any(w in c_low for w in ['ielts', 'edbase', 'mentors', 'learning', 'academy', 'education', 'edtech', 'school']):
                sec = 'EdTech & Education'
            elif any(w in c_low for w in ['beverage', 'juice', 'frutika', 'food', 'coca-cola', 'akij', 'pran', 'nestle', 'unilever', 'marico', 'square', 'city group', 'teer']):
                sec = 'FMCG & Consumer Goods'
            elif any(w in c_low for w in ['telecom', 'grameenphone', 'banglalink', 'robi']):
                sec = 'Telecommunications'
            elif any(w in c_low for w in ['tech', 'software', 'digital', 'gold kinen', 'it']):
                sec = 'Technology & Software'
            elif any(w in c_low for w in ['tv', 'radio', 'newspaper', 'standard', 'times', 'somoy', 'channel']):
                sec = 'News & Broadcast Media'

            if not cname or not ev:
                continue
            key = (cname.lower(), org.lower(), ev.lower())
            if key not in seen_keys:
                seen_keys.add(key)
                existing_rows.append({
                    'SL No': str(len(existing_rows) + 1),
                    'Company Name': cname,
                    'Industry Sector': sec,
                    'Sponsorship Tier': tier,
                    'Host Organization Name': full_org,
                    'Event Name': ev,
                    'Direct Proof Link': link
                })
                added_univs += 1

print(f"Added {added_univs} records from public_univs_verified_sponsors.csv")
print(f"Total master strictly verified records: {len(existing_rows)}")

# Re-number SL No
for idx, r in enumerate(existing_rows, 1):
    r['SL No'] = str(idx)

# Save all_companies_strictly_verified.csv
with open(all_master_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['SL No', 'Company Name', 'Industry Sector', 'Sponsorship Tier', 'Host Organization Name', 'Event Name', 'Direct Proof Link'])
    writer.writeheader()
    writer.writerows(existing_rows)

# Save sponsor_company_list_strictly_verified.csv (Company Name, Sponsor Event Name, Organization Name, Event Link)
with open(sponsor_master_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Company Name', 'Sponsor Event Name', 'Organization Name', 'Event Link'])
    writer.writeheader()
    for r in existing_rows:
        writer.writerow({
            'Company Name': r['Company Name'],
            'Sponsor Event Name': r['Event Name'],
            'Organization Name': r['Host Organization Name'],
            'Event Link': r['Direct Proof Link']
        })

print("Successfully written updated strictly verified master files.")

# 4. Update organisation_list.csv
org_rows = []
org_names_seen = set()
with open(org_list_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        oname = r['Organisation name'].strip()
        org_names_seen.add(oname.lower())
        # Check if status needs to be updated to 100%
        for comp_name in ['voice of business', 'iba communication', 'ducc', 'rucc', 'rubc', 'cucc', 'jubc', 'jnucc', 'kucc', 'buet edc', 'sustcc', 'bup', 'iut', 'rcf', 'cuet', 'butex', 'adamjee', 'josephite', 'notre dame', 'dhaka commerce', 'baf shaheen']:
            if comp_name in oname.lower():
                r['status'] = '100%'
        org_rows.append(r)

# New clubs to append
new_clubs = [
    ("DRMC Business and Career Club (DRMC BAC Club) - Dhaka Residential Model College, Dhaka", 8, "3rd DRMC International Business Summit 2026, BGMEA Presents 1st DRMC National Business Carnival, Milon Mela Presents Virtual Versatility Spectrum, National Accounting Olympiad 2025, 2nd DRMC Business Carnival, Mission Admission, Business Influencia", "https://www.facebook.com/drmcbacclub2019/events", "100%"),
    ("Holy Cross College Business Club (HCCBC) - Tejgaon, Dhaka", 7, "7th Inter College Business Festival 2026, 6th Inter College Business Festival 2025, 5th HCCBC Inter College Business Festival, Intra Olympiad, Wall Magazine Contest", "https://www.facebook.com/100057154341909", "100%"),
    ("Dhaka College Career Club (DCCC) - Dhaka College, Dhaka", 4, "DCCC Career Roadmap Conclave, Higher Study Guidance & BCS Guideline Session, Banking & Finance Career Development Workshop", "https://www.facebook.com/profile.php?id=61567544350291", "100%"),
    ("Chittagong Cantonment Public College Business & Career Club (CCPC BAC Club) - Chattogram", 4, "CCPC Business Carnival, Intra Case Challenge, Career Conclave, Banking Olympiad", "https://www.facebook.com/ccpcbusinessandcareerclub/events", "100%"),
    ("Kabi Nazrul Government College Business and Career Club (KNGC BAC Club) - Old Dhaka", 3, "KNGC Career Summit, Intra College Business Quiz, Corporate Skill Bootcamp", "https://www.facebook.com/profile.php?id=61589536306768", "100%"),
    ("Birshreshtha Munshi Abdur Rouf Public College Business & Career Club (BMARPC) - Peelkhana, Dhaka", 3, "Career Talks: Charting Your Path to Success, Web Design & Tech Workshop, Intra Business Contest", "https://www.facebook.com/Business.CRC/events", "100%"),
    ("Milestone College Business Club (MCBC) - Uttara, Dhaka", 3, "Milestone Business Olympiad, Intra Case Competition, Leadership Bootcamp", "https://www.facebook.com/milestonecollege.official", "100%"),
    ("SOS Hermann Gmeiner College Commerce Club - Mirpur, Dhaka", 3, "SHGC Business Carnival, Intra College Olympiad, Presentation Fest", "https://www.facebook.com/soshgcollege", "100%"),
    ("ACPS Business & Economics Club - ASBEC (Army Cantonment Public School & College)", 3, "2nd Intra Business Brilliance Challenge 2026, 1st Intra Business Brilliance Challenge, ACPS Economics Summit & Idea Challenge", "https://www.facebook.com/100090512895292", "100%"),
    ("Shamsul Hoque Khan School & College Nutrition & Business Network (SHKSC)", 3, "Notre Dame Business Summit Outreach Host Session, SHKSC Health & Nutrition Fest, Annual College Health & Business Olympiad", "https://www.facebook.com/shkscnc", "100%"),
    ("Amrita Lal Dey College Debating & Business Club (ALDC) - Barishal", 4, "Amrita Lal Dey Divisional Inter-College Debate Championship, Annual College Cultural & Talent Fest, ALDC Higher Education Guidance Seminar, ALDC Intra College Olympiad", "https://www.facebook.com/aldcbsl", "100%")
]

for name, ev_count, ev_names, link, status in new_clubs:
    match_found = False
    for r in org_rows:
        if name.split(' - ')[0].lower() in r['Organisation name'].lower() or r['Organisation name'].lower() in name.lower():
            match_found = True
            r['status'] = '100%'
            if int(r.get('event number', 0) or 0) < ev_count:
                r['event number'] = str(ev_count)
                r['event names'] = ev_names
            break
    if not match_found:
        org_rows.append({
            'Organisation name': name,
            'event number': str(ev_count),
            'event names': ev_names,
            'Event Link': link,
            'status': status
        })

print(f"Total organisations in list: {len(org_rows)}")

with open(org_list_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Organisation name', 'event number', 'event names', 'Event Link', 'status'])
    writer.writeheader()
    writer.writerows(org_rows)

print("Successfully updated organisation_list.csv.")
