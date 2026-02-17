#!/usr/bin/env python3
"""
hub_rewrite_fix.py — Fix files where tabs were inside the removed .header div.
Specifically: CM_Brasil_MasterDeck.html and CM_Simulador_Precos.html
"""

import re, os, shutil

WORKSPACE = os.path.expanduser("~/.openclaw/workspace-main")
ONEDRIVE  = os.path.expanduser("~/Library/CloudStorage/OneDrive-CoolerMaster/2026/Dashboards")

def extract_div_by_class(html, class_name):
    """Extract first <div class="CLASS"> and return (html_without_div, extracted_div)."""
    pat = rf'<div\s+class="{class_name}"'
    m = re.search(pat, html)
    if not m:
        return html, ''
    
    start = m.start()
    pos = start
    depth = 0
    while pos < len(html):
        op = re.search(r'<div', html[pos:])
        cl = re.search(r'</div>', html[pos:])
        if op is None and cl is None:
            break
        op_pos = op.start() + pos if op else len(html)
        cl_pos = cl.start() + pos if cl else len(html)
        if op_pos < cl_pos:
            depth += 1; pos = op_pos + 4
        else:
            depth -= 1
            end = cl_pos + 6
            if depth == 0:
                return html[:start] + html[end:], html[start:end]
            pos = cl_pos + 6
    return html, ''

def extract_inner_div(outer_html, inner_class):
    """Extract a <div class="INNER"> from within outer_html."""
    pat = rf'<div\s+(?:role="[^"]*"\s+)?class="{inner_class}"|<div\s+class="{inner_class}"'
    m = re.search(pat, outer_html)
    if not m:
        return ''
    
    start = m.start()
    pos = start
    depth = 0
    while pos < len(outer_html):
        op = re.search(r'<div', outer_html[pos:])
        cl = re.search(r'</div>', outer_html[pos:])
        if op is None and cl is None:
            break
        op_pos = op.start() + pos if op else len(outer_html)
        cl_pos = cl.start() + pos if cl else len(outer_html)
        if op_pos < cl_pos:
            depth += 1; pos = op_pos + 4
        else:
            depth -= 1
            end = cl_pos + 6
            if depth == 0:
                return outer_html[start:end]
            pos = cl_pos + 6
    return ''

def fix_file(filepath, tabs_html, tab_wrapper_css=''):
    """Insert the tabs HTML into the page-body, right after the hub-header."""
    with open(filepath, encoding='utf-8') as f:
        html = f.read()
    
    # Find the page-body div opening
    m = re.search(r'<div class="page-body">\s*\n', html)
    if not m:
        print(f"  ✗ Could not find page-body in {os.path.basename(filepath)}")
        return False
    
    # Build the tabs nav bar
    tabs_nav = f'''
<!-- ══ TAB NAV BAR ══ -->
<nav class="tab-nav-bar">
  {tabs_html.strip()}
</nav>
<!-- ══ END TAB NAV BAR ══ -->

'''
    
    # Insert tabs after page-body opening
    insert_pos = m.end()
    new_html = html[:insert_pos] + tabs_nav + html[insert_pos:]
    
    # Also add CSS for the tab nav bar if not present
    # Insert before </style>
    if 'tab-nav-bar' not in html:
        tab_bar_css = '''
    /* ─── Sticky Tab Nav Bar ─── */
    .tab-nav-bar {
      position: sticky;
      top: 72px;
      z-index: 100;
      background: var(--bg);
      border-bottom: 1px solid var(--border);
      padding: 0;
      margin-bottom: 28px;
    }
    .tab-nav-bar .tabs {
      display: flex;
      gap: 0;
      max-width: 1400px;
      margin: 0;
      padding: 8px 0 0;
      border-bottom: none;
      overflow-x: auto;
    }
''' + tab_wrapper_css
        new_html = new_html.replace('</style>', tab_bar_css + '\n  </style>', 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"  ✓ Fixed: {os.path.basename(filepath)}")
    return True


def main():
    print("Hub Rewrite Fix — Restoring tabs to MasterDeck and Simulador")
    
    # ── MasterDeck ──
    backup_md = os.path.join(WORKSPACE, '.backup_before_rewrite', 'CM_Brasil_MasterDeck.html')
    md_path = os.path.join(WORKSPACE, 'CM_Brasil_MasterDeck.html')
    
    print(f"\n{'─'*60}")
    print("  Fixing: CM_Brasil_MasterDeck.html")
    
    with open(backup_md, encoding='utf-8') as f:
        md_backup = f.read()
    
    # Extract the header div from backup
    _, md_header = extract_div_by_class(md_backup, 'header')
    # Extract the tabs div from within the header
    md_tabs = extract_inner_div(md_header, 'tabs')
    
    if md_tabs:
        print(f"  Found tabs: {md_tabs[:100]}...")
        fix_file(md_path, md_tabs)
    else:
        print("  ✗ Could not find tabs in backup")
    
    # ── Simulador ──
    backup_sim = os.path.join(WORKSPACE, '.backup_before_rewrite', 'CM_Simulador_Precos.html')
    sim_path = os.path.join(WORKSPACE, 'CM_Simulador_Precos.html')
    
    print(f"\n{'─'*60}")
    print("  Fixing: CM_Simulador_Precos.html")
    
    with open(backup_sim, encoding='utf-8') as f:
        sim_backup = f.read()
    
    _, sim_header = extract_div_by_class(sim_backup, 'header')
    sim_tabs = extract_inner_div(sim_header, 'tabs')
    
    if sim_tabs:
        print(f"  Found tabs: {sim_tabs[:100]}...")
        fix_file(sim_path, sim_tabs)
    else:
        print("  ✗ Could not find tabs in backup")
    
    # ── Also check Forecast and Playbook ──
    for fname in ['CM_Forecast_Dashboard.html', 'CM_Playbook_Processos.html', 'CM_Catalogo_Dashboard.html']:
        backup_path = os.path.join(WORKSPACE, '.backup_before_rewrite', fname)
        curr_path = os.path.join(WORKSPACE, fname)
        
        print(f"\n{'─'*60}")
        print(f"  Checking: {fname}")
        
        with open(backup_path, encoding='utf-8') as f:
            backup_html = f.read()
        
        _, header_div = extract_div_by_class(backup_html, 'header')
        if header_div and '<div class="tabs"' in header_div:
            tabs_div = extract_inner_div(header_div, 'tabs')
            print(f"  Has tabs in header — fixing...")
            fix_file(curr_path, tabs_div)
        else:
            print(f"  No tabs in header — OK")
    
    # ── Copy fixed files to OneDrive ──
    print(f"\n{'─'*60}")
    print("Copying to OneDrive...")
    os.makedirs(ONEDRIVE, exist_ok=True)
    for fname in [
        'CM_Brasil_MasterDeck.html',
        'CM_Simulador_Precos.html',
        'CM_Forecast_Dashboard.html',
        'CM_Playbook_Processos.html',
        'CM_Catalogo_Dashboard.html',
    ]:
        src = os.path.join(WORKSPACE, fname)
        dst = os.path.join(ONEDRIVE, fname)
        try:
            shutil.copy2(src, dst)
            print(f"  ✓ {fname}")
        except Exception as e:
            print(f"  ✗ {fname}: {e}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
