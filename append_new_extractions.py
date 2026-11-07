import csv, os

WORKSPACE = r'e:\DCCBC'

new_sponsors = [
    {
        'Company Name': 'BGMEA (Bangladesh Garment Manufacturers and Exporters Association)',
        'Industry Sector': 'Trade & Industry Association',
        'Sponsorship Tier': 'Title Sponsor',
        'Host Organization Name': 'DRMC Business and Career Club (DRMC BAC) - Dhaka Residential Model College',
        'Event Name': 'BGMEA Presents 1st DRMC National Business Carnival 2023',
        'Direct Proof Link': 'https://www.facebook.com/events/1164993830887391/'
    },
    {
        'Company Name': 'Milon Mela',
        'Industry Sector': 'E-Commerce / Consumer Brand',
        'Sponsorship Tier': 'Title Sponsor',
        'Host Organization Name': 'DRMC Business and Career Club (DRMC BAC) - Dhaka Residential Model College',
        'Event Name': 'Milon Mela Presents Virtual Versatility Spectrum Season 1',
        'Direct Proof Link': 'https://www.facebook.com/events/847217451666969/'
    },
    {
        'Company Name': 'English Carnival Bangladesh',
        'Industry Sector': 'Education & Training',
        'Sponsorship Tier': 'Title Sponsor',
        'Host Organization Name': 'DRMC Business and Career Club (DRMC BAC) - Dhaka Residential Model College',
        'Event Name': 'English Carnival Bangladesh presents National Accounting Olympiad 2025',
        'Direct Proof Link': 'https://www.facebook.com/events/1135606848740760/'
    },
    {
        'Company Name': 'Dhaka Bank PLC',
        'Industry Sector': 'Banking & Financial Services',
        'Sponsorship Tier': 'Title Sponsor',
        'Host Organization Name': 'FINACT - Finance and Accounting Club of BRAC University',
        'Event Name': 'Dhaka Bank PLC Presents ACCQUANTUM',
        'Direct Proof Link': 'https://www.facebook.com/events/1601109748218287/'
    },
    {
        'Company Name': 'Pubali Bank PLC',
        'Industry Sector': 'Banking & Financial Services',
        'Sponsorship Tier': 'Title Sponsor',
        'Host Organization Name': 'FINACT - Finance and Accounting Club of BRAC University',
        'Event Name': 'Pubali Bank Presents EXCELERATE 2025',
        'Direct Proof Link': 'https://www.facebook.com/events/895348089483638/'
    },
    {
        'Company Name': 'YOUR Campus',
        'Industry Sector': 'EdTech & Youth Platform',
        'Sponsorship Tier': 'Title Sponsor',
        'Host Organization Name': 'BUET Entrepreneurship Development Club (BUET EDC)',
        'Event Name': 'YOUR Campus Presents BUET-EDC Fresh Minds Case Clash 2.0',
        'Direct Proof Link': 'https://www.facebook.com/events/1386052282527983/'
    },
    {
        'Company Name': 'YOUR Campus',
        'Industry Sector': 'EdTech & Youth Platform',
        'Sponsorship Tier': 'Title Sponsor',
        'Host Organization Name': 'BUET Entrepreneurship Development Club (BUET EDC)',
        'Event Name': 'YOUR Campus Presents BUET-EDC Freshers Reception 2025',
        'Direct Proof Link': 'https://www.facebook.com/events/1093912115910159/'
    },
    {
        'Company Name': 'SMC Plus (Social Marketing Company)',
        'Industry Sector': 'Pharmaceuticals & Consumer Health',
        'Sponsorship Tier': 'Title Sponsor',
        'Host Organization Name': 'BUP Business & Communication Club (BUP BCC)',
        'Event Name': 'SMC Plus Presents BizNation 2.0',
        'Direct Proof Link': 'https://www.facebook.com/events/1690185031570851/'
    }
]

# Read existing sponsors
file_7col = os.path.join(WORKSPACE, 'all_companies_strictly_verified.csv')
with open(file_7col, mode='r', encoding='utf-8') as f:
    existing = list(csv.DictReader(f))

existing_keys = set((r['Company Name'].strip().lower(), r['Event Name'].strip().lower()) for r in existing)

added = 0
for ns in new_sponsors:
    k = (ns['Company Name'].strip().lower(), ns['Event Name'].strip().lower())
    if k not in existing_keys:
        ns['SL No'] = str(len(existing) + 1)
        existing.append(ns)
        existing_keys.add(k)
        added += 1

if added > 0:
    headers = ['SL No', 'Company Name', 'Industry Sector', 'Sponsorship Tier', 'Host Organization Name', 'Event Name', 'Direct Proof Link']
    with open(file_7col, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(existing)

    # 4-col csv
    file_4col = os.path.join(WORKSPACE, 'sponsor_company_list_strictly_verified.csv')
    with open(file_4col, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Company Name', 'Sponsor Event Name', 'Organization Name', 'Event Link'])
        for r in existing:
            writer.writerow([r['Company Name'], r['Event Name'], r['Host Organization Name'], r['Direct Proof Link']])

    print(f'Successfully added {added} new verified sponsors. Total sponsors now: {len(existing)}')
else:
    print('All sponsors already in database.')

# Update organisation_list.csv
orgs_file = os.path.join(WORKSPACE, 'organisation_list.csv')
with open(orgs_file, mode='r', encoding='utf-8') as f:
    org_rows = list(csv.DictReader(f))

org_names_existing = set(r['Organisation name'].strip().lower() for r in org_rows)

# 1. Update DRMC Business and Career Club
drmc_found = False
for r in org_rows:
    if 'DRMC' in r['Organisation name'] or 'Residential Model' in r['Organisation name']:
        r['event number'] = '8'
        r['event names'] = '3rd DRMC International Business Summit 2026, Milon Mela Presents Virtual Versatility Spectrum Season 1, English Carnival Bangladesh presents National Accounting Olympiad 2025, 5th Anniversary Special Business Summit Bangladesh Season 01, 2nd DRMC National Business Carnival 2024, BGMEA Presents 1st DRMC National Business Carnival 2023, Business Influencia, Mission Admission'
        r['status'] = '100%'
        drmc_found = True
        break

if not drmc_found:
    org_rows.append({
        'Organisation name': 'DRMC Business and Career Club (DRMC BAC) - Dhaka Residential Model College',
        'event number': '8',
        'event names': '3rd DRMC International Business Summit 2026, Milon Mela Presents Virtual Versatility Spectrum Season 1, English Carnival Bangladesh presents National Accounting Olympiad 2025, 5th Anniversary Special Business Summit Bangladesh Season 01, 2nd DRMC National Business Carnival 2024, BGMEA Presents 1st DRMC National Business Carnival 2023, Business Influencia, Mission Admission',
        'Event Link': 'https://www.facebook.com/drmcbacclub2019/events',
        'status': '100%'
    })

# 2. Update FINACT BRAC University
finact_found = False
for r in org_rows:
    if 'FINACT' in r['Organisation name']:
        r['event number'] = '5'
        r['event names'] = 'Dhaka Bank PLC Presents ACCQUANTUM, Pubali Bank Presents EXCELERATE 2025, EXCELERATE 2025, Unlock Global Opportunities: Explore Career Prospects in Corporate Finance Trends, FEMFEST 2.0'
        r['status'] = '100%'
        finact_found = True
        break

if not finact_found:
    org_rows.append({
        'Organisation name': 'FINACT - Finance and Accounting Club of BRAC University',
        'event number': '5',
        'event names': 'Dhaka Bank PLC Presents ACCQUANTUM, Pubali Bank Presents EXCELERATE 2025, EXCELERATE 2025, Unlock Global Opportunities: Explore Career Prospects in Corporate Finance Trends, FEMFEST 2.0',
        'Event Link': 'https://www.facebook.com/finact.bracu/events',
        'status': '100%'
    })

# Write back organisation_list.csv
headers_org = ['Organisation name', 'event number', 'event names', 'Event Link', 'status']
with open(orgs_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers_org)
    writer.writeheader()
    writer.writerows(org_rows)

print(f'Total organisations now in list: {len(org_rows)}')
