# Data Update Workflow

This document describes how to update the dashboard with fresh data from the House Oversight Committee Democrats' Immigration Enforcement Dashboard.

## Prerequisites

- Python 3.8+
- No external dependencies (uses only standard library)

## Quick Update

```bash
# 1. Scrape fresh data and output as JavaScript
python scripts/scrape_dashboard.py --format js --output scripts/new_data.js

# 2. The output will look like:
#    const REAL_INCIDENT_DATA = [
#      {date: "2025-11-20", city: "Long Beach", state: "California", ...},
#      ...
#    ];

# 3. Copy the array contents into index.html, replacing the existing
#    REAL_INCIDENT_DATA array (around line 780)

# 4. Update the "Last Updated" date in:
#    - index.html (search for "Last scraped:")
#    - README.md (search for "Last Updated")
```

## Detailed Steps

### Step 1: Run the Scraper

```bash
cd scripts/

# Option A: Output JSON (for inspection/debugging)
python scrape_dashboard.py --output data.json

# Option B: Output JavaScript array (for embedding)
python scrape_dashboard.py --format js --output new_data.js
```

The scraper will:
1. Detect the total number of pages automatically
2. Scrape each page sequentially (20 incidents per page)
3. Parse incident data: date, location, categories, source URL/title
4. Sort by date descending
5. Output in the requested format

### Step 2: Review the Data

```bash
# Check incident count
python -c "import json; d=json.load(open('data.json')); print(f'{d[\"total_incidents\"]} incidents')"

# Preview first few incidents
python -c "import json; d=json.load(open('data.json')); print(json.dumps(d['incidents'][:3], indent=2))"
```

### Step 3: Update index.html

1. Open `index.html` in your editor
2. Find the line: `const REAL_INCIDENT_DATA = [`
3. Replace the entire array with the contents of `new_data.js`
4. Update the comment with the new scrape date:
   ```javascript
   // Real data from House Committee on Oversight and Reform Democrats
   // Source: https://oversightdemocrats.house.gov/immigration-dashboard
   // Last scraped: [NEW DATE HERE]
   ```

### Step 4: Update Documentation

In `README.md`, update:
```markdown
**Last Updated**: [NEW DATE]  
**Total Incidents**: [NEW COUNT]
```

### Step 5: Commit and Deploy

```bash
git add index.html README.md
git commit -m "Update data: [COUNT] incidents as of [DATE]"
git push
```

GitHub Pages will automatically redeploy within ~60 seconds.

---

## Output Formats

### JSON Format (`--format json`)

```json
{
  "last_updated": "2025-11-28T10:10:32.669205",
  "source": "https://oversightdemocrats.house.gov/immigration-dashboard",
  "total_incidents": 251,
  "incidents": [
    {
      "date": "2025-11-20",
      "city": "Long Beach",
      "state": "California",
      "categories": ["Concerning Use of Force", "Concerning Arrest/Detention"],
      "source_url": "https://...",
      "source_title": "Article headline...",
      "is_us_citizen": false,
      "is_sensitive_location": false,
      "is_use_of_force": true,
      "is_arrest_detention": true,
      "is_deportation": false
    }
  ]
}
```

### JavaScript Format (`--format js`)

```javascript
const REAL_INCIDENT_DATA = [
  {date: "2025-11-20", city: "Long Beach", state: "California", categories: ["use of force", "arrest/detention"], usCitizen: false, sensitiveLocation: null, sourceUrl: "https://...", sourceTitle: "..."},
  // ...
];
```

---

## Automation (Optional)

### GitHub Actions

Create `.github/workflows/update-data.yml`:

```yaml
name: Update Dashboard Data

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM UTC
  workflow_dispatch:      # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Scrape data
        run: python scripts/scrape_dashboard.py --format js --output scripts/new_data.js
      
      - name: Update index.html
        run: |
          # This would require a more sophisticated script to inject the data
          # For now, manual updates are recommended
          echo "Data scraped. Manual review required."
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Data update: $(date +%Y-%m-%d)"
          body: "Automated data scrape from source dashboard."
          branch: data-update-${{ github.run_number }}
```

---

## Troubleshooting

### "Connection refused" or timeout errors

The source site may be rate-limiting or temporarily unavailable. Wait a few minutes and retry.

### Missing incidents

The scraper relies on the HTML structure of the source page. If the site redesigns, the regex patterns in `scrape_dashboard.py` may need updating.

### Character encoding issues

The scraper uses UTF-8 encoding and `html.unescape()` to handle special characters. If you see garbled text, check that the source hasn't changed its encoding.

---

## Data Integrity Notes

- **Source of truth**: https://oversightdemocrats.house.gov/immigration-dashboard
- **Verification**: All incidents are verified by media outlets or court filings (per source)
- **No modifications**: The scraper extracts data as-is; no editorial changes are made
- **Timestamps**: Dates are preserved exactly as published on the source
