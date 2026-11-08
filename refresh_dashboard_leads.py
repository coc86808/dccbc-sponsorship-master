import json
import csv
import re
import os

WORKSPACE = r'e:\DCCBC'
index_path = os.path.join(WORKSPACE, 'index.html')
leads_csv = os.path.join(WORKSPACE, 'company_sponsor_leads_verified.csv')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

leads = []
with open(leads_csv, 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        # Clean phone for UI display
        r['Official Phone / Corporate PBX'] = r['Official Phone / Corporate PBX'].lstrip("'")
        leads.append(r)

print(f"Loaded {len(leads)} leads from CSV.")

# 1. Update button text/badge
html = re.sub(
    r'<button id="tab-leads-btn"[^>]*>[\s\S]*?</button>',
    f'''<button id="tab-leads-btn" onclick="switchTab('leads')" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent">
            <i class="fa-solid fa-id-card-clip text-emerald-600"></i> Sponsor Decision Makers
            <span class="bg-emerald-100 text-emerald-700 text-xs px-2 py-0.5 rounded-full font-bold">{len(leads)} Leads</span>
          </button>''',
    html
)

# 2. Update leadsData variable in JS
leads_json = json.dumps(leads, ensure_ascii=False)
html = re.sub(
    r'const leadsData = \[[\s\S]*?\];',
    f'const leadsData = {leads_json};',
    html
)

# 3. Ensure renderLeadsTable displays phone number
old_render = '''tr.innerHTML = `
          <td class="py-3 px-4 text-center font-mono text-slate-400">${idx + 1}</td>
          <td class="py-3 px-4 font-bold text-slate-900">${l['Company Name']}</td>
          <td class="py-3 px-4 font-semibold text-slate-800">${l['Contact Person Name']}</td>
          <td class="py-3 px-4 text-xs font-medium text-slate-600">${l['Designation / Role']}</td>
          <td class="py-3 px-4">${emailHtml}</td>
          <td class="py-3 px-4 text-center">${linkedinHtml}</td>
          <td class="py-3 px-4 text-xs text-slate-600">${l['Office Location (Bangladesh)']}</td>
          <td class="py-3 px-4 text-xs font-medium text-blue-700 bg-blue-50/50 rounded">${l['Target Sponsoring Fit for College Events']}</td>
        `;'''

new_render = '''const phoneHtml = l['Official Phone / Corporate PBX'] ? 
          `<span class="inline-flex items-center gap-1 font-mono text-[11px] text-slate-600 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
            <i class="fa-solid fa-phone text-[9px] text-slate-400"></i> ${l['Official Phone / Corporate PBX']}
          </span>` : '<span class="text-slate-400 text-xs">N/A</span>';

        tr.innerHTML = `
          <td class="py-3 px-4 text-center font-mono text-slate-400">${idx + 1}</td>
          <td class="py-3 px-4">
            <div class="font-bold text-slate-900">${l['Company Name']}</div>
            <div class="text-[11px] text-slate-500">${l['Industry Sector']}</div>
          </td>
          <td class="py-3 px-4">
            <div class="font-semibold text-slate-800">${l['Contact Person Name']}</div>
            <div class="text-xs text-slate-500">${l['Designation / Role']}</div>
          </td>
          <td class="py-3 px-4">${emailHtml}</td>
          <td class="py-3 px-4">${phoneHtml}</td>
          <td class="py-3 px-4 text-center">${linkedinHtml}</td>
          <td class="py-3 px-4 text-xs text-slate-600">${l['Office Location (Bangladesh)']}</td>
          <td class="py-3 px-4 text-xs font-medium text-blue-700 bg-blue-50/50 rounded">${l['Target Sponsoring Fit for College Events']}</td>
        `;'''

if old_render in html:
    html = html.replace(old_render, new_render)
    print("Updated render function with phone column!")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Refreshed index.html successfully!")
