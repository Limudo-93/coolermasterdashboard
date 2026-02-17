#!/usr/bin/env python3
"""
Final improvements for remaining generic manufacturer links
"""

import re
import os

html_file = os.path.expanduser('~/.openclaw/workspace-main/CM_Catalogo_Dashboard.html')

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Check for generic patterns that are still there
generic_urls = {
    'https://www.montech.com.tw': 'MONTECH',
    'https://www.pcyes.com.br': 'PCYES',
    'https://nzxt.com': 'NZXT',  # Generic, some specific ones exist
    'https://lian-li.com': 'Lian Li',  # Generic, some specific ones exist
    'https://www.deepcool.com': 'Deepcool',
    'https://www.arctic.de': 'ARCTIC',
    'https://noctua.at': 'Noctua',
}

print("=== Checking for remaining generic links ===\n")

# Count occurrences of each generic URL
for generic_url, brand in generic_urls.items():
    # Pattern: the URL appears in an href
    pattern = re.escape(generic_url) + r'"'
    matches = len(re.findall(pattern, content))
    
    if matches > 0:
        print(f"{brand:<15} | {matches:>2} occurrences | {generic_url}")

# Now let's remove them intelligently
print("\n=== Applying final fixes ===\n")

# For brands where we should remove all generic links
brands_to_remove_generic = [
    ('MONTECH', 'https://www.montech.com.tw'),
    ('PCYES', 'https://www.pcyes.com.br'),
    ('Deepcool', 'https://www.deepcool.com'),
    ('ARCTIC', 'https://www.arctic.de'),
    ('Noctua', 'https://noctua.at'),
]

removed_count = 0

for brand, generic_url in brands_to_remove_generic:
    # Pattern: <a href="generic_url..." ... >Site ↗</a>
    pattern = re.escape(f'<a href="{generic_url}"') + r'[^>]*?class="link-of"[^>]*?>Site ↗</a>'
    
    matches = len(re.findall(pattern, content))
    
    if matches > 0:
        # Replace with em dash
        content = re.sub(pattern, '—', content)
        removed_count += matches
        print(f"✓ {brand:<15} | Removed {matches} generic links")

# For NZXT: keep generic ones if we can't find specific ones
# Check how many NZXT links are generic vs specific
nzxt_generic = len(re.findall(r'href="https://nzxt\.com"', content))
nzxt_specific = len(re.findall(r'href="https://nzxt\.com/product/', content))

print(f"\n⚠ NZXT: {nzxt_generic} generic + {nzxt_specific} specific links")
print(f"  Note: Some specific NZXT links exist, keeping generic ones for incomplete products")

# For Lian Li: similar situation
lianli_generic = len(re.findall(r'href="https://lian-li\.com"[^/]', content))
lianli_specific = len(re.findall(r'href="https://lian-li\.com/product/', content))

print(f"⚠ Lian Li: {lianli_generic} generic + {lianli_specific} specific links")
print(f"  Note: Some specific Lian Li links exist, keeping generic ones")

# Save the modified content
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== Summary ===")
print(f"Additional generic links removed: {removed_count}")
print(f"Total generic links removed in all phases: {70 + 107 + removed_count} (70+107+{removed_count})")
print(f"\nFile updated: {html_file}")

# Generate final statistics
print("\n=== Final Link Status ===")
all_links = re.findall(r'href="(https://[^"]+)"', content)
kabum_links = len(re.findall(r'href="https://www\.kabum\.com\.br', content))
manufacturer_links = len(all_links) - kabum_links

print(f"Total links: {len(all_links)}")
print(f"KaBuM links: {kabum_links}")
print(f"Manufacturer links: {manufacturer_links}")

# Group manufacturer links by domain
domains = {}
for url in all_links:
    if 'kabum' not in url:
        domain = re.sub(r'https?://([^/]+).*', r'\1', url)
        domains[domain] = domains.get(domain, 0) + 1

print(f"\nManufacturer links by domain:")
for domain in sorted(domains.keys()):
    print(f"  {domain:<30} | {domains[domain]:>3}")
