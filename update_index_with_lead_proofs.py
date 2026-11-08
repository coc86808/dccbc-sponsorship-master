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
        r['Official Phone / Corporate PBX'] = r['Official Phone / Corporate PBX'].lstrip("'")
        leads.append(r)

print(f"Loaded {len(leads)} leads from CSV.")

# 1. Update button text/badge
html = re.sub(
    r'<button id="tab-leads-btn"[^>]*>[\s\S]*?</button>',
    f'''<button id="tab-leads-btn" onclick="switchTab('leads')" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent">
            <i class="fa-solid fa-id-card-clip text-emerald-600"></i> Sponsor Decision Makers
            <span class="bg-emerald-100 text-emerald-700 text-xs px-2 py-0.5 rounded-full font-bold">{len(leads)} Verified Leads</span>
          </button>''',
    html
)

# 2. Update leadsData in JS
leads_json = json.dumps(leads, ensure_ascii=False)
html = re.sub(
    r'const leadsData = \[[\s\S]*?\];',
    f'const leadsData = {leads_json};',
    html
)

# 3. Update the thead of leads table to include Verification & Proof columns
old_thead = '''<thead>
          <tr class="bg-slate-50 text-slate-700 text-xs uppercase tracking-wider border-b border-slate-200">
            <th class="py-3 px-4 text-center">#</th>
            <th class="py-3 px-4 text-left">Company</th>
            <th class="py-3 px-4 text-left">Decision Maker</th>
            <th class="py-3 px-4 text-left">Email Address</th>
            <th class="py-3 px-4 text-left">Phone / PBX</th>
            <th class="py-3 px-4 text-center">LinkedIn</th>
            <th class="py-3 px-4 text-left">Office Location</th>
            <th class="py-3 px-4 text-left">Sponsoring Fit</th>
          </tr>
        </thead>'''

new_thead = '''<thead>
          <tr class="bg-slate-50 text-slate-700 text-xs uppercase tracking-wider border-b border-slate-200">
            <th class="py-3 px-4 text-center">#</th>
            <th class="py-3 px-4 text-left">Company & Sector</th>
            <th class="py-3 px-4 text-left">Decision Maker & Role</th>
            <th class="py-3 px-4 text-left">Verified Email</th>
            <th class="py-3 px-4 text-left">Official Phone / PBX</th>
            <th class="py-3 px-4 text-left">Verification Method</th>
            <th class="py-3 px-4 text-center">Screenshot Proof</th>
            <th class="py-3 px-4 text-center">LinkedIn</th>
            <th class="py-3 px-4 text-left">Sponsoring Fit</th>
          </tr>
        </thead>'''

if old_thead in html:
    html = html.replace(old_thead, new_thead)
    print("Replaced thead with new 9-column headers!")

# 4. Update renderLeadsTable logic
render_func_pattern = r'function renderLeadsTable\(data\)\s*\{[\s\S]*?\n    \}'
new_render_func = '''function renderLeadsTable(data) {
      const tbody = document.getElementById('leads-table-body');
      tbody.innerHTML = '';
      if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="py-8 text-center text-slate-400">No decision makers match your filter.</td></tr>';
        return;
      }
      data.forEach((l, idx) => {
        const tr = document.createElement('tr');
        tr.className = 'border-b border-slate-100 hover:bg-slate-50/80 transition-colors text-sm';
        
        const emailHtml = l['Email Address'] ? 
          `<a href="mailto:${l['Email Address']}" class="inline-flex items-center gap-1.5 font-mono text-xs text-blue-600 hover:text-blue-800 bg-blue-50/60 hover:bg-blue-100/80 px-2.5 py-1 rounded border border-blue-200/60 transition-colors">
            <i class="fa-solid fa-envelope text-[11px]"></i> ${l['Email Address']}
          </a>` : '<span class="text-slate-400 text-xs italic">Pending</span>';

        const phoneHtml = l['Official Phone / Corporate PBX'] ? 
          `<span class="inline-flex items-center gap-1 font-mono text-xs text-slate-700 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
            <i class="fa-solid fa-phone text-[10px] text-slate-400"></i> ${l['Official Phone / Corporate PBX']}
          </span>` : '<span class="text-slate-400 text-xs">N/A</span>';

        const linkedinHtml = l['LinkedIn Profile URL'] && l['LinkedIn Profile URL'].startsWith('http') ? 
          `<a href="${l['LinkedIn Profile URL']}" target="_blank" class="inline-flex items-center justify-center w-7 h-7 rounded bg-[#0A66C2]/10 text-[#0A66C2] hover:bg-[#0A66C2] hover:text-white transition-all text-xs" title="View LinkedIn Profile">
            <i class="fa-brands fa-linkedin-in"></i>
          </a>` : '<span class="text-slate-300">-</span>';

        const method = l['Extraction Method / Verification Type (উৎস ও যাচাই পদ্ধতি)'] || 'Direct Public Page Display';
        let methodBadge = '';
        if (method.includes('Display') || method.includes('প্রদর্শিত')) {
          methodBadge = `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200"><i class="fa-solid fa-circle-check text-[10px]"></i> Public Display</span>`;
        } else if (method.includes('Desk') || method.includes('ডেস্ক')) {
          methodBadge = `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-blue-100 text-blue-800 border border-blue-200"><i class="fa-solid fa-building text-[10px]"></i> Corporate Desk</span>`;
        } else {
          methodBadge = `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-100 text-amber-800 border border-amber-200" title="Retrieved via corporate domain schema code - not displayed on page"><i class="fa-solid fa-code text-[10px]"></i> Domain Schema</span>`;
        }

        const proofUrl = l['Screenshot Proof Link (স্ক্রিনশট প্রুফ লিঙ্ক)'];
        const proofHtml = proofUrl && proofUrl.startsWith('http') ?
          `<a href="${proofUrl}" target="_blank" class="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200 text-xs font-semibold transition-colors" title="View proof screenshot with visible phone and email">
            <i class="fa-solid fa-camera"></i> Proof
          </a>` : '<span class="text-slate-300 text-xs">-</span>';

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
          <td class="py-3 px-4">${methodBadge}</td>
          <td class="py-3 px-4 text-center">${proofHtml}</td>
          <td class="py-3 px-4 text-center">${linkedinHtml}</td>
          <td class="py-3 px-4 text-xs font-medium text-blue-700 bg-blue-50/50 rounded">${l['Target Sponsoring Fit for College Events']}</td>
        `;
        tbody.appendChild(tr);
      });
    }'''

html = re.sub(render_func_pattern, new_render_func, html)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with Verification Method and Proof Screenshot columns successfully!")
