import json
import csv
import re
import os

WORKSPACE = r'e:\DCCBC'
index_path = os.path.join(WORKSPACE, 'index.html')
leads_csv = os.path.join(WORKSPACE, 'company_sponsor_leads_verified.csv')

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Read leads
leads = []
with open(leads_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        leads.append(r)

print(f"Loaded {len(leads)} leads from CSV.")

# 1. Add tab button
old_nav_buttons = '''<button id="tab-orgs-btn" onclick="switchTab('orgs')" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent">
                        <i class="fas fa-sitemap"></i> Organisation List <span id="org-count-badge" class="px-2 py-0.5 text-xs bg-slate-100 text-slate-600 rounded-full font-bold">91</span>
                    </button>'''

new_nav_buttons = '''<button id="tab-orgs-btn" onclick="switchTab('orgs')" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent">
                        <i class="fas fa-sitemap"></i> Organisation List <span id="org-count-badge" class="px-2 py-0.5 text-xs bg-slate-100 text-slate-600 rounded-full font-bold">91</span>
                    </button>
                    <button id="tab-leads-btn" onclick="switchTab('leads')" class="pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent">
                        <i class="fas fa-user-tie text-emerald-600"></i> Sponsor Decision Makers <span class="px-2 py-0.5 text-xs bg-emerald-100 text-emerald-700 rounded-full font-bold">''' + str(len(leads)) + '''</span>
                    </button>'''

if old_nav_buttons in html:
    html = html.replace(old_nav_buttons, new_nav_buttons)
    print("Added leads nav tab button.")

# 2. Add leads section content
old_view_end = '<!-- VIEW 2: ORGANISATIONS -->'
# We can find where organisations view ends
# Look for </section> after view-orgs
orgs_section_match = re.search(r'(<div id="view-orgs".*?</div>\s*<!-- END ORGS -->|id="view-orgs"[^>]*>[\s\S]*?</div>\s*</div>)', html)

leads_view_html = '''
            <!-- VIEW 3: SPONSOR DECISION MAKERS & LEADS -->
            <div id="view-leads" class="hidden">
                <div class="mb-4 bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-lg shadow-sm">
                            <i class="fas fa-id-card"></i>
                        </div>
                        <div>
                            <h2 class="text-base font-bold text-slate-900">Verified Corporate Sponsor Decision-Makers</h2>
                            <p class="text-xs text-slate-600">Direct Brand Managers, CMOs & Corporate Communications Heads with LinkedIn profiles & official emails.</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-white border border-emerald-300 rounded-lg text-emerald-800 shadow-xs">
                            <i class="fab fa-linkedin text-blue-600 mr-1"></i> LinkedIn Verified
                        </span>
                        <span class="text-xs font-semibold px-2.5 py-1 bg-white border border-emerald-300 rounded-lg text-emerald-800 shadow-xs">
                            <i class="fas fa-envelope text-red-500 mr-1"></i> Corporate Mailto Active
                        </span>
                    </div>
                </div>

                <!-- Leads Table Card -->
                <div class="bg-white rounded-2xl shadow-xs border border-slate-200 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-50/80 border-b border-slate-200 text-slate-700 text-xs uppercase tracking-wider font-bold">
                                    <th class="py-3.5 px-4 w-12 text-center">SL</th>
                                    <th class="py-3.5 px-4">Company Name</th>
                                    <th class="py-3.5 px-4">Decision Maker / Contact</th>
                                    <th class="py-3.5 px-4">Designation & Role</th>
                                    <th class="py-3.5 px-4">Verified Corporate Email</th>
                                    <th class="py-3.5 px-4 text-center">LinkedIn Profile</th>
                                    <th class="py-3.5 px-4">Office Location</th>
                                    <th class="py-3.5 px-4">Target Sponsoring Fit</th>
                                </tr>
                            </thead>
                            <tbody id="leads-tbody" class="divide-y divide-slate-100 text-sm">
                                <!-- Populated dynamically by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
'''

# Insert view-leads before closing main wrapper
if '<div id="view-leads"' not in html:
    html = html.replace('</div>\n    </div>\n\n    <!-- MODAL FOR DETAILED INDIVIDUAL EVENT LIST -->', leads_view_html + '\n</div>\n    </div>\n\n    <!-- MODAL FOR DETAILED INDIVIDUAL EVENT LIST -->')
    print("Added view-leads HTML section.")

# 3. Add JS leadsData and rendering logic
js_leads_var = f"\n        const leadsData = {json.dumps(leads, ensure_ascii=False)};\n"

# Update switchTab logic to handle 'leads'
old_switch_tab = '''function switchTab(tab) {
            currentTab = tab;
            const spBtn = document.getElementById('tab-sponsors-btn');
            const orgBtn = document.getElementById('tab-orgs-btn');
            const spView = document.getElementById('view-sponsors');
            const orgView = document.getElementById('view-orgs');

            if (tab === 'sponsors') {
                spBtn.className = "pb-3 text-sm font-bold text-blue-600 border-b-2 border-blue-600 flex items-center gap-2";
                orgBtn.className = "pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent";
                spView.classList.remove('hidden');
                orgView.classList.add('hidden');
            } else {
                orgBtn.className = "pb-3 text-sm font-bold text-blue-600 border-b-2 border-blue-600 flex items-center gap-2";
                spBtn.className = "pb-3 text-sm font-semibold text-slate-500 hover:text-slate-700 flex items-center gap-2 border-b-2 border-transparent";
                orgView.classList.remove('hidden');
                spView.classList.add('hidden');
                renderOrgsTable();
            }
        }'''

new_switch_tab = '''function switchTab(tab) {
            currentTab = tab;
            const spBtn = document.getElementById('tab-sponsors-btn');
            const orgBtn = document.getElementById('tab-orgs-btn');
            const leadsBtn = document.getElementById('tab-leads-btn');
            const spView = document.getElementById('view-sponsors');
            const orgView = document.getElementById('view-orgs');
            const leadsView = document.getElementById('view-leads');

            // Reset all
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
                renderOrgsTable();
            } else if (tab === 'leads') {
                if (leadsBtn) leadsBtn.className = "pb-3 text-sm font-bold text-emerald-600 border-b-2 border-emerald-600 flex items-center gap-2";
                if (leadsView) leadsView.classList.remove('hidden');
                renderLeadsTable();
            }
        }

        function renderLeadsTable() {
            const tbody = document.getElementById('leads-tbody');
            if (!tbody) return;
            tbody.innerHTML = '';
            
            leadsData.forEach((lead, idx) => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50/70 transition-colors";
                
                const emailHtml = lead['Email Address'] ? 
                    `<a href="mailto:${lead['Email Address']}" class="inline-flex items-center gap-1.5 font-mono text-xs font-semibold text-emerald-700 hover:underline bg-emerald-50 px-2 py-1 rounded border border-emerald-200">
                        <i class="fas fa-envelope text-[10px]"></i> ${lead['Email Address']}
                    </a>` : '<span class="text-slate-400 text-xs">N/A</span>';
                
                const linkedinHtml = lead['LinkedIn Profile URL'] && lead['LinkedIn Profile URL'].startsWith('http') ?
                    `<a href="${lead['LinkedIn Profile URL']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-bold text-white bg-[#0A66C2] hover:bg-[#004182] rounded-lg transition shadow-2xs">
                        <i class="fab fa-linkedin"></i> Profile
                    </a>` : '<span class="text-slate-400 text-xs">N/A</span>';

                tr.innerHTML = `
                    <td class="py-3 px-4 text-center font-mono text-xs text-slate-400">${idx + 1}</td>
                    <td class="py-3 px-4 font-bold text-slate-900">${lead['Company Name']}</td>
                    <td class="py-3 px-4 font-semibold text-slate-800">${lead['Contact Person Name']}</td>
                    <td class="py-3 px-4 text-xs font-medium text-slate-600">${lead['Designation / Role']}</td>
                    <td class="py-3 px-4">${emailHtml}</td>
                    <td class="py-3 px-4 text-center">${linkedinHtml}</td>
                    <td class="py-3 px-4 text-xs text-slate-600">${lead['Office Location (Bangladesh)']}</td>
                    <td class="py-3 px-4 text-xs font-medium text-blue-700 bg-blue-50/50 rounded">${lead['Target Sponsoring Fit for College Events']}</td>
                `;
                tbody.appendChild(tr);
            });
        }
'''

if old_switch_tab in html:
    html = html.replace(old_switch_tab, new_switch_tab)
    print("Updated switchTab script with renderLeadsTable.")

# Inject leadsData into JS
if 'const leadsData = ' not in html:
    html = html.replace('const orgsData = ', js_leads_var + '        const orgsData = ')
    print("Injected leadsData into script.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html fully updated with Sponsor Decision Makers & Leads tab!")
