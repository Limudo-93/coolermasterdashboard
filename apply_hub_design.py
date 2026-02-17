#!/usr/bin/env python3
"""
apply_hub_design.py — Aplica o design do CM_Brasil_Hub.html nos 8 dashboards.
Estratégia:
  1. Copia arquivos ausentes do OneDrive para o workspace
  2. Injeta CSS do Hub (variáveis + tema dark) no início do primeiro <style>
  3. Substitui o header original por um Hub-style nav sticky
  4. Adiciona footer de navegação
  5. Copia arquivo atualizado de volta pro OneDrive
"""

import re, os, shutil

WORKSPACE = "/Users/viniciuslimadalbem/.openclaw/workspace-main"
ONEDRIVE  = "/Users/viniciuslimadalbem/Library/CloudStorage/OneDrive-CoolerMaster/2026/Dashboards"

# ── CM Logo SVG (compact, apenas o ícone circular) ──────────────────────────
CM_LOGO_SVG = (
    '<svg height="28" viewBox="0 0 42 32" xmlns="http://www.w3.org/2000/svg">'
    '<path fill="#ffffff" opacity="0.9" d="'
    'M40.502 12.391v7.782c0 3.929-0.597 5.074-4.199 6.643-1.25 0.541-3.138 1.478'
    '-7.962 3.304-2.124 0.805-5.318 1.881-8.108 1.881-2.776 0-5.969-1.076-8.1-1.881'
    '-4.818-1.826-6.705-2.763-7.955-3.304-3.602-1.569-4.206-2.714-4.206-6.643v-7.782'
    'c0-4.234 1.013-5.914 4.56-7.538 0.729-0.333 1.568-0.75 6.164-2.437'
    ' 5.268-1.936 7.906-2.416 9.537-2.416 1.638 0 4.276 0.479 9.551 2.416'
    ' 4.596 1.687 5.436 2.104 6.164 2.437 3.547 1.625 4.553 3.304 4.553 7.538z'
    '"/></svg>'
)

# ── Hub CSS Design Tokens ────────────────────────────────────────────────────
HUB_CSS = """\
/* ════════════════════════════════════════════
   HUB DESIGN SYSTEM — CM Brasil Intelligence
   Applied by apply_hub_design.py
════════════════════════════════════════════ */

/* Override root variables with Hub tokens */
:root {
  --bg:           #09090b !important;
  --bg-primary:   #09090b !important;
  --bg-secondary: #18181b !important;
  --bg-card:      #18181b !important;
  --bg2:          #18181b !important;
  --bg3:          #1c1c1f !important;
  --surface:      #18181b;
  --surface2:     #1c1c1f;
  --border:       #27272a;
  --border-hover: #3f3f46;
  --text:         #fafafa;
  --text-primary: #fafafa !important;
  --text-2:       #a1a1aa;
  --text-secondary:#a1a1aa !important;
  --text-3:       #71717a;
  --text-muted:   #71717a !important;
  --accent:       #7c3aed;
  --accent-2:     #6d28d9;
  --accent-glow:  rgba(124, 58, 237, 0.12);
  --blue:         #3b82f6;
  --blue-glow:    rgba(59, 130, 246, 0.10);
  --green:        #22c55e;
  --green-dim:    rgba(34, 197, 94, 0.15);
  --yellow:       #eab308;
  --yellow-dim:   rgba(234, 179, 8, 0.15);
  --red:          #ef4444;
  --red-dim:      rgba(239, 68, 68, 0.15);
  --purple-dim:   rgba(124, 58, 237, 0.15);
  --cm-blue:      #7c3aed !important;

  /* Alias overrides for older var names */
  --green-start:  #22c55e !important;
  --blue-start:   #3b82f6 !important;
}

/* Base body */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI',
               Helvetica, Arial, sans-serif !important;
  background: #09090b !important;
  color: #fafafa !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #27272a; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #3f3f46; }

/* ── Hub Top Nav ── */
.hub-nav {
  background: #09090b;
  border-bottom: 1px solid #27272a;
  padding: 0 32px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 9999;
  flex-shrink: 0;
}
.hub-nav-brand { display: flex; align-items: center; gap: 14px; }
.hub-nav-back {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: #71717a;
  text-decoration: none;
  border: 1px solid #27272a;
  border-radius: 6px;
  padding: 4px 10px;
  transition: color 0.15s, border-color 0.15s;
  white-space: nowrap;
}
.hub-nav-back:hover { color: #fafafa; border-color: #3f3f46; }
.hub-nav-sep { width: 1px; height: 26px; background: #27272a; flex-shrink: 0; }
.hub-nav-info {}
.hub-nav-title {
  font-size: 14px;
  font-weight: 650;
  color: #fafafa;
  letter-spacing: -0.25px;
  line-height: 1.2;
}
.hub-nav-sub {
  font-size: 10.5px;
  color: #71717a;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 1px;
}
.hub-nav-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 0 2px rgba(34,197,94,0.2);
  animation: hubnav-pulse 2.5s ease-in-out infinite;
  flex-shrink: 0;
}
@keyframes hubnav-pulse { 0%,100%{opacity:1} 50%{opacity:0.45} }
.hub-nav-clock {
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  color: #71717a;
  font-family: 'Menlo','SF Mono','Consolas',monospace;
  flex-shrink: 0;
}

/* ── Hub Footer ── */
.hub-footer {
  border-top: 1px solid #27272a;
  padding: 20px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 48px;
  font-size: 11.5px;
  color: #52525b;
}
.hub-footer a {
  color: #71717a;
  text-decoration: none;
  transition: color 0.15s;
}
.hub-footer a:hover { color: #fafafa; }
"""

# ── Hub Nav HTML template ────────────────────────────────────────────────────
def make_hub_nav(title: str, subtitle: str) -> str:
    return (
        f'\n<!-- ══ HUB NAV ══ -->\n'
        f'<nav class="hub-nav" id="hub-nav">\n'
        f'  <div class="hub-nav-brand">\n'
        f'    <a href="CM_Brasil_Hub.html" class="hub-nav-back">\n'
        f'      <svg width="12" height="12" viewBox="0 0 24 24" fill="none"'
        f' stroke="currentColor" stroke-width="2" stroke-linecap="round"'
        f' stroke-linejoin="round"><path d="M19 12H5M12 5l-7 7 7 7"/></svg>\n'
        f'      Hub\n'
        f'    </a>\n'
        f'    <div class="hub-nav-sep"></div>\n'
        f'    <div class="hub-nav-info">\n'
        f'      <div class="hub-nav-title">{title}</div>\n'
        f'      <div class="hub-nav-sub"><span class="hub-nav-dot"></span>Cooler Master Brasil</div>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'  <div class="hub-nav-clock" id="hub-nav-clock">--:--:--</div>\n'
        f'</nav>\n'
        f'<script>\n'
        f'(function(){{\n'
        f'  function _hubtick(){{\n'
        f'    var el=document.getElementById("hub-nav-clock");\n'
        f'    if(el) el.textContent=new Date().toLocaleTimeString("pt-BR",{{hour:"2-digit",minute:"2-digit",second:"2-digit"}});\n'
        f'  }}\n'
        f'  _hubtick(); setInterval(_hubtick,1000);\n'
        f'}})();\n'
        f'</script>\n'
        f'<!-- ══ END HUB NAV ══ -->\n'
    )

HUB_FOOTER_HTML = (
    '\n<!-- ══ HUB FOOTER ══ -->\n'
    '<footer class="hub-footer">\n'
    '  <a href="CM_Brasil_Hub.html">← Command Center</a>\n'
    '  <span>CM Brasil Intelligence Platform · Cooler Master</span>\n'
    '</footer>\n'
    '<!-- ══ END HUB FOOTER ══ -->\n'
)

# ── Dashboard definitions ────────────────────────────────────────────────────
DASHBOARDS = [
    ("CM_Brasil_MasterDeck.html",   "MasterDeck",           "Sell-In, Sell-Out, Clientes, Pipeline, Insights"),
    ("CM_Simulador_Precos.html",    "Simulador de Preços",  "FOB→Varejo, FUNDAP, TTD — precificação completa"),
    ("CM_FollowUp_Tracker.html",    "Follow-up Tracker",    "Gestão de follow-ups e oportunidades"),
    ("CM_Catalogo_Dashboard.html",  "Catálogo Brasil",      "207 SKUs ativos · KaBuM × Pichau"),
    ("Organograma_CM.html",         "Organograma",          "Estrutura organizacional Cooler Master Brasil"),
    ("dashboard_sellin.html",       "Dashboard Sell-In",    "Dados de sell-in por canal"),
    ("dashboard_sellout.html",      "Dashboard Sell-Out",   "Performance sell-out KaBuM, Pichau, Terabyte"),
    ("Dashboard_CM_Brasil_2026.html","CM Brasil 2026",      "Planejamento estratégico & KPIs 2026"),
]

# ── CSS injection helper ─────────────────────────────────────────────────────
def inject_hub_css(content: str) -> str:
    """Inject Hub CSS into the first <style> block."""
    # Try to insert right after first <style> opening tag
    m = re.search(r'(<style[^>]*>)', content, re.IGNORECASE)
    if m:
        pos = m.end()
        return content[:pos] + '\n' + HUB_CSS + '\n' + content[pos:]
    # Fallback: inject before </head>
    return content.replace('</head>', f'<style>\n{HUB_CSS}\n</style>\n</head>', 1)

# ── Header removal helpers ───────────────────────────────────────────────────
def hide_original_header(content: str) -> str:
    """Hide original header element by injecting CSS to display:none it."""
    # Inject targeted CSS to hide common header patterns
    hide_css = (
        "\n/* Hide original header — replaced by Hub nav */\n"
        ".header:not(.hub-nav) { display: none !important; }\n"
        "header:not(.hub-nav) { display: none !important; }\n"
        "#header { display: none !important; }\n"
        ".topbar:not(.hub-nav) { display: none !important; }\n"
        ".navbar:not(.hub-nav) { display: none !important; }\n"
        ".top-bar:not(.hub-nav) { display: none !important; }\n"
    )
    # Add after the Hub CSS injection (which is inside first <style>)
    # Find end of first </style>
    m = re.search(r'</style>', content, re.IGNORECASE)
    if m:
        pos = m.start()
        return content[:pos] + hide_css + '\n' + content[pos:]
    return content

def inject_hub_nav(content: str, title: str, subtitle: str) -> str:
    """Inject Hub nav right after <body> opening tag."""
    hub_nav = make_hub_nav(title, subtitle)
    # Match <body> with optional attributes
    new_content = re.sub(
        r'(<body[^>]*>)',
        r'\1' + hub_nav,
        content,
        count=1,
        flags=re.IGNORECASE
    )
    return new_content

def inject_hub_footer(content: str) -> str:
    """Inject Hub footer before </body>."""
    return content.replace('</body>', HUB_FOOTER_HTML + '\n</body>', 1)

def already_has_hub(content: str) -> bool:
    return 'hub-nav' in content or 'HUB DESIGN SYSTEM' in content

# ── Main ─────────────────────────────────────────────────────────────────────
results = []

for filename, title, subtitle in DASHBOARDS:
    filepath = os.path.join(WORKSPACE, filename)

    # Copy from OneDrive if not in workspace
    if not os.path.exists(filepath):
        od_src = os.path.join(ONEDRIVE, filename)
        if os.path.exists(od_src):
            shutil.copy2(od_src, filepath)
            print(f"📥  Copied {filename} from OneDrive")
        else:
            print(f"⚠️  SKIP: {filename} not found anywhere")
            results.append((filename, False, "NOT FOUND"))
            continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_size = len(content)

    if already_has_hub(content):
        print(f"⏭️  {filename} already has Hub design — skipping CSS/nav injection")
    else:
        content = inject_hub_css(content)
        content = hide_original_header(content)
        content = inject_hub_nav(content, title, subtitle)
        content = inject_hub_footer(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    new_size = len(content)

    # Copy to OneDrive
    od_dest = os.path.join(ONEDRIVE, filename)
    shutil.copy2(filepath, od_dest)

    delta = new_size - orig_size
    print(f"✅  {filename:42s}  +{delta:,} bytes → OneDrive ✓")
    results.append((filename, True, f"+{delta:,} bytes"))

print(f"\n{'='*60}")
print(f"Done: {sum(1 for _,ok,_ in results if ok)}/{len(DASHBOARDS)} dashboards updated")
for fname, ok, note in results:
    icon = "✅" if ok else "⚠️"
    print(f"  {icon}  {fname}: {note}")
