# Immigration Enforcement Dashboard - AI Agent Instructions

## Project Overview

This is a **single-file static web application** (`index.html`) that visualizes immigration enforcement incidents from the House Committee on Oversight and Reform Democrats. No build process, no dependencies to install—just pure HTML/CSS/JavaScript.

## Architecture

### Single-File Design
- **Everything in `index.html`**: All CSS (in `<style>` tags), JavaScript (in `<script>` tags), and HTML structure
- **External dependencies**: Only CDN-loaded libraries (Plotly.js, Font Awesome)
- **No transpilation/bundling**: Code runs directly in the browser
- **Deployment**: Simply serve `index.html` from any web server or GitHub Pages

### Data Structure
Incidents are stored as a JavaScript array `REAL_INCIDENT_DATA` embedded directly in the HTML:
```javascript
{ 
  date: "2025-11-20",           // String, converted to Date object
  city: "Long Beach", 
  state: "California",
  categories: ["use of force", "arrest/detention"],  // Array of lowercase strings
  usCitizen: false,             // Boolean
  sensitiveLocation: null,      // String: "School", "Church", "Hospital", etc. or null
  sourceUrl: "https://...",     // Direct link to news article
  sourceTitle: "..."            // Article headline
}
```

**Critical**: Categories must be lowercase for filtering to work. Sensitive location types are title-cased.

## Key Patterns & Conventions

### Theme System
Uses CSS variables for light/dark theming:
- Theme toggled via `data-theme="dark"` attribute on `<body>`
- Stored in `localStorage` as `'theme'` key
- All colors reference CSS variables: `var(--bg-primary)`, `var(--text-primary)`, etc.
- Plotly charts detect theme: `const isDark = document.body.getAttribute('data-theme') === 'dark'`

### Filtering Architecture
Two-stage filtering system:
1. **Global `filteredData`**: Holds currently filtered incidents
2. **`applyFilters()` function**: 
   - Reads all filter inputs (date range, location, category, citizen status, sensitive location)
   - Filters `REAL_INCIDENT_DATA` array
   - Updates metrics, charts, and incident list
   - Category filter uses radio buttons with `value="all"` or specific category names (lowercase)

### Chart Rendering
All charts use Plotly.js with consistent patterns:
- Each chart has its own `render*Chart()` function (e.g., `renderCategoryChart()`)
- Transparent backgrounds: `plot_bgcolor: 'transparent', paper_bgcolor: 'transparent'`
- Theme-aware text colors: Check `data-theme` attribute before rendering
- Centered charts: CSS uses flexbox with `justify-content: center`
- Responsive: `{ responsive: true }` in Plotly config

### State Management
- **Theme**: `localStorage.getItem('theme')` / `localStorage.setItem('theme', value)`
- **Panel state**: CSS class toggle on `<body>` (`panel-open`) and panel element (`open`)
- **Incident cards**: Toggle `.active` class on `.incident-content` to expand/collapse
- **Tab navigation**: Toggle `.active` class on both button and content div

## Common Tasks

### Updating Data
1. Add new incidents to `REAL_INCIDENT_DATA` array (around line 817)
2. Update "Last Updated" date in README.md and in the data comment
3. Update total incident count in `<div id="metric-total">` (line 705)
4. **Important**: Categories must match existing lowercase strings: `"use of force"`, `"arrest/detention"`, `"deportation"`, `"sensitive location"`

### Adding a New Chart
1. Create a render function (e.g., `function renderMyChart()`)
2. Use `filteredData` array as data source
3. Include theme detection: `const isDark = document.body.getAttribute('data-theme') === 'dark'`
4. Add corresponding `<div>` with unique ID to HTML
5. Call function in `renderCharts()` function
6. Add to tab content structure if it's a new visualization tab

### Adding a New Filter
1. Add HTML input in `.sidebar` section
2. Add event listener in `DOMContentLoaded` handler
3. Modify `applyFilters()` to read the new filter value
4. Apply filter logic to `REAL_INCIDENT_DATA.filter(...)` chain

### Styling Guidelines
- Use CSS variables for all colors (never hardcode hex/rgb values)
- Maintain transition properties for theme switching: `transition: background-color 0.3s, color 0.3s`
- Follow existing class naming: kebab-case (`.incident-card`, `.filter-group`)
- Maintain responsive grid patterns: `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))`

## Testing & Validation

### Local Testing
No build step required. Open `index.html` in a browser:
- **Windows**: `start index.html` or double-click file
- **Mac**: `open index.html`
- **Local server** (optional): `python -m http.server` or any static server

### Data Validation Checks
- All dates must be valid ISO format strings (`YYYY-MM-DD`)
- Categories must be lowercase and match filter options
- `sourceUrl` should be valid URLs
- `sensitiveLocation` must be title-cased or `null`
- Boolean fields must be actual booleans, not strings

### Browser Compatibility
- Tested on modern Chrome, Firefox, Safari, Edge
- Uses ES6+ features (arrow functions, template literals, spread operator)
- No polyfills included—assumes modern browser

## Deployment

### GitHub Pages
1. Push to `main` branch
2. Enable Pages in repo settings (source: `main` branch)
3. URL will be `https://[username].github.io/[repo-name]/`

### Other Hosts
Just upload `index.html` to any static hosting (Netlify Drop, Vercel, S3, etc.). No special configuration needed.

## Project-Specific Notes

- **Data source**: House Oversight Committee Democrats dashboard (only verified incidents)
- **Verification criteria**: Must have reputable media coverage OR court filing references
- **Disclaimer**: This is an unofficial visualization tool, not affiliated with the government
- **License**: MIT License
- **Author**: John F. Holliday (Information Architect & Software Engineer)

## What NOT to Do

- ❌ Don't add a build process (webpack, vite, etc.)—this is intentionally build-free
- ❌ Don't extract CSS/JS into separate files—single-file architecture is deliberate
- ❌ Don't add npm packages—use CDN resources only
- ❌ Don't modify category strings without updating filters/tags/styling
- ❌ Don't break the two-way theme sync between CSS variables and Plotly charts
