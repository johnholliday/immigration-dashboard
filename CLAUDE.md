# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-file static web application (`index.html`) visualizing immigration enforcement incidents from the House Committee on Oversight and Reform Democrats. No build process, no npm dependencies—pure HTML/CSS/JavaScript with CDN-loaded libraries (Plotly.js, Font Awesome).

## Commands

### Local Testing
```bash
# Open directly in browser (no server needed)
open index.html          # Mac
start index.html         # Windows
xdg-open index.html      # Linux

# Optional: serve locally
python -m http.server
```

### Data Updates
```bash
# Scrape fresh data
python scripts/scrape_dashboard.py --format js --output scripts/new_data.js

# Then manually replace REAL_INCIDENT_DATA array in index.html
```

## Architecture

### Single-File Design
Everything lives in `index.html`:
- CSS in `<style>` tags (uses CSS variables for light/dark theming)
- JavaScript in `<script>` tags
- Data embedded as `REAL_INCIDENT_DATA` array

### Data Structure
```javascript
{
  date: "2025-11-20",           // ISO format string
  city: "Long Beach",
  state: "California",
  categories: ["use of force", "arrest/detention"],  // MUST be lowercase
  usCitizen: false,             // Boolean
  sensitiveLocation: null,      // "School", "Church", "Hospital", or null
  sourceUrl: "https://...",
  sourceTitle: "..."
}
```

### Theme System
- Toggle via `data-theme="dark"` attribute on `<body>`
- All colors use CSS variables: `var(--bg-primary)`, `var(--text-primary)`, etc.
- Plotly charts detect theme: `document.body.getAttribute('data-theme') === 'dark'`
- Persisted in `localStorage` under `'theme'` key

### Filtering Flow
1. User interacts with filter controls in sidebar
2. `applyFilters()` reads all inputs and filters `REAL_INCIDENT_DATA`
3. Results stored in global `filteredData`
4. Calls `renderCharts()` and `renderIncidentList()`

### Chart Pattern
Each chart has a `render*Chart()` function that:
- Uses `filteredData` as source
- Clears container innerHTML before rendering (prevents overlap)
- Sets transparent backgrounds and theme-aware text colors
- Uses `{ responsive: true }` in Plotly config

## Key Constraints

- **Do not add build tools** (webpack, vite, etc.)—intentionally build-free
- **Do not extract CSS/JS** into separate files—single-file architecture is deliberate
- **Do not add npm packages**—use CDN resources only
- **Categories must be lowercase** for filtering to work
- **Sensitive locations must be title-cased** or null

## File Locations

- `index.html` — The entire application
- `scripts/scrape_dashboard.py` — Python scraper (no dependencies)
- `scripts/UPDATE_WORKFLOW.md` — Detailed data update instructions
