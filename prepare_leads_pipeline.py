import csv
import os

WORKSPACE = r'e:\DCCBC'
leads_file = os.path.join(WORKSPACE, 'company_sponsor_leads_verified.csv')

headers = [
    'SL No',
    'Company Name',
    'Industry Sector',
    'Contact Person Name',
    'Designation / Role',
    'Email Address',
    'LinkedIn Profile URL',
    'Contact Source / Verification URL',
    'Official Phone / Corporate PBX',
    'Office Location (Bangladesh)',
    'Target Sponsoring Fit for College Events'
]

# Create or initialize the leads file if not present
if not os.path.exists(leads_file):
    with open(leads_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
    print("Created empty company_sponsor_leads_verified.csv with full schema.")
else:
    print("company_sponsor_leads_verified.csv already exists.")
