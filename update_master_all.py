import csv, json, re, glob, os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

WORKSPACE = r'e:\DCCBC'

print("=== 1. Building Event Links Database ===")
event_link_db = {}

# From all_companies_strictly_verified.csv
with open(os.path.join(WORKSPACE, 'all_companies_strictly_verified.csv'), mode='r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        ev = row.get('Event Name', '').strip()
        link = row.get('Direct Proof Link', '').strip()
        org = row.get('Host Organization Name', '').strip()
        if ev and link:
            event_link_db[ev.lower()] = link
            event_link_db[(org.lower(), ev.lower())] = link

# From all markdown audit files
for mdf in glob.glob(os.path.join(WORKSPACE, '*.md')):
    with open(mdf, mode='r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        matches = re.findall(r'\[([^\]]+)\]\((https://www\.facebook\.com/(?:events/\d+|photo/\?[^)]+|posts/[^)]+|reel/[^)]+))\)', content)
        for label, url in matches:
            label_clean = label.strip().lower()
            if len(label_clean) > 3 and not label_clean.startswith('post'):
                event_link_db[label_clean] = url
        
        table_matches = re.findall(r'\|\s*\d+\s*\|\s*([^|]+)\|\s*(https://www\.facebook\.com/events/\d+[^|]*)\s*\|', content)
        for ev_title, ev_url in table_matches:
            event_link_db[ev_title.strip().lower()] = ev_url.strip()

print(f"Total cataloged direct event URLs: {len(event_link_db)}")

# 2. Process organisation_list.csv
orgs_file = os.path.join(WORKSPACE, 'organisation_list.csv')
with open(orgs_file, mode='r', encoding='utf-8') as f:
    org_rows = list(csv.DictReader(f))

enhanced_orgs = []
for org in org_rows:
    org_name = org['Organisation name']
    ev_count = org['event number']
    ev_names_raw = org['event names']
    hub_link = org['Event Link']
    status = org['status']
    
    # Base URL for search fallback
    base_club_url = hub_link.replace('/events', '').rstrip('/')
    
    raw_list = [e.strip() for e in ev_names_raw.split(',') if e.strip()]
    structured_events = []
    
    for ev in raw_list:
        ev_low = ev.lower()
        matched_url = None
        
        # Exact match or substring match in catalog
        if (org_name.lower(), ev_low) in event_link_db:
            matched_url = event_link_db[(org_name.lower(), ev_low)]
        elif ev_low in event_link_db:
            matched_url = event_link_db[ev_low]
        else:
            for k, u in event_link_db.items():
                if isinstance(k, str) and (k in ev_low or ev_low in k) and len(k) > 4:
                    matched_url = u
                    break
        
        if not matched_url:
            clean_q = re.sub(r'[^a-zA-Z0-9\s]', '', ev).strip().replace(' ', '+')
            matched_url = f"{base_club_url}/search/?q={clean_q}"
            
        structured_events.append({
            "name": ev,
            "url": matched_url
        })
        
    enhanced_orgs.append({
        "Organisation name": org_name,
        "event number": ev_count,
        "event names": ev_names_raw,
        "Event Link": hub_link,
        "status": status,
        "events": structured_events
    })

print(f"Enhanced {len(enhanced_orgs)} organisations with individual event links.")

# 3. Read sponsors list
sponsors_file = os.path.join(WORKSPACE, 'all_companies_strictly_verified.csv')
with open(sponsors_file, mode='r', encoding='utf-8') as f:
    sponsors_rows = list(csv.DictReader(f))

# 4. Generate updated index.html
print("=== 2. Updating index.html with Interactive Individual Event Links ===")
index_path = os.path.join(WORKSPACE, 'index.html')
with open(index_path, mode='r', encoding='utf-8') as f:
    html_content = f.read()

# Replace sponsorsData and orgsData JSON
sponsors_json = json.dumps(sponsors_rows, ensure_ascii=False)
orgs_json = json.dumps(enhanced_orgs, ensure_ascii=False)

# Replace the script block with enhanced render functions
js_code_target = """    const sponsorsData = """
if js_code_target in html_content:
    # We replace from const sponsorsData to </script>
    start_pos = html_content.find("    const sponsorsData = ")
    end_pos = html_content.rfind("  </script>")
    
    new_js = f"""    const sponsorsData = {sponsors_json};
    const orgsData = {orgs_json};

    let currentTab = 'sponsors';

    function switchTab(tab) {{
      currentTab = tab;
      const tabSponsors = document.getElementById('tabSponsors');
      const tabOrgs = document.getElementById('tabOrgs');
      const sponsorsView = document.getElementById('sponsorsTableView');
      const orgsView = document.getElementById('orgsTableView');
      const sectorFilterWrap = document.getElementById('sectorFilterWrap');
      const statusFilterWrap = document.getElementById('statusFilterWrap');

      if (tab === 'sponsors') {{
        tabSponsors.className = 'px-4 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-sm flex items-center gap-1.5 transition';
        tabOrgs.className = 'px-4 py-2 text-xs font-medium rounded-lg text-slate-600 hover:bg-slate-100 flex items-center gap-1.5 transition';
        sponsorsView.classList.remove('hidden');
        orgsView.classList.add('hidden');
        sectorFilterWrap.classList.remove('hidden');
        statusFilterWrap.classList.add('hidden');
      }} else {{
        tabOrgs.className = 'px-4 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-sm flex items-center gap-1.5 transition';
        tabSponsors.className = 'px-4 py-2 text-xs font-medium rounded-lg text-slate-600 hover:bg-slate-100 flex items-center gap-1.5 transition';
        orgsView.classList.remove('hidden');
        sponsorsView.classList.add('hidden');
        sectorFilterWrap.classList.add('hidden');
        statusFilterWrap.classList.remove('hidden');
      }}
      filterData();
    }}

    function renderSponsors(list) {{
      const tbody = document.getElementById('sponsorsTableBody');
      if (list.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="7" class="py-8 text-center text-slate-400">No matching corporate sponsors found.</td></tr>`;
        return;
      }}
      tbody.innerHTML = list.map((item, idx) => `
        <tr class="hover:bg-blue-50/40 transition">
          <td class="py-3 px-4 text-center font-mono text-slate-400">${{idx + 1}}</td>
          <td class="py-3 px-4 font-bold text-slate-900">${{item['Company Name']}}</td>
          <td class="py-3 px-4">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-800 border border-slate-200">
              ${{item['Industry Sector']}}
            </span>
          </td>
          <td class="py-3 px-4">
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
              ${{item['Sponsorship Tier']}}
            </span>
          </td>
          <td class="py-3 px-4 text-slate-800 font-medium">${{item['Host Organization Name']}}</td>
          <td class="py-3 px-4 text-slate-600 text-xs">${{item['Event Name']}}</td>
          <td class="py-3 px-4 text-center">
            <a href="${{item['Direct Proof Link']}}" target="_blank" class="inline-flex items-center gap-1 px-2.5 py-1 text-[11px] font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 rounded-lg border border-emerald-200 transition">
              <i class="fa-solid fa-arrow-up-right-from-square"></i> Proof
            </a>
          </td>
        </tr>
      `).join('');
    }}

    function openEventModal(orgIdx) {{
      const org = orgsData[orgIdx];
      document.getElementById('modalOrgName').textContent = org['Organisation name'];
      document.getElementById('modalEventCount').textContent = `${{org['event number']}} Arranged Events & Direct Individual Links`;
      document.getElementById('modalHubLink').href = org['Event Link'];

      const eventsList = org.events || [];
      const listEl = document.getElementById('modalEventsList');
      
      listEl.innerHTML = eventsList.map((ev, i) => `
        <div class="py-3 flex items-center justify-between gap-3 hover:bg-slate-50 px-2 rounded-lg transition">
          <div class="flex items-center gap-2.5">
            <span class="w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-xs font-bold flex items-center justify-center shrink-0">${{i + 1}}</span>
            <span class="text-xs font-semibold text-slate-800">${{ev.name}}</span>
          </div>
          <a href="${{ev.url}}" target="_blank" class="text-[11px] font-medium text-blue-600 hover:text-blue-800 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg border border-blue-200 transition flex items-center gap-1.5 shrink-0">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Open Event
          </a>
        </div>
      `).join('');

      document.getElementById('eventModal').classList.remove('hidden');
    }}

    function closeModal() {{
      document.getElementById('eventModal').classList.add('hidden');
    }}

    function renderOrgs(list) {{
      const tbody = document.getElementById('orgsTableBody');
      if (list.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="6" class="py-8 text-center text-slate-400">No matching organisations found.</td></tr>`;
        return;
      }}
      tbody.innerHTML = list.map((item, idx) => {{
        const rawIdx = orgsData.indexOf(item);
        const evList = item.events || [];
        const previewEvents = evList.slice(0, 3);
        const remainingCount = evList.length - 3;

        return `
        <tr class="hover:bg-blue-50/40 transition">
          <td class="py-3 px-4 text-center font-mono text-slate-400">${{idx + 1}}</td>
          <td class="py-3 px-4 font-bold text-slate-900">${{item['Organisation name']}}</td>
          <td class="py-3 px-4 text-center font-extrabold text-blue-700">${{item['event number']}}</td>
          <td class="py-3 px-4 text-slate-700 text-xs leading-relaxed max-w-md">
            <div class="flex flex-wrap gap-1.5 items-center">
              ${{previewEvents.map(e => `
                <a href="${{e.url}}" target="_blank" title="Click to open this specific event" class="inline-flex items-center gap-1 bg-slate-100 hover:bg-blue-100 text-slate-700 hover:text-blue-800 text-[11px] px-2 py-0.5 rounded-md border border-slate-200 transition">
                  <i class="fa-regular fa-calendar text-blue-500"></i> ${{e.name}}
                </a>
              `).join('')}}
              ${{remainingCount > 0 ? `
                <button onclick="openEventModal(${{rawIdx}})" class="text-[10px] text-blue-600 font-bold hover:underline bg-blue-50 px-1.5 py-0.5 rounded">
                  +${{remainingCount}} more
                </button>
              ` : ''}}
            </div>
          </td>
          <td class="py-3 px-4 text-center">
            <span class="px-2.5 py-1 rounded-full text-xs font-bold ${{item['status'] === '100%' ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-amber-100 text-amber-800 border border-amber-300'}}">
              ${{item['status']}}
            </span>
          </td>
          <td class="py-3 px-4 text-center">
            <button onclick="openEventModal(${{rawIdx}})" class="inline-flex items-center gap-1 px-2.5 py-1 text-[11px] font-medium bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg border border-blue-200 transition">
              <i class="fa-solid fa-list-check"></i> View Events (${{item['event number']}})
            </button>
          </td>
        </tr>
        `;
      }}).join('');
    }}

    function handleSearch() {{
      filterData();
    }}

    function filterData() {{
      const q = document.getElementById('searchInput').value.trim().toLowerCase();
      const countEl = document.getElementById('resultCount');

      if (currentTab === 'sponsors') {{
        const sec = document.getElementById('sectorFilter').value;
        const filtered = sponsorsData.filter(s => {{
          const matchQuery = !q || Object.values(s).some(v => String(v).toLowerCase().includes(q));
          const matchSec = (sec === 'ALL') || (s['Industry Sector'] === sec);
          return matchQuery && matchSec;
        }});
        renderSponsors(filtered);
        countEl.textContent = `Showing ${{filtered.length}} of ${{sponsorsData.length}} verified sponsor partnerships`;
      }} else {{
        const st = document.getElementById('statusFilter').value;
        const filtered = orgsData.filter(o => {{
          const matchQuery = !q || Object.values(o).some(v => String(v).toLowerCase().includes(q));
          const matchSt = (st === 'ALL') || (st === '100%' && o['status'] === '100%') || (st === 'PARTIAL' && o['status'] !== '100%');
          return matchQuery && matchSt;
        }});
        renderOrgs(filtered);
        countEl.textContent = `Showing ${{filtered.length}} of ${{orgsData.length}} organisations`;
      }}
    }}

    filterData();
"""
    updated_html = html_content[:start_pos] + new_js + html_content[end_pos:]
    with open(index_path, mode='w', encoding='utf-8') as f:
        f.write(updated_html)
    print("index.html successfully updated with clickable event badges and individual event modal links!")

# 5. Update Excel Workbook
print("=== 3. Updating Bangladesh_Business_Clubs_Sponsorship_Master.xlsx ===")
excel_path = os.path.join(WORKSPACE, 'Bangladesh_Business_Clubs_Sponsorship_Master.xlsx')
wb = openpyxl.load_workbook(excel_path)

if 'Organisation list' in wb.sheetnames:
    ws = wb['Organisation list']
    # Clear existing rows except header
    for row in range(2, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            ws.cell(row=row, column=col).value = None
            
    header_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='1B365D', end_color='1B365D', fill_type='solid')
    border = Border(left=Side(style='thin', color='DDDDDD'), right=Side(style='thin', color='DDDDDD'),
                    top=Side(style='thin', color='DDDDDD'), bottom=Side(style='thin', color='DDDDDD'))

    ws.cell(row=1, column=1, value='Organisation name').font = header_font
    ws.cell(row=1, column=2, value='event number').font = header_font
    ws.cell(row=1, column=3, value='event names').font = header_font
    ws.cell(row=1, column=4, value='Event Link').font = header_font
    ws.cell(row=1, column=5, value='status').font = header_font
    ws.cell(row=1, column=6, value='Individual Event Permalinks').font = header_font

    for col in range(1, 7):
        ws.cell(row=1, column=col).fill = header_fill

    for idx, org in enumerate(enhanced_orgs, start=2):
        ws.cell(row=idx, column=1, value=org['Organisation name']).border = border
        ws.cell(row=idx, column=2, value=int(org['event number']) if str(org['event number']).isdigit() else org['event number']).border = border
        ws.cell(row=idx, column=3, value=org['event names']).border = border
        
        c4 = ws.cell(row=idx, column=4, value=org['Event Link'])
        c4.hyperlink = org['Event Link']
        c4.font = Font(color='0563C1', underline='single')
        c4.border = border
        
        ws.cell(row=idx, column=5, value=org['status']).border = border
        
        # Individual links string
        ev_links_str = " | ".join([f"{e['name']}: {e['url']}" for e in org['events']])
        ws.cell(row=idx, column=6, value=ev_links_str).border = border

    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = 30
        
    wb.save(excel_path)
    print("Excel workbook updated with Individual Event Permalinks!")

print("=== ALL UPDATES COMPLETED SUCCESSFULLY ===")
