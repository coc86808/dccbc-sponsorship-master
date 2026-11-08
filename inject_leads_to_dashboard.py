import csv
import json
import os

WORKSPACE = r'e:\DCCBC'
index_path = os.path.join(WORKSPACE, 'index.html')
leads_csv = os.path.join(WORKSPACE, 'company_sponsor_leads_verified.csv')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

leads = []
with open(leads_csv, 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        leads.append(r)

print(f"Loaded {len(leads)} leads.")

# 1. Update Metrics Hero numbers
html = html.replace('<p class="text-2xl sm:text-3xl font-extrabold text-[#1B365D] mt-1">228</p>', '<p class="text-2xl sm:text-3xl font-extrabold text-[#1B365D] mt-1">385</p>')
html = html.replace('<p class="text-2xl sm:text-3xl font-extrabold text-blue-600 mt-1">80</p>', '<p class="text-2xl sm:text-3xl font-extrabold text-blue-600 mt-1">91</p>')
html = html.replace('<p class="text-2xl sm:text-3xl font-extrabold text-purple-600 mt-1">700+</p>', '<p class="text-2xl sm:text-3xl font-extrabold text-purple-600 mt-1">814</p>')

# Update badges in tabs
html = html.replace('<span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded-full font-bold">228</span>', '<span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded-full font-bold">385</span>')
html = html.replace('<span class="bg-slate-200 text-slate-700 text-xs px-2 py-0.5 rounded-full font-bold">80</span>', '<span class="bg-slate-200 text-slate-700 text-xs px-2 py-0.5 rounded-full font-bold">91</span>')

# 2. Add Tab Button
target_tab_btn = '''          <button id="tab-orgs-btn" onclick="switchTab('orgs')" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent">
            <i class="fa-solid fa-users-rectangle"></i> Organisation List & Individual Events
            <span class="bg-slate-200 text-slate-700 text-xs px-2 py-0.5 rounded-full font-bold">91</span>
          </button>'''

replacement_tab_btn = target_tab_btn + '''
          <button id="tab-leads-btn" onclick="switchTab('leads')" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent">
            <i class="fa-solid fa-id-card-clip text-emerald-600"></i> Sponsor Decision Makers
            <span class="bg-emerald-100 text-emerald-700 text-xs px-2 py-0.5 rounded-full font-bold">''' + str(len(leads)) + ''' Leads</span>
          </button>'''

if target_tab_btn in html and 'tab-leads-btn' not in html:
    html = html.replace(target_tab_btn, replacement_tab_btn)
    print("Added tab-leads-btn.")

# 3. Add leadsTableView
leads_table_html = '''
      <!-- Table 3: Sponsor Decision Makers & Leads -->
      <div id="leadsTableView" class="hidden overflow-x-auto">
        <div class="p-3 bg-emerald-50 border-b border-emerald-100 flex items-center justify-between text-xs text-emerald-900 font-medium">
          <span class="flex items-center gap-1.5"><i class="fa-solid fa-circle-check text-emerald-600"></i> Direct marketing, brand managers & sponsorship decision-makers across Bangladesh</span>
          <a href="./company_sponsor_leads_verified.csv" download class="inline-flex items-center gap-1 px-2.5 py-1 bg-white border border-emerald-300 rounded-lg text-emerald-800 hover:bg-emerald-100 shadow-2xs font-semibold">
            <i class="fa-solid fa-file-csv text-emerald-600"></i> Download Leads CSV
          </a>
        </div>
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-100/75 border-b border-slate-200 text-xs font-bold text-slate-600 uppercase tracking-wider">
              <th class="py-3 px-4 w-12 text-center">#</th>
              <th class="py-3 px-4">Company Name</th>
              <th class="py-3 px-4">Decision Maker Name</th>
              <th class="py-3 px-4">Designation / Role</th>
              <th class="py-3 px-4">Corporate Email</th>
              <th class="py-3 px-4 text-center">LinkedIn Profile</th>
              <th class="py-3 px-4">Office Location</th>
              <th class="py-3 px-4">College Sponsoring Fit</th>
            </tr>
          </thead>
          <tbody id="leadsTableBody" class="divide-y divide-slate-200 text-xs text-slate-700">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>
'''

if 'id="leadsTableView"' not in html:
    # insert after orgsTableView closing div
    idx = html.find('<!-- Modal -->')
    if idx == -1:
        idx = html.find('id="eventModal"')
    if idx != -1:
        # find preceding </div>
        div_idx = html.rfind('</div>', 0, idx)
        html = html[:div_idx+6] + leads_table_html + html[div_idx+6:]
        print("Inserted leadsTableView.")

# 4. Inject JS data and render logic
js_injection = f'''
    const leadsData = {json.dumps(leads, ensure_ascii=False)};

    function renderLeadsTable(data = leadsData) {{
      const tbody = document.getElementById('leadsTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      if (data.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="8" class="text-center py-8 text-slate-400">No leads found matching query.</td></tr>';
        return;
      }}

      data.forEach((l, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition';

        const emailHtml = l['Email Address'] ? 
          `<a href="mailto:${{l['Email Address']}}" class="inline-flex items-center gap-1.5 font-mono text-xs font-semibold text-emerald-700 hover:underline bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
            <i class="fa-solid fa-envelope text-[10px]"></i> ${{l['Email Address']}}
          </a>` : '<span class="text-slate-400">N/A</span>';

        const linkedinHtml = l['LinkedIn Profile URL'] && l['LinkedIn Profile URL'].startsWith('http') ? 
          `<a href="${{l['LinkedIn Profile URL']}}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-bold text-white bg-[#0A66C2] hover:bg-[#004182] rounded-lg transition shadow-2xs">
            <i class="fa-brands fa-linkedin"></i> Profile
          </a>` : '<span class="text-slate-400">N/A</span>';

        tr.innerHTML = `
          <td class="py-3 px-4 text-center font-mono text-slate-400">${{idx + 1}}</td>
          <td class="py-3 px-4 font-bold text-slate-900">${{l['Company Name']}}</td>
          <td class="py-3 px-4 font-semibold text-slate-800">${{l['Contact Person Name']}}</td>
          <td class="py-3 px-4 text-xs font-medium text-slate-600">${{l['Designation / Role']}}</td>
          <td class="py-3 px-4">${{emailHtml}}</td>
          <td class="py-3 px-4 text-center">${{linkedinHtml}}</td>
          <td class="py-3 px-4 text-xs text-slate-600">${{l['Office Location (Bangladesh)']}}</td>
          <td class="py-3 px-4 text-xs font-medium text-blue-700 bg-blue-50/50 rounded">${{l['Target Sponsoring Fit for College Events']}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}
'''

# Replace switchTab
old_switch_target = '''function switchTab(tab) {
      currentTab = tab;
      const spBtn = document.getElementById('tab-sponsors-btn');
      const orgBtn = document.getElementById('tab-orgs-btn');
      const spView = document.getElementById('sponsorsTableView');
      const orgView = document.getElementById('orgsTableView');'''

new_switch_replacement = '''function switchTab(tab) {
      currentTab = tab;
      const spBtn = document.getElementById('tab-sponsors-btn');
      const orgBtn = document.getElementById('tab-orgs-btn');
      const leadsBtn = document.getElementById('tab-leads-btn');
      const spView = document.getElementById('sponsorsTableView');
      const orgView = document.getElementById('orgsTableView');
      const leadsView = document.getElementById('leadsTableView');

      // Reset
      spBtn.className = "pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent";
      orgBtn.className = "pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent";
      if (leadsBtn) leadsBtn.className = "pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent";
      spView.classList.add('hidden');
      orgView.classList.add('hidden');
      if (leadsView) leadsView.classList.add('hidden');

      if (tab === 'sponsors') {
        spBtn.className = "pb-3 text-sm font-bold text-blue-600 border-b-2 border-blue-600 flex items-center gap-2";
        spView.classList.remove('hidden');
      } else if (tab === 'orgs') {
        orgBtn.className = "pb-3 text-sm font-bold text-blue-600 border-b-2 border-blue-600 flex items-center gap-2";
        orgView.classList.remove('hidden');
      } else if (tab === 'leads') {
        if (leadsBtn) leadsBtn.className = "pb-3 text-sm font-bold text-emerald-600 border-b-2 border-emerald-600 flex items-center gap-2";
        if (leadsView) leadsView.classList.remove('hidden');
        renderLeadsTable();
      }'''

if old_switch_target in html:
    html = html.replace(old_switch_target, new_switch_replacement)
    print("Replaced switchTab.")

if 'const leadsData = ' not in html:
    html = html.replace('const sponsorsData = ', js_injection + '\n    const sponsorsData = ')
    print("Injected leadsData JS.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully injected leads into index.html!")
