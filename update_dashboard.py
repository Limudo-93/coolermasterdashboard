#!/usr/bin/env python3
"""
Update CM_Catalogo_Dashboard.html with fresh stock data from all 3 stores.
Updates:
1. Multilojas table (prodCMTable) - add stock columns for all stores  
2. Per-store stock tables (Pichau/KaBuM/Terabyte tabs)
3. Terabyte capped stock shows ≥X
"""
import csv, json, re, os
from pathlib import Path
from collections import defaultdict

BASE = Path(os.path.expanduser("~/.openclaw"))
WORKSPACE = BASE / "workspace-main"
PESQUISA = BASE / "workspace-pesquisa"

HTML_PATH = WORKSPACE / "CM_Catalogo_Dashboard.html"
PICHAU_CSV = PESQUISA / "pichau-scraper" / "pichau_estoque.csv"
KABUM_CSV = PESQUISA / "kabum-scraper" / "kabum_estoque.csv"
TERA_CSV = PESQUISA / "terabyte-scraper" / "terabyte_estoque.csv"

def read_csv(path, encoding="utf-8-sig"):
    with open(path, encoding=encoding) as f:
        return list(csv.DictReader(f))

def norm_mpn(s):
    """Normalize MPN for matching."""
    return re.sub(r'[\s\-_]', '', s.strip().upper()) if s else ""

def fmt_price(val):
    try:
        v = float(val)
        return f"R${v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except:
        return "—"

def fmt_qty(qty, status=""):
    try:
        q = int(float(qty))
    except:
        return "—"
    if status == "in_stock_capped":
        return f"≥{q}"
    return str(q)

# ─── Load data ───
print("Loading data...")
pichau = read_csv(PICHAU_CSV)
kabum = read_csv(KABUM_CSV)
tera = read_csv(TERA_CSV)

# Build MPN indexes
pichau_by_mpn = {}
for r in pichau:
    mpn = norm_mpn(r.get("sku", ""))
    if mpn:
        pichau_by_mpn[mpn] = r

kabum_by_mpn = {}
for r in kabum:
    mpn = norm_mpn(r.get("mpn", ""))
    if mpn:
        kabum_by_mpn[mpn] = r
    # Also try extracting from name
    nome = r.get("nome", "")
    m = re.search(r'[-–]\s*([A-Z0-9][\w\-]{5,25})\s*$', nome)
    if m:
        k = norm_mpn(m.group(1))
        if k and k not in kabum_by_mpn:
            kabum_by_mpn[k] = r

tera_by_mpn = {}
for r in tera:
    mpn = norm_mpn(r.get("mpn", ""))
    if mpn:
        tera_by_mpn[mpn] = r

print(f"Pichau: {len(pichau)} rows, {len(pichau_by_mpn)} MPNs")
print(f"KaBuM:  {len(kabum)} rows, {len(kabum_by_mpn)} MPNs") 
print(f"Tera:   {len(tera)} rows, {len(tera_by_mpn)} MPNs")

# ─── Collect all unique CM products by MPN ───
all_mpns = set()
all_mpns.update(pichau_by_mpn.keys())
all_mpns.update(kabum_by_mpn.keys())
all_mpns.update(tera_by_mpn.keys())

print(f"Unique MPNs across all stores: {len(all_mpns)}")

# Build unified product list
products = []
for mpn in sorted(all_mpns):
    p = pichau_by_mpn.get(mpn, {})
    k = kabum_by_mpn.get(mpn, {})
    t = tera_by_mpn.get(mpn, {})
    
    # Best name
    name = p.get("nome", "") or k.get("nome", "") or t.get("nome", "")
    # Shorten name
    short = re.sub(r'^(Fonte|Gabinete|Cooler|Water Cooler|Kit|Teclado|Headset|Pasta|Stream|Combo|Air Cooler|Ventoinha)\s+(Gamer\s+)?(Cooler Master|Para Processador Cooler Master|Cooler Master)\s+', '', name).strip()
    short = re.sub(r',\s*(Cooler Master|Preto|Black|Branco|White|RGB|ARGB|Mid.Tower|Mini.Tower|Full.Tower|ATX|mATX|Mini.ITX|E.ATX|Vidro Temperado|Lateral de Vidro|Sem Fonte|PFC Ativo|80 Plus \w+|Com \d+ Fan\w*)\s*', ' ', short)
    short = re.sub(r'\s+', ' ', short).strip()[:60]
    
    # Category
    cat = p.get("categoria", "") or t.get("categoria_principal", "") or k.get("categoria", "")
    cat = cat.lower().replace("fontes","Fontes").replace("gabinetes","Gabinetes").replace("coolers","Coolers").replace("perifericos","Periféricos")
    if not cat:
        if any(x in name.lower() for x in ["fonte","power","psu"]): cat = "Fontes"
        elif any(x in name.lower() for x in ["gabinete","case","tower"]): cat = "Gabinetes"
        elif any(x in name.lower() for x in ["cooler","fan","water","pasta","thermal","gel","cryofuze"]): cat = "Coolers"
        else: cat = "Periféricos"
    
    # Denormalize MPN for display
    display_mpn = p.get("sku","") or t.get("mpn","") or k.get("mpn","") or mpn
    
    # Prices
    p_price = p.get("preco_brl","") if p else ""
    k_price = k.get("preco","") if k else ""
    t_price = t.get("preco_atual","") if t else ""
    
    # Stock
    p_stock = p.get("estoque_cart","") if p else ""
    p_avail = p.get("disponivel","") == "True" if p else False
    k_stock = k.get("stock","") if k else ""
    k_avail = k.get("available","") == "True" if k else False
    t_stock = t.get("estoque_qty","") if t else ""
    t_status = t.get("estoque_status","") if t else ""
    t_avail = t_status in ("in_stock","in_stock_capped") if t else False
    
    # Count stores available
    stores = 0
    if p_avail and p_stock and int(float(p_stock)) > 0: stores += 1
    if k_avail and k_stock and int(float(k_stock)) > 0: stores += 1
    if t_avail: stores += 1
    
    # Best price
    prices = []
    if p_avail and p_price:
        try: prices.append(("Pichau", float(p_price)))
        except: pass
    if k_avail and k_price:
        try: prices.append(("KaBuM", float(k_price)))
        except: pass
    if t_avail and t_price:
        try: prices.append(("Terabyte", float(t_price)))
        except: pass
    
    best = min(prices, key=lambda x: x[1]) if prices else None
    
    products.append({
        "mpn": display_mpn,
        "mpn_norm": mpn,
        "name": short,
        "full_name": name,
        "cat": cat,
        "p_price": p_price, "p_stock": p_stock, "p_avail": p_avail,
        "k_price": k_price, "k_stock": k_stock, "k_avail": k_avail,
        "t_price": t_price, "t_stock": t_stock, "t_status": t_status, "t_avail": t_avail,
        "stores": stores,
        "best": best,
        "p_url": p.get("url","") if p else "",
        "k_url": k.get("url","") if k else "",
        "t_url": t.get("url_produto","") if t else "",
    })

# Sort: most stores first, then by best price
products.sort(key=lambda x: (-x["stores"], x["best"][1] if x["best"] else 99999))

# Count categories per store
cat_counts = {"Fontes": {"k":0,"p":0,"t":0}, "Gabinetes": {"k":0,"p":0,"t":0}, "Coolers": {"k":0,"p":0,"t":0}, "Periféricos": {"k":0,"p":0,"t":0}}
for pr in products:
    c = pr["cat"] if pr["cat"] in cat_counts else "Periféricos"
    if pr["k_avail"]: cat_counts[c]["k"] += 1
    if pr["p_avail"]: cat_counts[c]["p"] += 1
    if pr["t_avail"]: cat_counts[c]["t"] += 1

print(f"\nProducts for multilojas table: {len(products)}")
avail_products = [p for p in products if p["stores"] > 0]
print(f"Available in at least 1 store: {len(avail_products)}")

# ─── Generate HTML sections ───

def cell_price_stock(price, stock, status, avail, color, url=""):
    """Generate a table cell with price and stock info."""
    if not avail or not price:
        return f'<td style="color:#71717a">—</td>'
    
    p_fmt = fmt_price(price)
    s_fmt = fmt_qty(stock, status)
    
    link = ""
    if url:
        link = f' <a href="{url}" target="_blank" style="color:{color};font-size:.7rem;text-decoration:none">↗</a>'
    
    return f'<td style="color:{color}">{p_fmt} <span style="font-size:.75em;opacity:.7">({s_fmt})</span>{link}</td>'

# ─── Multilojas Table ───
def gen_multilojas_table():
    rows = []
    for pr in avail_products:
        mpn = pr["mpn"]
        name = pr["name"]
        cat = pr["cat"]
        
        # Badge color
        badge_map = {"Fontes":"badge-yellow","Gabinetes":"badge-green","Coolers":"badge-blue","Periféricos":"badge-purple"}
        badge_short = {"Fontes":"Fonte","Gabinetes":"Gab","Coolers":"Cool","Periféricos":"Peri"}
        badge = badge_map.get(cat, "badge-purple")
        bshort = badge_short.get(cat, cat[:4])
        
        # KaBuM cell
        k_cell = cell_price_stock(pr["k_price"], pr["k_stock"], "", pr["k_avail"], "#0066CC", pr["k_url"])
        # Pichau cell
        p_cell = cell_price_stock(pr["p_price"], pr["p_stock"], "", pr["p_avail"], "#E31E24", pr["p_url"])
        # Terabyte cell
        t_cell = cell_price_stock(pr["t_price"], pr["t_stock"], pr["t_status"], pr["t_avail"], "#FF6600", pr["t_url"])
        
        # Best price
        if pr["best"]:
            best_store, best_price = pr["best"]
            best_html = f'<strong style="color:#22c55e">{fmt_price(best_price)}</strong> <span style="font-size:.75em;color:var(--text-3)">{best_store}</span>'
        else:
            best_html = '<span style="color:#71717a">—</span>'
        
        # Coverage badge
        s = pr["stores"]
        if s == 3:
            cov = '<span class="badge badge-green">3/3 lojas</span>'
        elif s == 2:
            cov = '<span class="badge badge-yellow">2/3 lojas</span>'
        elif s == 1:
            # Which store?
            store = ""
            if pr["k_avail"]: store = "KaBuM"
            elif pr["p_avail"]: store = "Pichau"
            elif pr["t_avail"]: store = "Terabyte"
            cov = f'<span class="badge badge-red">1/3 ({store})</span>'
        else:
            cov = '<span class="badge" style="background:var(--border)">0/3</span>'
        
        row = f'''        <tr>
          <td>{name}</td>
          <td style="font-family:monospace;font-size:.78rem;color:var(--text-3)">{mpn}</td>
          <td><span class="badge {badge}">{bshort}</span></td>
          {k_cell}
          {p_cell}
          {t_cell}
          <td>{best_html}</td>
          <td>{cov}</td>
        </tr>'''
        rows.append(row)
    
    return "\n".join(rows)

# ─── Category coverage section ───  
def gen_cat_coverage():
    cats_data = [
        ("⚡ Fontes", "Fontes"),
        ("🖥️ Gabinetes", "Gabinetes"), 
        ("❄️ Coolers", "Coolers"),
        ("🖱️ Periféricos", "Periféricos"),
    ]
    items = []
    for label, cat in cats_data:
        c = cat_counts.get(cat, {"k":0,"p":0,"t":0})
        items.append(f'''    <div class="stat-row">
      <span class="stat-label">{label}</span>
      <div style="display:flex;gap:16px;align-items:center">
        <div style="text-align:center"><div style="color:#0066CC;font-size:1.4rem;font-weight:700">{c["k"]}</div><div style="font-size:.7rem;color:#71717a">KaBuM</div></div>
        <div style="text-align:center"><div style="color:#E31E24;font-size:1.4rem;font-weight:700">{c["p"]}</div><div style="font-size:.7rem;color:#71717a">Pichau</div></div>
        <div style="text-align:center"><div style="color:#FF6600;font-size:1.4rem;font-weight:700">{c["t"]}</div><div style="font-size:.7rem;color:#71717a">Terabyte</div></div>
      </div>
    </div>''')
    return "\n".join(items)

# ─── Per-store stock table rows ───
def gen_store_table(store):
    if store == "pichau":
        data = sorted(pichau, key=lambda x: -int(x.get("estoque_cart",0) or 0))
        color = "#E31E24"
    elif store == "kabum":
        data = sorted([r for r in kabum if r.get("available","")=="True" and int(float(r.get("stock",0) or 0))>0], 
                       key=lambda x: -int(float(x.get("stock",0) or 0)))
        color = "#0066CC"
    else:
        data = sorted([r for r in tera if r.get("estoque_status","") in ("in_stock","in_stock_capped")],
                       key=lambda x: -int(x.get("estoque_qty",0) or 0))
        color = "#FF6600"
    
    rows = []
    for i, r in enumerate(data, 1):
        if store == "pichau":
            mpn = r.get("sku","")
            nome = r.get("nome","")
            # Shorten
            nome = re.sub(r'^(Fonte|Gabinete|Cooler|Water Cooler|Kit|Teclado|Headset|Pasta|Stream|Combo)\s+(Gamer\s+)?(Cooler Master|Para Processador Cooler Master|Cooler Master)\s+', '', nome).strip()
            nome = nome[:50]
            cat_raw = r.get("categoria","")
            qty = r.get("estoque_cart","")
            price = fmt_price(r.get("preco_brl",""))
            url = r.get("url","")
            status = ""
        elif store == "kabum":
            mpn = r.get("mpn","") or ""
            nome = r.get("nome","")
            nome = re.sub(r'^(Fonte|Gabinete|Cooler|Air Cooler|Water Cooler|Ventoinha|Kit|Teclado|Headset|Pasta|Stream|Combo)\s+(Gamer\s+)?(Cooler Master|Para Processador Cooler Master)\s*,?\s*', '', nome).strip()
            nome = re.sub(r'\s*-\s*[A-Z0-9][\w\-]{5,25}\s*$', '', nome).strip()[:50]
            cat_raw = r.get("categoria","")
            qty = str(int(float(r.get("stock","0"))))
            price = fmt_price(r.get("preco",""))
            url = r.get("url","")
            status = ""
        else:
            mpn = r.get("mpn","")
            nome = r.get("nome","")
            nome = re.sub(r'^(Fonte|Gabinete|Cooler|Water Cooler|Kit|Teclado|Headset|Pasta|Stream|Combo)\s+(Gamer\s+)?(Cooler Master|Para Processador Cooler Master|Cooler Master)\s+', '', nome).strip()
            nome = nome[:50]
            cat_raw = r.get("categoria_principal","")
            qty_raw = r.get("estoque_qty","")
            status = r.get("estoque_status","")
            qty = fmt_qty(qty_raw, status)
            price = fmt_price(r.get("preco_atual",""))
            url = r.get("url_produto","")
        
        # Category badge
        cat_lower = cat_raw.lower()
        if "fonte" in cat_lower: badge, bshort, data_cat = "badge-yellow", "Fonte", "fontes"
        elif "gabinete" in cat_lower: badge, bshort, data_cat = "badge-green", "Gab", "gabinetes"
        elif "cooler" in cat_lower or "thermal" in cat_lower: badge, bshort, data_cat = "badge-blue", "Cool", "coolers"
        else: badge, bshort, data_cat = "badge-purple", "Peri", "perifericos"
        
        qty_display = qty if store != "pichau" and store != "kabum" else qty
        qty_style = f"color:{color}" if status != "in_stock_capped" else f"color:{color};font-style:italic"
        
        row = f'            <tr data-cat="{data_cat}"><td>{i}</td><td style="font-family:monospace;font-size:.78rem;color:var(--text-3)">{mpn}</td><td>{nome}</td><td><span class="badge {badge}">{bshort}</span></td><td style="text-align:right;font-weight:700;font-size:1rem;{qty_style}">{qty_display}</td><td style="text-align:right;color:#22c55e;font-weight:600">{price}</td><td><a href="{url}" target="_blank" style="color:{color};font-size:.8rem">↗</a></td></tr>'
        rows.append(row)
    
    return "\n".join(rows), len(data)

# ─── Build replacement sections ───
print("Generating HTML sections...")

multilojas_rows = gen_multilojas_table()
cat_cov = gen_cat_coverage()
pichau_rows, pichau_count = gen_store_table("pichau")
kabum_rows, kabum_count = gen_store_table("kabum")
tera_rows, tera_count = gen_store_table("terabyte")

# Pichau total stock
pichau_total_stock = sum(int(r.get("estoque_cart",0) or 0) for r in pichau)
# KaBuM total stock  
kabum_total_stock = sum(int(float(r.get("stock",0) or 0)) for r in kabum if r.get("available","")=="True")
# Terabyte total stock (sum of capped = minimum)
tera_total_stock = sum(int(r.get("estoque_qty",0) or 0) for r in tera if r.get("estoque_status","") in ("in_stock","in_stock_capped"))
tera_capped = sum(1 for r in tera if r.get("estoque_status","") == "in_stock_capped")

print(f"Pichau: {pichau_count} SKUs, {pichau_total_stock} units")
print(f"KaBuM: {kabum_count} SKUs, {kabum_total_stock} units") 
print(f"Terabyte: {tera_count} SKUs, ≥{tera_total_stock} units ({tera_capped} capped)")

# ─── Read and update HTML ───
print("\nReading HTML...")
html = open(HTML_PATH, encoding="utf-8").read()

# 1. Replace multilojas table tbody
old_tbody = re.search(
    r'(<table id="prodCMTable".*?<thead>.*?</thead>\s*<tbody>)(.*?)(</tbody>\s*</table>)',
    html, re.DOTALL
)
if old_tbody:
    html = html[:old_tbody.start(2)] + "\n" + multilojas_rows + "\n      " + html[old_tbody.end(2):]
    print("✅ Updated multilojas table")

    # Also update the header columns
    old_header = re.search(r'(<table id="prodCMTable".*?<thead>\s*<tr>)(.*?)(</tr>\s*</thead>)', html, re.DOTALL)
    if old_header:
        new_header = """
          <th>Produto CM</th>
          <th>MPN/SKU</th>
          <th>Cat.</th>
          <th style="color:#0066CC">KaBuM (qty)</th>
          <th style="color:#E31E24">Pichau (qty)</th>
          <th style="color:#FF6600">Terabyte (qty)</th>
          <th>Menor Preço</th>
          <th>Cobertura</th>
        """
        html = html[:old_header.start(2)] + new_header + html[old_header.end(2):]
        print("✅ Updated multilojas header")
else:
    print("❌ Could not find multilojas table")

# 2. Replace category coverage stats
# Find the stat-row divs for categories
for cat_label, cat_key in [("⚡ Fontes","Fontes"),("🖥️ Gabinetes","Gabinetes"),("❄️ Coolers","Coolers"),("🖱️ Periféricos","Periféricos")]:
    c = cat_counts.get(cat_key, {"k":0,"p":0,"t":0})
    # Find the stat-row that contains this category label and update the store counts
    pattern = re.escape(cat_label) + r'.*?</div>\s*</div>'
    # This is complex to do with regex on the existing structure. Skip for now.

# 3. Replace Pichau stock table body  
old_pichau = re.search(r'(<tbody id="pichauStockBody">)(.*?)(</tbody>)', html, re.DOTALL)
if old_pichau:
    html = html[:old_pichau.start(2)] + "\n" + pichau_rows + "\n          " + html[old_pichau.end(2):]
    print("✅ Updated Pichau stock table")

# 4. Replace KaBuM stock table body
old_kabum = re.search(r'(<table id="kabumStockTable">.*?<tbody>)(.*?)(</tbody>)', html, re.DOTALL)
if old_kabum:
    html = html[:old_kabum.start(2)] + "\n" + kabum_rows + "\n          " + html[old_kabum.end(2):]
    print("✅ Updated KaBuM stock table")

# Update KaBuM tab label
html = re.sub(
    r'(id="stab-kabum".*?KaBuM &nbsp;<span[^>]*>)[^<]*(</span>)',
    rf'\g<1>{kabum_count} SKUs · {kabum_total_stock:,} un\2',
    html
)

# 5. Replace Terabyte stock table body
old_tera = re.search(r'(<tbody id="terabyteStockBody">)(.*?)(</tbody>)', html, re.DOTALL)
if old_tera:
    html = html[:old_tera.start(2)] + "\n" + tera_rows + "\n          " + html[old_tera.end(2):]
    print("✅ Updated Terabyte stock table")

# Update Terabyte tab label
html = re.sub(
    r'(id="stab-terabyte".*?Terabyte &nbsp;<span[^>]*>)[^<]*(</span>)',
    rf'\g<1>{tera_count} SKUs · ≥{tera_total_stock} un ({tera_capped} capped)\2',
    html
)

# Update Pichau tab label
html = re.sub(
    r'(id="stab-pichau".*?Pichau &nbsp;<span[^>]*>)[^<]*(</span>)',
    rf'\g<1>{pichau_count} SKUs · {pichau_total_stock:,} un\2',
    html
)

# 6. Update KPI cards for store counts  
# Update "CM no KaBuM" KPI
kabum_in_stock = sum(1 for r in kabum if r.get("available","")=="True" and int(float(r.get("stock",0) or 0))>0)
html = re.sub(
    r'(CM no KaBuM.*?<div class="kpi-value[^"]*">)\d+',
    rf'\g<1>{kabum_count}',
    html, count=1
)

# ─── Save ───
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\n✅ Dashboard saved: {HTML_PATH}")
print(f"   {len(html):,} chars, ~{len(html.splitlines())} lines")
