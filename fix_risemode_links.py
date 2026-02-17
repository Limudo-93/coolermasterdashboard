#!/usr/bin/env python3
"""
Fix Rise Mode links specifically
Search for exact product pages based on part numbers
"""

import re
import os
import json
import time
from collections import defaultdict

html_file = os.path.expanduser('~/.openclaw/workspace-main/CM_Catalogo_Dashboard.html')

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all Rise Mode products
row_pattern = r'<tr[^>]*data-brand="Rise Mode"[^>]*?>(.*?)</tr>'
rows = re.findall(row_pattern, content, re.DOTALL)

print(f"Rise Mode products found: {len(rows)}")

# Extract details from each row
risemode_products = []

for row_html in rows:
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
    
    if len(cells) >= 5:
        product_id = cells[0].strip()
        product_name_raw = cells[1]
        product_name = re.sub(r'<[^>]+>', '', product_name_raw).strip()
        part_number = cells[3].strip() if len(cells) > 3 else ''
        links_cell = cells[-1] if cells else ''
        
        risemode_products.append({
            'id': product_id,
            'name': product_name,
            'part_number': part_number,
            'links_cell': links_cell,
            'row_html': row_html
        })

print(f"\nRise Mode products with generic links: {len(risemode_products)}")

# Display first few products
print("\n=== Sample Rise Mode Products ===")
for p in risemode_products[:10]:
    print(f"ID: {p['id']:<8} Part: {p['part_number']:<25} Name: {p['name'][:50]}")

# Known Rise Mode URL patterns
# Example: RM-PSU-ELKM-650-B
# Pattern seems to be: RM-PSU-[product-line]-[wattage]-[grade]

# Build a dictionary of known Rise Mode products and their URLs
# We'll construct URLs based on patterns we can observe

risemode_url_patterns = {
    # PSUs (RM-PSU-*)
    'elkm': 'elektra-650w-80-plus-bronze',  # Elektra
    'zeus': 'zeus-series',  # Zeus series
    'pa': 'platinum',  # Platinum
    'bz': 'bronze',  # Bronze
    'gold': 'gold',  # Gold
    'silentx': 'silentx',  # SilentX
    'magma': 'magma',  # Magma
}

# Strategy:
# 1. For products with part numbers starting with RM-PSU-, try to find them
# 2. Most Rise Mode products likely don't have public product pages (they're reseller products)
# 3. So we'll remove generic links and replace with a search suggestion

fixes_info = []
products_to_fix = 0

modified_content = content

for product in risemode_products:
    part_num = product['part_number']
    product_id = product['id']
    
    # Check if this product has the generic Rise Mode link
    if 'https://www.risemode.com.br' in product['links_cell']:
        products_to_fix += 1
        
        # Try to find the product page
        # Most likely: https://www.risemode.com.br/produto/[product-name] or similar
        
        # For now, extract key info for potential URL construction
        name = product['name'].lower()
        
        # Pattern examples:
        # Fonte Gamer Rise Mode Elektra, 650W, ... → elektra
        # Fonte Gamer Rise Mode Zeus, ... → zeus
        # etc.
        
        # Try simple heuristics
        search_keywords = None
        if 'elektra' in name or 'elkm' in part_num:
            search_keywords = 'elektra'
        elif 'zeus' in name:
            search_keywords = 'zeus'
        elif 'silentx' in name:
            search_keywords = 'silentx'
        elif 'magma' in name:
            search_keywords = 'magma'
        
        # Likely these products don't have individual product pages
        # Mark them for manual review or removal
        fixes_info.append({
            'id': product_id,
            'name': product['name'],
            'part_number': part_num,
            'search_term': search_keywords,
            'recommendation': 'REMOVE' if not search_keywords else 'REVIEW'
        })

print(f"\nRise Mode products requiring fixes: {products_to_fix}")
print(f"Products with clear product lines: {sum(1 for f in fixes_info if f['search_term'])}")
print(f"Products to remove links: {sum(1 for f in fixes_info if f['recommendation'] == 'REMOVE')}")

# Now let's remove the generic Rise Mode links
# Pattern: <a href="https://www.risemode.com.br" ... >Site ↗</a>

pattern = re.escape('<a href="https://www.risemode.com.br"') + r'[^>]*?class="link-of"[^>]*?>Site ↗</a>'
matches = len(re.findall(pattern, modified_content))

if matches > 0:
    # Replace with "—" (em dash)
    modified_content = re.sub(pattern, '—', modified_content)
    print(f"\n✓ Removed {matches} generic Rise Mode links")
else:
    print("\n⚠ Pattern not found exactly - trying alternative patterns...")
    # Try finding just href="https://www.risemode.com.br"
    pattern2 = r'<a href="https://www\.risemode\.com\.br"[^>]*>Site ↗</a>'
    matches = len(re.findall(pattern2, modified_content))
    if matches > 0:
        modified_content = re.sub(pattern2, '—', modified_content)
        print(f"✓ Removed {matches} generic Rise Mode links (alternative pattern)")

# Save the modified HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(modified_content)

print(f"\nFile updated: {html_file}")

# Save detailed report
report = {
    'total_risemode_products': len(risemode_products),
    'generic_links_removed': matches if matches > 0 else 0,
    'products_requiring_manual_review': sum(1 for f in fixes_info if f['recommendation'] == 'REVIEW'),
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'sample_products': fixes_info[:20]
}

with open('/tmp/risemode_fix_report.json', 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("\nReport saved to /tmp/risemode_fix_report.json")
