#!/usr/bin/env python3
"""
Scrape incident data from the House Oversight Committee Democrats 
Immigration Enforcement Dashboard.

Source: https://oversightdemocrats.house.gov/immigration-dashboard

Usage:
    python scrape_dashboard.py                    # Output JSON to stdout
    python scrape_dashboard.py --output data.json # Save to file
    python scrape_dashboard.py --format js        # Output as JavaScript array
    python scrape_dashboard.py --format js --output ../data.js
"""

import urllib.request
import re
import json
import argparse
from html import unescape
from datetime import datetime


BASE_URL = "https://oversightdemocrats.house.gov/immigration-dashboard"


def scrape_page(page_num: int) -> list[dict]:
    """Scrape a single page of incidents."""
    url = f"{BASE_URL}?page={page_num}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; OversightDashboardScraper/1.0)'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching page {page_num}: {e}", file=__import__('sys').stderr)
        return []
    
    incidents = []
    
    # Regex patterns to extract data from table rows
    date_pattern = r'<time datetime="([^"]+)">[^<]+</time>'
    city_pattern = r'views-field-field-city[^>]*>([^<]+)</td>'
    category_pattern = r'views-field-field-category">([^<]+)</td>'
    link_pattern = r'views-field-field-link[^>]*><a href="([^"]+)">([^<]+)</a>'
    
    # Split by table rows
    rows = re.split(r'<tr>', html)
    
    for row in rows[1:]:  # Skip first split (before any <tr>)
        if 'views-field-field-date-inc' not in row:
            continue
            
        date_match = re.search(date_pattern, row)
        city_match = re.search(city_pattern, row)
        category_match = re.search(category_pattern, row)
        link_match = re.search(link_pattern, row)
        
        if date_match and category_match and link_match:
            date_str = date_match.group(1)[:10]  # YYYY-MM-DD
            city_state = city_match.group(1).strip() if city_match else "Unknown"
            categories = [c.strip() for c in category_match.group(1).split(',')]
            source_url = unescape(link_match.group(1))
            source_title = unescape(link_match.group(2)).strip()
            
            # Parse city and state
            parts = city_state.rsplit(',', 1)
            city = parts[0].strip() if parts else city_state
            state = parts[1].strip() if len(parts) > 1 else ""
            
            incident = {
                "date": date_str,
                "city": city,
                "state": state,
                "categories": categories,
                "source_url": source_url,
                "source_title": source_title,
                "is_us_citizen": "U.S. Citizen" in categories,
                "is_sensitive_location": any("Sensitive Location" in c for c in categories),
                "is_use_of_force": any("Use of Force" in c for c in categories),
                "is_arrest_detention": any("Arrest" in c or "Detention" in c for c in categories),
                "is_deportation": any("Deportation" in c for c in categories)
            }
            incidents.append(incident)
    
    return incidents


def get_total_pages() -> int:
    """Determine the total number of pages by checking pagination."""
    url = BASE_URL
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; OversightDashboardScraper/1.0)'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
    except Exception:
        return 13  # Default fallback
    
    # Find the last page link
    last_page_match = re.search(r'href="\?page=(\d+)"[^>]*title="Go to last page"', html)
    if last_page_match:
        return int(last_page_match.group(1)) + 1  # Pages are 0-indexed
    return 13  # Default fallback


def scrape_all() -> list[dict]:
    """Scrape all pages of incidents."""
    total_pages = get_total_pages()
    all_incidents = []
    
    for page in range(total_pages):
        print(f"Scraping page {page + 1}/{total_pages}...", file=__import__('sys').stderr)
        incidents = scrape_page(page)
        all_incidents.extend(incidents)
        print(f"  Found {len(incidents)} incidents", file=__import__('sys').stderr)
    
    # Sort by date descending
    all_incidents.sort(key=lambda x: x['date'], reverse=True)
    
    return all_incidents


def to_javascript_array(incidents: list[dict]) -> str:
    """Convert incidents to JavaScript array format for embedding in HTML."""
    lines = ["const REAL_INCIDENT_DATA = ["]
    
    for i, inc in enumerate(incidents):
        # Normalize categories to lowercase format used in dashboard
        cats = []
        for c in inc['categories']:
            if 'Use of Force' in c:
                cats.append('use of force')
            elif 'Arrest' in c or 'Detention' in c:
                cats.append('arrest/detention')
            elif 'Deportation' in c:
                cats.append('deportation')
            elif 'Sensitive Location' in c:
                cats.append('sensitive location')
        
        # Determine sensitive location type from title
        sensitive_type = 'null'
        title = inc.get('source_title', '').lower()
        if 'church' in title or 'worship' in title:
            sensitive_type = '"Church"'
        elif 'school' in title or 'daycare' in title or 'day care' in title:
            sensitive_type = '"School"'
        elif 'hospital' in title or 'medical' in title:
            sensitive_type = '"Hospital"'
        elif 'courthouse' in title or 'court' in title:
            sensitive_type = '"Courthouse"'
        elif inc['is_sensitive_location']:
            sensitive_type = '"Sensitive Location"'
        
        us_citizen = 'true' if inc['is_us_citizen'] else 'false'
        comma = '' if i == len(incidents) - 1 else ','
        
        line = (
            f'  {{date: "{inc["date"]}", '
            f'city: "{inc["city"]}", '
            f'state: "{inc["state"]}", '
            f'categories: {json.dumps(cats)}, '
            f'usCitizen: {us_citizen}, '
            f'sensitiveLocation: {sensitive_type}, '
            f'sourceUrl: "{inc["source_url"]}", '
            f'sourceTitle: {json.dumps(inc["source_title"])}}}{comma}'
        )
        lines.append(line)
    
    lines.append("];")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Scrape the House Oversight Immigration Enforcement Dashboard'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'js'],
        default='json',
        help='Output format: json or js (JavaScript array)'
    )
    args = parser.parse_args()
    
    # Scrape all data
    incidents = scrape_all()
    
    # Create output
    if args.format == 'js':
        output = to_javascript_array(incidents)
    else:
        output_data = {
            "last_updated": datetime.now().isoformat(),
            "source": BASE_URL,
            "total_incidents": len(incidents),
            "incidents": incidents
        }
        output = json.dumps(output_data, indent=2)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\nSaved {len(incidents)} incidents to {args.output}", file=__import__('sys').stderr)
    else:
        print(output)
    
    print(f"\nTotal incidents scraped: {len(incidents)}", file=__import__('sys').stderr)


if __name__ == '__main__':
    main()
