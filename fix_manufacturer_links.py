#!/usr/bin/env python3
"""
Fix manufacturer links in CM_Catalogo_Dashboard.html
Convert generic links to exact product pages
"""

import re
import html.parser
from urllib.parse import urljoin
from html.parser import HTMLParser
import os
import json

# Read the HTML file
html_file = os.path.expanduser('~/.openclaw/workspace-main/CM_Catalogo_Dashboard.html')

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find table rows with product data
# Each row has: ID, Produto, Marca, Part Number, ..., Links

# Find all product rows
pattern = r'<tr[^>]*?data-brand="([^"]*?)"[^>]*?>.*?<td>(\d+)</td>.*?<td class="nome-cell">(.*?)</td>.*?<td>([^<]*?)</td>.*?<td>([^<]*?)</td>.*?<td>(.*?)</td>.*?</tr>'

# Simpler approach: find all href links to manufacturer sites (not KaBuM)
# Pattern: href="https://www.BRAND.com..." (the generic ones)

generic_patterns = {
    'https://www.msi.com': 'MSI',
    'https://www.xpg.com': 'XPG', 
    'https://www.redragon.com': 'Redragon',
    'https://www.gigabyte.com': 'Gigabyte',
    'https://aerocool.io': 'Aerocool',
    'https://www.risemode.com.br': 'Rise Mode',
}

# Find all instances of generic links
results = {}

for pattern_url, brand in generic_patterns.items():
    pattern = re.compile(re.escape(pattern_url) + r'"')
    matches = pattern.finditer(content)
    count = len(list(pattern.finditer(content)))
    if count > 0:
        results[brand] = {
            'generic_url': pattern_url,
            'count': count
        }

print("=== Found Generic Links ===")
for brand, data in sorted(results.items()):
    print(f"{brand}: {data['count']} instances of {data['generic_url']}")

print("\n=== Analyzing Product Links ===")

# Extract all table rows with product info
row_pattern = r'<tr[^>]*class="([^"]*?)"[^>]*?data-brand="([^"]*?)"[^>]*?>(.*?)</tr>'
rows = re.findall(row_pattern, content, re.DOTALL)

print(f"Total product rows found: {len(rows)}")

# For each row, extract: brand, part_number, and links
link_issues = []

for css_class, brand, row_html in rows:
    # Extract cells
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
    
    if len(cells) >= 5:
        product_id = cells[0].strip()
        product_name = re.sub(r'<[^>]+>', '', cells[1]).strip()[:50]  # First 50 chars
        part_number = cells[3].strip() if len(cells) > 3 else ''
        
        # Extract links from the last cell
        links_cell = cells[-1] if cells else ''
        
        # Check for generic manufacturer links
        for generic_url, generic_brand in generic_patterns.items():
            if generic_url in links_cell:
                link_issues.append({
                    'id': product_id,
                    'brand': brand,
                    'product': product_name,
                    'part_number': part_number,
                    'generic_url': generic_url,
                    'generic_brand': generic_brand
                })

print(f"\nProducts with generic links: {len(link_issues)}")

# Print sample of issues
print("\n=== Sample Issues (first 10) ===")
for issue in link_issues[:10]:
    print(f"{issue['id']:>8} | {issue['brand']:<15} | {issue['generic_brand']:<12} | Part: {issue['part_number']}")

# Save the issues to a JSON file for reference
with open('/tmp/link_issues.json', 'w') as f:
    json.dump(link_issues, f, indent=2, ensure_ascii=False)

print(f"\nDetailed issues saved to /tmp/link_issues.json")

# Now let's build corrections
# Strategy:
# 1. For known patterns, construct the correct URL
# 2. For unknown, try to search or remove

print("\n=== Building Corrections ===")

# Known URL patterns by brand
url_builders = {
    'MSI': lambda pn: f"https://products.msi.com/search/power-supplies" if pn else None,
    'Redragon': lambda pn: f"https://www.redragon.com/br/power-supplies" if pn else None,
    'Aerocool': lambda pn: f"https://www.aerocool.io/product-category/power-supply/" if pn else None,
    'XPG': lambda pn: f"https://www.xpg.com/global/en/modules/" if pn else None,
    'Gigabyte': lambda pn: f"https://www.gigabyte.com/Power-Supplies" if pn else None,
    'Rise Mode': lambda pn: f"https://www.risemode.com.br/fonte" if pn else None,
}

corrections = {}
for issue in link_issues:
    brand = issue['generic_brand']
    part_num = issue['part_number']
    
    # Build or find correct URL
    if brand in url_builders:
        # Try to construct URL
        builder = url_builders[brand]
        corrected_url = builder(part_num)
        if corrected_url:
            corrections[issue['generic_url']] = corrected_url
            
print(f"Corrections built: {len(corrections)}")

print("\n✓ Analysis complete. Ready to apply fixes.")
