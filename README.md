# Oversight Immigration Enforcement Dashboard

An interactive visualization of verified immigration enforcement incidents compiled by the [House Committee on Oversight and Reform Democrats](https://oversightdemocrats.house.gov/immigration-dashboard).

## Live Demo

🔗 **[View Dashboard](https://johnholliday.github.io/immigration-dashboard/)**

## Overview

This dashboard provides interactive visualizations of documented incidents of possible misconduct during federal immigration enforcement operations. All data is sourced directly from the official House Oversight Committee Democrats' dashboard, which only includes incidents verified by reputable media outlets or referenced in federal court filings.

### Features

- **Interactive Filtering**: Filter by date range, location, incident category, U.S. citizen involvement, and sensitive location enforcement
- **Multiple Visualizations**:
  - Category distribution (pie chart)
  - Monthly trends (bar chart)
  - Cumulative timeline (line chart)
  - Weekly heatmap
  - Geographic distribution (choropleth map)
  - Top locations breakdown
  - Sensitive location breakdown
- **Hierarchical Incident Browser**: Expandable tree organized by State → City → Date with source links
- **Data Export**: Download filtered data as CSV with dynamic filename reflecting active filters
- **Take Action Panel**: Quick links to report wrongdoing, latest news, and the Oversight Committee website
- **Dark/Light Theme**: Toggle for accessibility
- **Responsive Design**: Three-column layout (credits | visualizations | filters) that adapts to mobile

## Data Source

All incident data is scraped from the official [Oversight Immigration Enforcement Dashboard](https://oversightdemocrats.house.gov/immigration-dashboard) maintained by House Committee on Oversight and Reform Democrats.

**Inclusion Criteria** (per the Committee):
- Verified by reputable media outlets OR
- Referenced in federal court filings/litigation
- Social media videos without corroboration are excluded

**Last Updated**: November 28, 2025
**Total Incidents**: 314

## Categories Tracked

| Category | Description |
|----------|-------------|
| Concerning Use of Force | Allegations of excessive or inappropriate force |
| Concerning Arrest/Detention | Procedural concerns during arrest or detention |
| Concerning Deportation | Issues related to deportation proceedings |
| Sensitive Location | Enforcement at schools, churches, hospitals, courthouses |
| U.S. Citizen | Incidents involving U.S. citizens |

## Take Action

The dashboard includes direct links to official House Oversight Committee resources:

- **[Report Potential Wrongdoing](https://oversightdemocrats.house.gov/contact/tip-line)** — Submit tips about immigration enforcement misconduct
- **[Latest News](https://oversightdemocrats.house.gov/news)** — Press releases and updates from the Committee
- **[Oversight Committee](https://oversightdemocrats.house.gov)** — Main Committee website

## Technology

- Pure HTML/CSS/JavaScript (no build step required)
- [Plotly.js](https://plotly.com/javascript/) for interactive charts
- [Font Awesome](https://fontawesome.com/) for icons
- CSS Variables for theming
- LocalStorage for user preferences

## Deployment

### GitHub Pages (Recommended)

1. Fork this repository
2. Go to Settings → Pages
3. Select "main" branch as source
4. Your dashboard will be live at `https://yourusername.github.io/immigration-dashboard/`

### Netlify

1. Drag the folder to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Instant deployment

### Self-Hosted

Simply serve `index.html` from any web server. No dependencies or build process required.

## Updating Data

The incident data is embedded in `index.html`. To update with fresh data:

```bash
# Scrape fresh data from the source
python scripts/scrape_dashboard.py --format js --output scripts/new_data.js

# Then copy the REAL_INCIDENT_DATA array into index.html
# See scripts/UPDATE_WORKFLOW.md for detailed instructions
```

**Scripts included:**
- `scripts/scrape_dashboard.py` — Python scraper (no dependencies)
- `scripts/UPDATE_WORKFLOW.md` — Detailed update instructions

## Disclaimer

This is an **unofficial** visualization tool created for educational and oversight purposes. It is not affiliated with, endorsed by, or officially connected to the House Committee on Oversight and Reform or any government entity.

The dashboard faithfully represents data from the official source but the visualization design and implementation are independent contributions.

## Author

**John F. Holliday**  
Information Architect & Software Engineer  
[johnholliday.net](https://johnholliday.net)

## License

MIT License - Free to use, modify, and distribute.

The underlying incident data is public information compiled by the U.S. House of Representatives.
