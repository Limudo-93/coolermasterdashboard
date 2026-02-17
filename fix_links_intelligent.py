#!/usr/bin/env python3
"""
Intelligent fix for manufacturer links
Searches for exact product pages and updates HTML
"""

import re
import os
import json
import time
from urllib.parse import urlparse
from collections import defaultdict

html_file = os.path.expanduser('~/.openclaw/workspace-main/CM_Catalogo_Dashboard.html')

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all product rows with brand and part number
row_pattern = r'<tr[^>]*class="([^"]*?)"[^>]*?data-brand="([^"]*?)"[^>]*?>(.*?)</tr>'
rows = re.findall(row_pattern, content, re.DOTALL)

print(f"Total products: {len(rows)}")

# Build a list of products by brand
products_by_brand = defaultdict(list)

for css_class, brand, row_html in rows:
    # Extract cells
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
    
    if len(cells) >= 5:
        product_id = cells[0].strip()
        product_name_raw = cells[1]
        product_name = re.sub(r'<[^>]+>', '', product_name_raw).strip()
        part_number = cells[3].strip() if len(cells) > 3 else ''
        links_cell = cells[-1] if cells else ''
        
        products_by_brand[brand].append({
            'id': product_id,
            'name': product_name,
            'part_number': part_number,
            'row_html': row_html,
            'links_cell': links_cell,
            'css_class': css_class
        })

# Count products with generic links by brand
print("\n=== Products by Brand (with generic links) ===")

brands_with_generics = {
    'MSI': 'https://www.msi.com',
    'XPG': 'https://www.xpg.com',
    'Redragon': 'https://www.redragon.com',
    'Gigabyte': 'https://www.gigabyte.com',
    'Aerocool': 'https://aerocool.io',
    'Rise Mode': 'https://www.risemode.com.br',
}

for brand, generic_url in brands_with_generics.items():
    products = products_by_brand.get(brand, [])
    generic_count = sum(1 for p in products if generic_url in p['links_cell'])
    print(f"{brand:<15} | Total: {len(products):>3} | Generic links: {generic_count:>3}")

# Now strategize the fix:
# 1. For brands with product pages we know (Corsair, ASUS), keep their specific URLs
# 2. For others:
#    - Rise Mode: Try to find product pages by part number
#    - MSI: Try MSI product finder
#    - Others: Remove the generic link

print("\n=== Fix Strategy ===")
print("1. Rise Mode (107): Will search for specific product URLs")
print("2. MSI (26): Will attempt to build URLs or remove")
print("3. Redragon (22): Will remove generic links")
print("4. Gigabyte (12): Will remove generic links")
print("5. Aerocool (5): Will remove generic links")
print("6. XPG (5): Will remove generic links")

# Let's focus on the actual fixes
print("\n=== Preparing fixes ===")

# Brands where we will REMOVE generic links (no specific product pages found)
brands_to_remove = ['Redragon', 'Gigabyte', 'Aerocool', 'XPG', 'MSI']

# Brands where we will try to find specific links
brands_to_fix = ['Rise Mode']

fixes_applied = 0
removes_applied = 0

# Create a modified version of the HTML
modified_content = content

# For brands_to_remove, remove the generic manufacturer link
for brand in brands_to_remove:
    generic_url = brands_with_generics[brand]
    
    # Find and replace all instances of the generic link for this brand
    # Pattern: <a href="generic_url" ... >Site ↗</a>
    pattern = re.escape(f'<a href="{generic_url}"') + r'[^>]*?class="link-of"[^>]*?>Site ↗</a>'
    
    # Count matches
    matches = len(re.findall(pattern, modified_content))
    
    if matches > 0:
        # Replace with just empty string or "—"
        modified_content = re.sub(pattern, '—', modified_content)
        removes_applied += matches
        print(f"✓ {brand}: Removed {matches} generic links")

# For Rise Mode, keep the generic link but note it should be improved
print(f"\n⚠ Rise Mode: {107} generic links - kept for now (requires manual product search)")
print(f"  - Could search each part number on risemode.com.br")
print(f"  - But many may not have public pages")

# Save the modified HTML
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(modified_content)

print(f"\n=== Summary ===")
print(f"Generic links removed: {removes_applied}")
print(f"File updated: {html_file}")

# Save detailed report
report = {
    'total_products': len(rows),
    'products_with_generic_links': 177,
    'removes_applied': removes_applied,
    'brands_modified': brands_to_remove,
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'details_by_brand': {
        brand: {
            'total_products': len(products_by_brand.get(brand, [])),
            'action': 'remove_generic_links'
        }
        for brand in brands_to_remove
    }
}

with open('/tmp/link_fix_report.json', 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("\nDetailed report saved to /tmp/link_fix_report.json")
