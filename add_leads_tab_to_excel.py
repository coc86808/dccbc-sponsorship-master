import csv
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

WORKSPACE = r'e:\DCCBC'
excel_path = os.path.join(WORKSPACE, 'Bangladesh_Business_Clubs_Sponsorship_Master.xlsx')
leads_csv = os.path.join(WORKSPACE, 'company_sponsor_leads_verified.csv')

wb = openpyxl.load_workbook(excel_path)

sheet_name = 'Company Sponsor Leads'
if sheet_name in wb.sheetnames:
    del wb[sheet_name]

ws = wb.create_sheet(title=sheet_name)

header_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='1B365D', end_color='1B365D', fill_type='solid')
border = Border(
    left=Side(style='thin', color='DDDDDD'),
    right=Side(style='thin', color='DDDDDD'),
    top=Side(style='thin', color='DDDDDD'),
    bottom=Side(style='thin', color='DDDDDD')
)

with open(leads_csv, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Write headers
for col_idx, header in enumerate(rows[0], 1):
    cell = ws.cell(row=1, column=col_idx, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Write rows
for row_idx, row in enumerate(rows[1:], 2):
    for col_idx, val in enumerate(row, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.border = border
        cell.alignment = Alignment(vertical='center')
        
        # Hyperlink email
        if col_idx == 6 and '@' in str(val):
            cell.hyperlink = f"mailto:{val}"
            cell.font = Font(color='0563C1', underline='single')
        # Hyperlink LinkedIn
        elif col_idx == 7 and str(val).startswith('http'):
            cell.hyperlink = val
            cell.font = Font(color='0563C1', underline='single')
        # Hyperlink Source URL
        elif col_idx == 8 and str(val).startswith('http'):
            cell.hyperlink = val
            cell.font = Font(color='0563C1', underline='single')

# Set column widths
for col in ws.columns:
    col_letter = get_column_letter(col[0].column)
    max_len = max(len(str(cell.value or '')) for cell in col)
    ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 40)

wb.save(excel_path)
print(f"Successfully added '{sheet_name}' with {len(rows)-1} leads to {excel_path}!")
