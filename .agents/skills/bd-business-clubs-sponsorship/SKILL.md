---
name: bd-business-clubs-sponsorship
description: >-
  Systematic workflow and rules for extracting, verifying, and publishing corporate sponsorships
  across Bangladesh student business, career, and entrepreneurship clubs. Enforces strict Bangladesh-only
  territory, host-only attribution, individual event permalinks, exact photo/post proof links, recursive
  partner club discovery, Google Sheets sync, Excel generation, GitHub sync, and Vercel web deployment.
---

# Bangladesh Business & Career Clubs Sponsorship Research Skill

This skill provides the standard operating procedure (SOP), strict verification invariants, data formats, and multi-channel synchronization pipelines for corporate sponsorship intelligence across student business and career clubs in Bangladesh.

---

## 1. Core Principles & Mandatory Invariants

### Invariant 1: Bangladesh Territory Only (Strict Boundary)
- Every single school, college, and university audited MUST strictly be located inside Bangladesh.
- No international or foreign institutions allowed.

### Invariant 2: Individual Event Permalinks (No Generic `/events` Hub Links)
- In the `Organisation list`, every arranged event MUST be mapped to its own individual direct event permalink (`https://www.facebook.com/events/<EVENT_ID>/`).
- A generic club `/events` link alone is insufficient. Each arranged event must have an individual clickable link in the data and web UI.

### Invariant 3: Exact Sponsor Post / Photo Permalinks (Proof Standard)
- A sponsor proof link MUST be the exact photo/post permalink where the sponsor is explicitly announced with their official logo/poster and role caption (e.g. `https://www.facebook.com/photo/?fbid=...&set=...`).
- Random club posts or search queries are strictly prohibited. The link must open the specific sponsor reveal post.

### Invariant 4: Strict Host Attribution (Host Only)
- A sponsor belongs ONLY to the club that arranged and hosted the event.
- If Club B participates in Club A's fest, or reshares Club A's roadshow poster, that sponsor belongs ONLY to Club A, never Club B.
- Personal payment accounts (e.g. personal bKash/Nagad for iftar or entry fees) are NOT corporate sponsorships.

### Invariant 5: Recursive Partner Club Discovery
- Inspect event partner reveal posts and banners (e.g. "Introducing Our Club Partners", "Promotional Partners", "Roadshow Partners").
- Extract every collaborating club (e.g. SHKSC Nutrition Club, ACPS Business & Economics Club, Amrita Lal Dey Debating Club, etc.).
- Immediately check and append missing partner clubs to the `Organisation list`.

### Invariant 6: Concurrent Multi-Subagent Execution
- When crawling or auditing multiple clubs, run 3 to 4 subagents concurrently to avoid blocking on slow page loads.

### Invariant 7: Real Chrome Profile & DOM Navigation (No Blank/Incognito Windows)
- Operate strictly within the user's active Chrome browser profile where their session is logged in.
- Do not launch blank, clean, or incognito Chrome instances that lack authentication.
- When navigating Facebook pages and photo dialogs, use real DOM events and tab multitasking. While one tab is loading, switch to another tab to extract data in parallel.

### Invariant 8: Real-time Messenger Progress Updates
- Frequently notify the user ("Sakibul Hasan Sakin") on Facebook Messenger through their active browser session with concise milestone updates on newly verified sponsor links and ingested partner clubs.

---

## 2. Standard Operating Procedure (SOP)

```
[1. Identify Club in Bangladesh]
       │
       ▼
[2. Inventory Arranged Events with Individual Event Links]
       │
       ▼
[3. Inspect Event Discussion & Post Feeds for Sponsor Reveals]
       │
       ▼
[4. Extract Exact Photo/Post Permalinks for Each Corporate Sponsor]
       │
       ▼
[5. Discover & Ingest Collaborating Partner Clubs into Organisation List]
       │
       ▼
[6. Multi-Channel Synchronization: CSV, Excel, Google Sheets, GitHub, Vercel]
```

---

## 3. Data Schemas & Deliverables

### (a) Organisation List (5 Columns + Individual Event Links Map)
- `Organisation name`: Full official club name and institution
- `event number`: Exact count of arranged/co-organized events
- `event names`: Title of each arranged event
- `Event Link`: Direct individual event links (or formatted individual map: `Event 1: https://... | Event 2: https://...`)
- `status`: Completion percentage (`100%`, `60%`, `50%`, `30%`, `Pending`)

### (b) Formatted Sponsor List (4 Columns)
- `Company Name`: Corporate brand / entity
- `Sponsor Event Name`: Exact event title
- `Organization Name`: Host club only
- `Event Link`: Exact sponsor reveal post/photo permalink

### (c) Master Sponsor Directory (7 Columns)
- `SL No, Company Name, Industry Sector, Sponsorship Tier, Host Organization Name, Event Name, Direct Proof Link`

---

## 4. Multi-Channel Synchronization Runbook

1. **Google Sheets CLI**:
   ```bash
   gsheets mutate import-csv <SPREADSHEET_ID> <CSV_PATH> --sheet "<SHEET_NAME>"
   gsheets mutate freeze <SPREADSHEET_ID> --sheet-id <ID> --rows 1
   gsheets mutate autosize <SPREADSHEET_ID> --sheet-id <ID> --start-col 0 --end-col <N>
   ```

2. **Git & GitHub Single Repository**:
   ```bash
   git add .
   git commit -m "<Descriptive message>"
   git push origin main
   ```

3. **Vercel Instant Deployment**:
   ```powershell
   $headers = @{ "Authorization" = "Bearer <VERCEL_TOKEN>"; "Content-Type" = "application/json" }
   $body = @{ "name" = "dccbc-sponsorship-master"; "project" = "<PROJECT_ID>"; "gitSource" = @{ "type" = "github"; "ref" = "main"; "repo" = "coc86808/dccbc-sponsorship-master"; "repoId" = 1449619264 } } | ConvertTo-Json
   Invoke-RestMethod -Uri "https://api.vercel.com/v13/deployments" -Method Post -Headers $headers -Body $body
   ```
