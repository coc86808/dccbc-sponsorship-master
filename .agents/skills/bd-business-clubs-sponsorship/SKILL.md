---
name: bd-business-clubs-sponsorship
description: >-
  Systematic workflow and rules for extracting, verifying, and publishing corporate sponsorships
  across Bangladesh student business, career, and entrepreneurship clubs. Enforces strict host-only
  attribution, recursive partner club discovery, Google Sheets sync, Excel generation, GitHub sync,
  and Vercel web deployment.
---

# Bangladesh Business & Career Clubs Sponsorship Research Skill

This skill provides the standard operating procedure (SOP), strict verification invariants, data formats, and multi-channel synchronization pipelines for corporate sponsorship intelligence across student business and career clubs in Bangladesh.

---

## 1. Core Workflow (Step-by-Step)

```
[1. Identify Club Facebook Page]
       │
       ▼
[2. Inventory Arranged Events (event number)]
       │
       ▼
[3. Inspect Event Posts & Discussion Tabs (?active_tab=discussion)]
       │
       ▼
[4. Verify Corporate Sponsors with Strict Host Attribution]
       │
       ▼
[5. Recursive Partner Club Discovery (Expand Organization List)]
       │
       ▼
[6. Multi-Channel Synchronization: CSV, Excel, Google Sheets, GitHub, Vercel]
```

### Step 1: Identify Organization & Facebook Digital Assets
- Locate official Facebook page for the student business/career club.
- Determine primary Facebook Events tab (`/events` and `/past_hosted_events`).

### Step 2: Event Counting (`event number`)
- Count only events **actually arranged or co-organized** by that club.
- Exclude external competitions where members merely participated as delegates.

### Step 3: Event Inspection & Discussion Proof Audit
- Navigate to the event's Discussion tab: `https://www.facebook.com/events/<EVENT_ID>/?active_tab=discussion`.
- Look for official announcements, banner reveals, partner reveals, and sponsor acknowledgment posts.

### Step 4: Strict Host Attribution Rules (Mandatory Invariant)
- **Host Only**: A company is ONLY an event sponsor for the club that **organized/hosted** the event. If Club B sends participants to Club A's fest, Club B did NOT receive that sponsor.
- **Official Banner/Logo Requirement**: The post must be from the host's official page with their official event branding, naming the company and tier (Title Sponsor, Powered By, Beverage Partner, Media Partner, etc.).
- **No Shared Posts**: Resharing another club's fest poster or roadshow does NOT make that event or its sponsors belong to the sharing club.
- **No Personal Payments**: Personal bKash/Nagad/Rocket numbers used to collect entry tickets or iftar fees are NOT corporate sponsorships.
- **Valid Links Only**: Permalinks must be real Facebook Event links (`/events/<ID>/`) or specific post/photo permalinks (`/photo/?fbid=...` or `/posts/pfbid...`). Never use search queries (`/search/posts/...`) or root URLs.

### Step 5: Recursive Partner Club Discovery (Additional Work)
- While reviewing event banners and partner credits, look for collaborating student clubs (e.g., Roadshow Partners, Promotional Partners, Co-Host Clubs).
- Check the current `Organisation list`. If the collaborating club is not present, immediately add them with initial status (e.g., `40%` or `Pending`).

### Step 6: Multi-Channel Synchronization
- **Formatted Sponsor List (4 columns)**: `Company Name, Sponsor Event Name, Organization Name, Event Link`
- **Master Sponsor Directory (7 columns)**: `SL No, Company Name, Industry Sector, Sponsorship Tier, Host Organization Name, Event Name, Direct Proof Link`
- **Organisation List (5 columns)**: `Organisation name, event number, event names, Event Link, status`
- **Synchronize To**:
  1. Local CSVs (`sponsor_company_list_strictly_verified.csv`, `all_companies_strictly_verified.csv`, `organisation_list.csv`)
  2. Local multi-tab Excel workbook (`Bangladesh_Business_Clubs_Sponsorship_Master.xlsx`)
  3. Live Google Spreadsheet via `gsheets` CLI (`19A3ZJINmcG0AdaNycqclDcfVzEmo3nSIAczmap1ITiU`)
  4. GitHub single repository (`coc86808/dccbc-sponsorship-master`)
  5. Live Vercel web application (`https://dccbc-sponsorship-master.vercel.app`)

---

## 2. Technical Synchronization Commands

### Google Sheets CLI
```bash
# Import CSV to specific tab
gsheets mutate import-csv <SPREADSHEET_ID> <PATH_TO_CSV> --sheet "<SHEET_NAME>"

# Freeze header and auto-size columns
gsheets mutate freeze <SPREADSHEET_ID> --sheet-id <ID> --rows 1
gsheets mutate autosize <SPREADSHEET_ID> --sheet-id <ID> --start-col 0 --end-col <N>
```

### GitHub Push
```bash
git add .
git commit -m "<Descriptive message>"
git push origin main
```

### Vercel Deployment via REST API
```powershell
$headers = @{ "Authorization" = "Bearer <VERCEL_TOKEN>"; "Content-Type" = "application/json" }
$body = @{
    "name" = "dccbc-sponsorship-master"
    "project" = "<PROJECT_ID>"
    "gitSource" = @{
        "type" = "github"
        "ref" = "main"
        "repo" = "coc86808/dccbc-sponsorship-master"
        "repoId" = 1449619264
    }
} | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.vercel.com/v13/deployments" -Method Post -Headers $headers -Body $body
```
