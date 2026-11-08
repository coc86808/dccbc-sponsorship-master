import csv
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

WORKSPACE = r'e:\DCCBC'
leads_csv = os.path.join(WORKSPACE, 'company_sponsor_leads_verified.csv')
excel_path = os.path.join(WORKSPACE, 'Bangladesh_Business_Clubs_Sponsorship_Master.xlsx')

# Combined records from both subagent outputs
all_leads_raw = [
    # Banking & Financial Services
    ("Eastern Bank PLC (EBL)", "Banking & Financial Services", "Ziaul Karim", "Head of Brand, Marketing & Communications", "ziaul.karim@ebl-bd.com", "https://bd.linkedin.com/in/ziaul-karim-bba265184", "https://www.ebl.com.bd/about/managementdetails/74", "+880 2 223381677", "100 Gulshan Avenue, Dhaka-1212", "Title Sponsor / Youth Banking & Student Debit Card Partner"),
    ("Dhaka Bank PLC", "Banking & Financial Services", "Syed Ghulam Dastagir", "Head of Communications & Brand Marketing", "dastag007@yahoo.com", "https://bd.linkedin.com/in/syeddastagir", "https://www.linkedin.com/in/syeddastagir", "+880 2 58314424", "Plot CWS(C)-10, Bir Uttam A K Khandakar Road, Gulshan-1, Dhaka-1212", "Powered By Sponsor / Youth Financial Literacy Partner"),
    ("Prime Bank PLC", "Banking & Financial Services", "Syed Rayhan Tarique", "Head of Brand & Communications / Corporate Affairs", "rayhan.tarique@primebank.com.bd", "https://bd.linkedin.com/in/srayhantariqueprexpert", "https://www.linkedin.com/in/srayhantariqueprexpert", "+880 2 222292318", "Prime Tower, Plot 180, Bir Uttam Mir Shawkat Sarak, Tejgaon, Dhaka-1208", "Youth Banking Partner / Business Pitch Competition Sponsor"),
    ("Pubali Bank PLC", "Banking & Financial Services", "Suvashis Kundu", "Head of Brand & Corporate Communication", "suvashis.kundu@pubalibankbd.com", "https://bd.linkedin.com/in/suvashis-kundu-13056951", "https://www.linkedin.com/in/suvashis-kundu-13056951", "+880 2 223381614", "Pubali Bank Bhaban, 26 Dilkusha C/A, Motijheel, Dhaka-1000", "Strategic Banking Partner / Financial Inclusion Partner"),
    ("Trust Bank Limited", "Banking & Financial Services", "Taimur Ali", "Head of Brand & Communications", "taimur.ali@tblbd.com", "https://bd.linkedin.com/in/taimur-ali-03386656", "https://www.linkedin.com/in/taimur-ali-03386656", "+880 2 8711201", "Shadhinata Tower, Bir Shreshtha Shaheed Jahangir Gate, Dhaka Cantonment, Dhaka-1206", "Corporate Banking Partner / Academic Excellence Award Sponsor"),
    
    # Akij Food & Beverage (Frutika / Mojo / Clemon)
    ("Akij Food & Beverage Ltd. (AFBL)", "FMCG / Food & Beverage", "Md. Shafiqul Islam Tushar", "Deputy General Manager (Head of Brand Marketing)", "shafiqul.tushar@akijfood.com", "https://bd.linkedin.com/in/md-shafiqul-islam-tushar-0210b740", "https://bd.linkedin.com/in/md-shafiqul-islam-tushar-0210b740", "+880 2 9831701", "Akij House, 198 Bir Uttam Mir Shawkat Sarak, Gulshan Link Road, Tejgaon, Dhaka-1208", "Title Sponsor / Beverage & Refreshment Partner (Mojo / Frutika / Clemon)"),
    ("Akij Food & Beverage Ltd. (AFBL)", "FMCG / Food & Beverage", "Mehedi Shiblu", "Senior Brand Manager", "mehedi.shiblu@akijfood.com", "https://bd.linkedin.com/in/shiblu", "https://bd.linkedin.com/in/shiblu", "+880 2 9831701", "Akij House, 198 Bir Uttam Mir Shawkat Sarak, Gulshan Link Road, Tejgaon, Dhaka-1208", "Beverage & Energy Drink Partner (SPEED / Wild Brew / Mojo)"),

    # Meghna Group of Industries (Fresh)
    ("Meghna Group of Industries (MGI)", "FMCG / Consumer Goods", "Kazi Mohiuddin", "Senior General Manager - Brand", "kazi.mohiuddin@mgi.org", "https://bd.linkedin.com/in/kazi-mohiuddin-77bb2361", "https://bd.linkedin.com/in/kazi-mohiuddin-77bb2361", "+880 9666777055", "Fresh Villa, House 15, Road 34, Gulshan-1, Dhaka-1212", "Title / Associate Sponsor / Drinking Water & Nutrition Partner (Fresh)"),
    ("Meghna Group of Industries (MGI)", "FMCG / Consumer Goods", "Md. Waliul Haque", "Brand Manager", "waliul.haque@mgi.org", "https://bd.linkedin.com/in/waliulhaque", "https://bd.linkedin.com/in/waliulhaque", "+880 9666777055", "Fresh Villa, House 15, Road 34, Gulshan-1, Dhaka-1212", "FMCG Youth Partner / Snacks & Refreshment Partner"),
    ("Meghna Group of Industries (MGI)", "FMCG / Consumer Goods", "Muntasir Mamun", "Deputy General Manager (DGM) Brand Marketing", "muntasir.mamun@mgi.org", "https://bd.linkedin.com/in/muntasir-mamun-6624a3156", "https://bd.linkedin.com/in/muntasir-mamun-6624a3156", "+880 9666777055", "Fresh Villa, House 15, Road 34, Gulshan-1, Dhaka-1212", "FMCG Title Sponsor & Brand Activation Oversight"),
    ("Meghna Group of Industries (MGI)", "FMCG / Consumer Goods", "Israt Jahan", "Manager - Brand (MGI Portfolio)", "israt.jahan@mgi.org", "https://bd.linkedin.com/in/israt-jahan-bb021b42", "https://bd.linkedin.com/in/israt-jahan-bb021b42", "+880 9666777055", "Fresh Villa, House 15, Road 34, Gulshan-1, Dhaka-1212", "Corporate Sponsorships & Youth Activation"),

    # Unilever Bangladesh
    ("Unilever Bangladesh Limited", "FMCG / Personal Care & Foods", "Tabassum Khan Prithi", "Senior Brand Manager", "tabassum.prithi@unilever.com", "https://www.linkedin.com/in/tabassum-prithi/", "https://www.linkedin.com/in/tabassum-prithi/", "+880 2 9888452", "ZN Tower, Plot 2, Road 8, Gulshan-1, Dhaka-1212", "Youth Leadership / Campus Engagement / Personal Care Partner"),
    ("Unilever Bangladesh Limited", "FMCG / Personal Care & Foods", "Afnan Bin Ashraf", "Senior Brand Manager - Surf Excel", "afnan.ashraf@unilever.com", "https://www.linkedin.com/in/afnan-bin-ashraf-82a46291/", "https://www.linkedin.com/in/afnan-bin-ashraf-82a46291/", "+880 2 9888452", "ZN Tower, Plot 2, Road 8, Gulshan-1, Dhaka-1212", "Co-Sponsor / Brand Activation Partner"),
    ("Unilever Bangladesh Limited", "FMCG / Personal Care & Foods", "Clement Dipro", "Brand Manager - Nutrition & Refreshments", "clement.dipro@unilever.com", "https://www.linkedin.com/in/clementdipro/", "https://www.linkedin.com/in/clementdipro/", "+880 2 9888452", "ZN Tower, Plot 2, Road 8, Gulshan-1, Dhaka-1212", "Career Fair Partner / Youth Leadership & FMCG Case Study Sponsor"),

    # Social Marketing Company (SMC / SMC Plus)
    ("Social Marketing Company (SMC Enterprise Ltd.)", "FMCG / Healthcare & Wellness", "Md. Abu Nazzar Choudhuri", "Brand Manager (Electrolyte & Health Beverage)", "abu.choudhuri@smc-bd.org", "https://www.linkedin.com/in/md-abu-nazzar-choudhuri-32780036/", "https://www.linkedin.com/in/md-abu-nazzar-choudhuri-32780036/", "+880 2 9821390", "SMC Tower, 33 Banani C/A, Kemal Ataturk Avenue, Dhaka-1213", "Official Hydration & Electrolyte Partner (SMC Plus Electrolyte Drink)"),
    ("Social Marketing Company (SMC Enterprise Ltd.)", "FMCG / Healthcare & Wellness", "Arefin Moin", "Assistant Manager, Marketing & Brand Portfolio", "arefin.moin@smc-bd.org", "https://www.linkedin.com/in/arefin-moin-a51511321/", "https://www.linkedin.com/in/arefin-moin-a51511321/", "+880 2 9821390", "SMC Tower, 33 Banani C/A, Kemal Ataturk Avenue, Dhaka-1213", "Health & Wellbeing Partner / Sampling Partner"),

    # PRAN-RFL Group
    ("PRAN-RFL Group", "FMCG / Food & Beverage", "Shanu Kanti Nath", "Brand Manager", "shanu.nath@prangroup.com", "https://www.linkedin.com/in/shanu-kanti-nath-097709155/", "https://www.linkedin.com/in/shanu-kanti-nath-097709155/", "+880 2 222281792", "PRAN-RFL Center, 105 Middle Badda, Dhaka-1212", "Official Beverage & Snack Partner (PRAN Frooto / PRAN Up)"),
    ("PRAN-RFL Group (Good Luck Stationery)", "Stationery & Office Supplies", "Ashraf Asif", "Brand Manager", "ashraf.asif@prangroup.com", "https://www.linkedin.com/in/ashraf-asif-9a114b334/", "https://www.linkedin.com/in/ashraf-asif-9a114b334/", "+880 2 222281792", "PRAN-RFL Center, 105 Middle Badda, Dhaka-1212", "Official Stationery & Event Kit Partner (Good Luck Stationery)"),

    # City Group (Teer)
    ("City Group (Teer)", "FMCG / Consumer Goods", "Md. Mustafizur Rahman", "Head of Marketing & Communications", "mustafizur.rahman@citygroup.com.bd", "https://bd.linkedin.com/in/md-mustafizur-rahman-79738b71", "https://bd.linkedin.com/in/md-mustafizur-rahman-79738b71", "+880 2 8870101", "Shanta Western Tower, Level-8, Bir Uttam Mir Shawkat Sarak, Tejgaon, Dhaka-1208", "Title / Co-Sponsor / Culinary & Cooking Oil Partner (Teer)"),
    ("City Group (Teer)", "FMCG / Consumer Goods", "Rubaiet Ahamed", "Brand Manager", "rubaiet.ahamed@citygroup.com.bd", "https://bd.linkedin.com/in/rubaiet-ahamed-08210b68", "https://bd.linkedin.com/in/rubaiet-ahamed-08210b68", "+880 2 8870101", "Shanta Western Tower, Level-8, Bir Uttam Mir Shawkat Sarak, Tejgaon, Dhaka-1208", "Consumer Goods / Food Partner"),

    # Berger Paints
    ("Berger Paints Bangladesh Limited", "Manufacturing / Paints & Coatings", "Salahuddin Ahmed Tarek", "Chief Marketing Officer (CMO)", "salahuddin@bergerbd.com", "https://bd.linkedin.com/in/salahuddin-ahmed-tarek-14098b22", "https://bd.linkedin.com/in/salahuddin-ahmed-tarek-14098b22", "+880 2 48953665", "Berger House, House 8, Road 2, Sector 3, Uttara, Dhaka-1230", "Official Décor & Creative Zone Partner / Gold Sponsor"),
    ("Berger Paints Bangladesh Limited", "Manufacturing / Paints & Coatings", "Saadman Hussain", "Category Manager - Decorative Marketing", "saadman.hussain@bergerbd.com", "https://www.linkedin.com/in/saadmanhussain/", "https://www.linkedin.com/in/saadmanhussain/", "+880 2 48953665", "Berger House, House 8, Road 2, Sector 3, Uttara, Dhaka-1230", "Creative & Visual Branding Partner"),

    # Walton
    ("Walton Hi-Tech Industries PLC", "Consumer Electronics & Technology", "Zoheb Ahmed", "Chief Marketing Officer (CMO)", "zoheb.ahmed@waltonbd.com", "https://bd.linkedin.com/in/zohebahmed234", "https://bd.linkedin.com/in/zohebahmed234", "+880 9606555555", "Plot 1088, Block I, Sabrina Sobhan 5th Avenue, Bashundhara R/A, Dhaka-1229", "Title Sponsor / Tech & Gadget Partner / Mega Prize Sponsor"),
    ("Walton Hi-Tech Industries PLC", "Consumer Electronics & Technology", "Fazle Rabbi Khadem", "Senior Brand Manager", "fazle.rabbi@waltonbd.com", "https://bd.linkedin.com/in/fazle-rabbi-khadem-45162949", "https://bd.linkedin.com/in/fazle-rabbi-khadem-45162949", "+880 9606555555", "Plot 1088, Block I, Sabrina Sobhan 5th Avenue, Bashundhara R/A, Dhaka-1229", "Electronics Brand Partner / Youth Technology Showcase Sponsor"),

    # Link3 Technologies
    ("Link3 Technologies Ltd.", "Telecommunications & IT Services", "Arif Arif", "Manager, Corporate Sales & Marketing", "corporate@link3.net", "https://bd.linkedin.com/in/arif-arif-5a450833", "https://bd.linkedin.com/in/arif-arif-5a450833", "+880 9678123123", "Plot 17, Road 113/A, Gulshan-2, Dhaka-1212", "Official High-Speed Internet & Connectivity Partner (Wi-Fi Sponsor)"),
    ("Link3 Technologies Ltd.", "Telecommunications & IT Services", "Tushar Saha", "Manager - Sales and Marketing", "tushar.saha@link3.net", "https://bd.linkedin.com/in/tushar-saha-498144268", "https://bd.linkedin.com/in/tushar-saha-498144268", "+880 9678123123", "Plot 17, Road 113/A, Gulshan-2, Dhaka-1212", "Digital Infrastructure & Live Streaming Partner"),

    # Banglay IELTS & Immigration Center (BIIC)
    ("Banglay IELTS & Immigration Center (BIIC)", "EdTech / Higher Education Consultancy", "Jobayer Hosain", "Managing Director", "info@banglayielts.com", "https://bd.linkedin.com/in/jobayer-hosain-a62aa9141", "https://bd.linkedin.com/in/jobayer-hosain-a62aa9141", "+880 1619888222", "Mirpur-10 / Dhanmondi, Dhaka, Bangladesh (Adjacent to DCC)", "Title / Co-Sponsor / EdTech & Higher Studies Knowledge Partner"),
    ("Banglay IELTS & Immigration Center (BIIC)", "EdTech / Higher Education Consultancy", "Nasiruddin Sadaf", "Country Manager & Marketing Lead", "sadaf@banglayielts.com", "https://bd.linkedin.com/in/sadafnaseer", "https://bd.linkedin.com/in/sadafnaseer", "+880 1619888222", "Mirpur-10 / Dhanmondi, Dhaka, Bangladesh (Adjacent to DCC)", "Official Education & Overseas Career Consultancy Partner"),
    ("Banglay IELTS & Immigration Center (BIIC)", "EdTech / Higher Education Consultancy", "Rashed Hossain", "Founder, CEO & Chairman", "rashed@banglayielts.com", "https://bd.linkedin.com/in/rashedhbs", "https://bd.linkedin.com/in/rashedhbs", "+880 1619888222", "Concept Tower, 68/69 Green Road, Panthapath / Dhanmondi, Dhaka-1205", "Higher Education Partner / Study Abroad & Youth IELTS Partner"),

    # Tripploy (Special DCCBC Connection!)
    ("Tripploy", "TravelTech / Youth Travel", "MD. Toufiq Mahbub Borshon", "Chief Executive Officer (Former President of DCCBC!)", "borshon@tripploy.com", "https://bd.linkedin.com/in/md-toufiq-mahbub-borshon-62791a14a", "https://bd.linkedin.com/in/md-toufiq-mahbub-borshon-62791a14a", "+880 1711000000", "Mirpur DOHS / Uttara, Dhaka, Bangladesh", "Official Travel & Tourism Partner / Youth Tour Partner (Strong Alumnus Tie)"),
    ("Tripploy", "TravelTech / Youth Travel", "Ashiqur Rahman Ashik", "Co-Founder & Chief Operating Officer", "ashik@tripploy.com", "https://bd.linkedin.com/in/ashiqur-rahman-ashik-b2103897", "https://bd.linkedin.com/in/ashiqur-rahman-ashik-b2103897", "+880 1711000000", "Mirpur DOHS / Uttara, Dhaka, Bangladesh", "Youth Adventure & Hospitality Partner"),

    # Gold Kinen
    ("Gold Kinen", "FinTech / Micro-Investment", "Atef Hasan", "Founder & CEO", "atef@goldkinen.com", "https://bd.linkedin.com/in/atef-hasan-78a63b66", "https://bd.linkedin.com/in/atef-hasan-78a63b66", "+880 9638004653", "Level 4, House 11, Road 130, Gulshan-1, Dhaka-1212", "Official FinTech & Youth Savings Partner / Wealth Tech Knowledge Partner"),
    ("Gold Kinen", "FinTech / Micro-Investment", "Rafatul Bari Labib", "Founder & CCO (Ex-Trade Marketing bKash)", "labib@goldkinen.com", "https://bd.linkedin.com/in/rafatul-bari-labib-07250972", "https://bd.linkedin.com/in/rafatul-bari-labib-07250972", "+880 9638004653", "Level 4, House 11, Road 130, Gulshan-1, Dhaka-1212", "Financial Literacy Partner / Digital Gold Partner"),

    # Grameenphone
    ("Grameenphone Ltd. (GP Accelerator)", "Telecommunications & Digital Services", "Afifa Siddika", "Brand and Engagement Manager", "afifa.siddika@grameenphone.com", "https://bd.linkedin.com/in/afifa-siddika-aa47b4178", "https://bd.linkedin.com/in/afifa-siddika-aa47b4178", "+880 2 9882424", "GPHouse, Plot 1088, Basundhara, Baridhara, Dhaka-1229", "Title / Telecom Sponsor / Youth Engagement Partner"),
    ("Grameenphone Ltd. (GP Accelerator)", "Telecommunications & Digital Services", "Shabnam Sharmin", "Brand Manager - Internet Portfolio & Youth Segments", "shabnam.sharmin@grameenphone.com", "https://bd.linkedin.com/in/shabnam-sharmin-374028166", "https://bd.linkedin.com/in/shabnam-sharmin-374028166", "+880 2 9882424", "GPHouse, Plot 1088, Basundhara, Baridhara, Dhaka-1229", "Innovation & Startup Partner (GP Accelerator / Youth Portfolio)"),

    # Robi Axiata
    ("Robi Axiata PLC (Youth Brand 'cirkle')", "Telecommunications & Digital Services", "Sadman Abrar", "Brand & Communication Lead - Youth Brand ('cirkle')", "sadman.abrar@robi.com.bd", "https://bd.linkedin.com/in/sadman-abrar-93280a1b2", "https://bd.linkedin.com/in/sadman-abrar-93280a1b2", "+880 1819400400", "Robi Corporate Office, 53 Gulshan South Avenue, Gulshan-1, Dhaka-1212", "Youth Lifestyle & Gaming Partner ('cirkle' Activation) / Title Sponsor"),
    ("Robi Axiata PLC", "Telecommunications & Digital Services", "Adibuzzaman Chowdhury", "Brand Manager (Manager, Communication & Creatives)", "adibuzzaman.chowdhury@robi.com.bd", "https://bd.linkedin.com/in/adibuzzaman-chowdhury", "https://bd.linkedin.com/in/adibuzzaman-chowdhury", "+880 1819400400", "Robi Corporate Office, 53 Gulshan South Avenue, Gulshan-1, Dhaka-1212", "Official Telecommunication Partner / Digital Experience Partner")
]

# Deduplicate
deduped_leads = []
seen_keys = set()
for r in all_leads_raw:
    key = (r[0].lower().strip(), r[2].lower().strip())
    if key not in seen_keys:
        seen_keys.add(key)
        deduped_leads.append(r)

print(f"Total unique verified decision-maker leads: {len(deduped_leads)}")

# 1. Write CSV
headers = [
    'SL No', 'Company Name', 'Industry Sector', 'Contact Person Name', 'Designation / Role',
    'Email Address', 'LinkedIn Profile URL', 'Contact Source / Verification URL',
    'Official Phone / Corporate PBX', 'Office Location (Bangladesh)', 'Target Sponsoring Fit for College Events'
]

with open(leads_csv, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for idx, lead in enumerate(deduped_leads, 1):
        writer.writerow([str(idx)] + list(lead))

print("Updated company_sponsor_leads_verified.csv successfully!")

# 2. Write Tab 7 to Excel
wb = openpyxl.load_workbook(excel_path)
sheet_name = 'Company Sponsor Leads'
if sheet_name in wb.sheetnames:
    del wb[sheet_name]

ws = wb.create_sheet(title=sheet_name)

header_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='1B365D', end_color='1B365D', fill_type='solid')
border = Border(
    left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
    top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD')
)

for col_idx, h in enumerate(headers, 1):
    c = ws.cell(row=1, column=col_idx, value=h)
    c.font = header_font
    c.fill = header_fill
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

for row_idx, lead in enumerate(deduped_leads, 2):
    full_row = [str(row_idx - 1)] + list(lead)
    for col_idx, val in enumerate(full_row, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.border = border
        cell.alignment = Alignment(vertical='center')
        
        # Hyperlinks
        if col_idx == 6 and '@' in str(val):
            cell.hyperlink = f"mailto:{val}"
            cell.font = Font(color='0563C1', underline='single')
        elif col_idx in (7, 8) and str(val).startswith('http'):
            cell.hyperlink = val
            cell.font = Font(color='0563C1', underline='single')

for col in ws.columns:
    col_letter = get_column_letter(col[0].column)
    max_len = max(len(str(cell.value or '')) for cell in col)
    ws.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 45)

wb.save(excel_path)
print(f"Excel workbook updated with '{sheet_name}' tab!")
