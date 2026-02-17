#!/usr/bin/env python3
"""
Transform all CM Brasil dashboards to match CM_Brasil_Hub.html design.
Preserves all functionality (charts, tabs, filters, search, JS).
Applies Hub palette, CM logo header, Jubinha AI footer.
"""
import re, os

WS = "/Users/viniciuslimadalbem/.openclaw/workspace-main"

# ── Cooler Master SVG logo (white, same as Hub) ─────────────
CM_SVG = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="124" height="32" viewBox="0 0 124 32"><path fill="#ffffff" d="M61.768 12.164v1.437h-0.614v5.007h0.614v1.437h-3.083v-1.437h0.626v-3.153h-0.023l-1.658 4.59h-1.17l-1.797-4.59h-0.023v3.153h0.672v1.437h-2.99v-1.437h0.626v-5.007h-0.626v-1.437h2.875l1.959 4.822h0.024l1.773-4.822h2.816zM62.439 16.117v-1.704c0.846-0.174 1.739-0.278 2.469-0.278 1.519 0 2.365 0.359 2.365 1.959v2.515h0.614v1.437h-2.353v-0.58h-0.024c-0.487 0.522-1.055 0.73-1.738 0.684-1.020-0.012-1.681-0.742-1.681-1.785 0-1.542 1.426-1.855 2.423-1.855h1.020v-0.313c0-0.522-0.371-0.626-1.032-0.626-0.21 0-0.419 0.016-0.626 0.046v0.498h-1.437zM65.534 17.543h-0.742c-0.533 0-0.974 0.081-0.974 0.649 0 0.452 0.382 0.638 0.742 0.638 0.382 0 0.776-0.151 0.974-0.301v-0.985zM68.222 11.932h2.364v4.949l1.6-1.194h-0.429v-1.437h3.014v1.437h-0.638l-1.124 0.835 1.426 2.086h0.452v1.437h-3.013v-1.437h0.371l-0.707-1.136-0.951 0.73v0.406h0.626v1.437h-2.991v-1.437h0.626v-5.239h-0.626v-1.437zM76.95 17.543c0.046 0.719 0.568 1.182 1.484 1.182 0.464 0 1.020 0 1.796-0.232l0.209 1.391c-0.788 0.22-1.507 0.278-2.26 0.278-2.272 0-3.072-1.171-3.072-3.014s0.8-3.014 3.060-3.014c2.516 0 2.701 1.634 2.457 3.408h-3.674zM76.95 16.465h1.959c0.081-0.556-0.058-0.997-0.846-0.997-0.684 0-1.055 0.359-1.112 0.997zM83.892 18.609v-5.007h-0.626v-1.437h3.095v1.437h-0.626v5.007h0.626v1.437h-3.095v-1.437h0.626zM87.080 15.479h-0.742v-1.124l0.742-0.104 0.208-1.623h1.53v1.623h1.368v1.229h-1.368v2.62c0 0.44 0.232 0.684 0.765 0.684 0.168-0.005 0.334-0.024 0.498-0.058l0.162 1.333c-0.418 0.063-0.84 0.098-1.263 0.104-1.38 0-1.901-0.579-1.901-1.762v-2.921zM98.090 18.609v1.437h-3.083v-1.437h0.626v-0.939l-2.063-4.069h-0.707v-1.437h3.431v1.437h-0.776l1.171 2.376h0.023l1.159-2.376h-0.753v-1.437h3.106v1.437h-0.603l-2.156 4.069v0.939h0.626zM99.179 17.149c0-1.843 0.788-3.014 2.887-3.014s2.886 1.171 2.886 3.014-0.788 3.014-2.886 3.014c-2.098 0-2.887-1.171-2.887-3.014zM101.022 17.149c0 0.997 0.232 1.576 1.044 1.576s1.043-0.579 1.043-1.576-0.232-1.576-1.043-1.576c-0.812 0-1.044 0.579-1.044 1.576zM105.206 14.251h2.364v3.547c0 0.626 0.302 0.927 0.812 0.927 0.383 0 0.753-0.185 1.020-0.336v-2.701h-0.672v-1.437h2.411v4.358h0.614v1.437h-2.353v-0.719h-0.023c-0.475 0.522-1.078 0.835-1.808 0.835-1.159 0-1.739-0.777-1.739-1.959v-2.515h-0.626v-1.437zM112.091 14.251h2.365v0.927h0.023c0.206-0.322 0.491-0.587 0.828-0.77s0.714-0.277 1.096-0.274v1.634c-0.742 0-1.484 0.128-1.947 0.348v2.492h0.649v1.437h-3.014v-1.437h0.626v-2.921h-0.626v-1.437zM120.308 16.117v-0.522c-0.314-0.056-0.632-0.083-0.95-0.081-0.522 0-0.73 0.174-0.73 0.371 0 0.22 0.197 0.301 0.788 0.44 1.043 0.232 2.538 0.487 2.538 1.913 0 1.333-0.939 1.924-2.364 1.924-0.962 0-2.017-0.104-2.712-0.278v-1.704h1.437v0.522c0.353 0.056 0.709 0.083 1.067 0.081 0.579 0 0.835-0.209 0.835-0.417 0-0.243-0.336-0.313-0.846-0.406-1.356-0.232-2.481-0.684-2.481-2.028 0-1.321 0.939-1.797 2.365-1.797 0.962 0 1.796 0.104 2.492 0.278v1.704h-1.437zM124.4 18.285v1.762h-1.739v-1.762h1.739zM2.408 11.951c-0.061-2.206 0.689-4.273 2.575-4.698 1.23-0.277 2.454 0.778 2.716 2.35l-1.716 0.32c-0.122-0.606-0.469-0.991-0.976-0.849-0.786 0.22-1.066 1.295-1.039 2.639 0.027 1.325 0.339 2.195 1.107 2.141 0.505-0.036 0.97-0.561 1.052-1.287 0 0 1.343-0.111 1.647-0.138 0 1.64-1.226 3.136-2.676 3.136-1.62 0-2.631-1.468-2.692-3.613zM14.295 10.004c-0.142-3.199 0.64-6.178 2.661-6.948 2.105-0.803 3.611 2.106 3.675 5.78 0.077 4.465-1.264 6.729-3.275 6.729-1.8 0-2.917-2.288-3.061-5.56zM16.294 9.796c0.066 1.955 0.448 3.382 1.090 3.32 0.709-0.070 1.084-1.788 1.026-4.037-0.059-2.31-0.528-3.797-1.248-3.372-0.51 0.301-0.943 1.867-0.868 4.090zM8.083 10.892c-0.098-2.781 0.764-5.114 2.417-5.668 1.847-0.62 3.185 1.725 3.243 4.742 0.065 3.438-0.973 5.599-2.956 5.599-1.621 0-2.607-1.935-2.704-4.672zM9.791 10.592c0.049 1.688 0.417 2.927 1.037 2.875 0.659-0.055 1.053-1.457 1.010-3.285-0.043-1.863-0.505-3.132-1.173-2.912-0.447 0.148-0.93 1.411-0.875 3.322zM23.726 3.223l-2.275-0.764v12.971h5.187v-2.332l-2.912-0.212v-9.663zM36.975 12.394l0.998 3.037h-1.61l-0.89-2.872-0.635-0.073v2.945h-1.891v-9.156l3.031 1.019c1.223 0.411 1.94 1.702 1.94 3.078 0 1.263-0.496 1.83-0.943 2.023zM36.454 10.063c0-0.584-0.299-1.009-0.726-1.122l-0.891-0.236v1.986l0.891 0.166c0.427 0.080 0.726-0.21 0.726-0.794zM21.452 19.094l1.583-0.106 0.001 9.864 2.165-0.722v-9.297l1.422-0.117v-2.322h-5.172v2.699zM27.286 27.437l5.003-1.667v-1.94l-2.937 0.772v-2.038l2.589-0.516v-1.978l-2.589 0.334v-1.849l2.937-0.206v-1.954h-5.003v11.042zM36.985 21.185l0.989 2.692-1.617 0.539-0.879-2.562-0.637 0.139v2.927l-1.894 0.63v-9.156h3.037c1.227 0 1.948 1.057 1.948 2.439 0 1.27-0.499 2.007-0.947 2.351zM36.461 19.017c0-0.587-0.299-0.913-0.728-0.883l-0.893 0.063v1.994l0.893-0.132c0.429-0.063 0.728-0.455 0.728-1.042zM12.501 16.395l2.142 11.434-1.994-0.695-0.265-1.72-1.795-0.511-0.229 1.448-1.642-0.566 1.713-9.389h2.070zM12.070 23.182l-0.636-3.869-0.587 3.59 1.223 0.278zM5.171 20.255l-0.752-3.86h-1.837v7.269l1.283 0.449v-4.596l0.973 4.929 0.553 0.192 1.254-4.712v5.147l1.683 0.584v-9.261h-2.183l-0.975 3.86zM40.502 12.391v7.782c0 3.929-0.597 5.074-4.199 6.643-1.25 0.541-3.138 1.478-7.962 3.304-2.124 0.805-5.318 1.881-8.108 1.881-2.776 0-5.969-1.076-8.1-1.881-4.818-1.826-6.705-2.763-7.955-3.304-3.602-1.569-4.206-2.714-4.206-6.643v-7.782c0-4.234 1.013-5.914 4.56-7.538 0.729-0.333 1.568-0.75 6.164-2.437 5.268-1.936 7.906-2.416 9.537-2.416 1.638 0 4.276 0.479 9.551 2.416 4.596 1.687 5.436 2.104 6.164 2.437 3.547 1.625 4.553 3.304 4.553 7.538zM39.371 11.87c0-3.859-1.735-5.158-4.22-6.192-0.875-0.368-1.236-0.604-5.644-2.235-3.623-1.346-6.941-2.352-9.274-2.352-2.318 0-5.636 1.006-9.267 2.352-4.4 1.632-4.762 1.868-5.643 2.235-2.479 1.034-4.214 2.333-4.214 6.192v8.601c0 2.984 0.687 4.123 3.151 5.227 2.061 0.916 2.27 1.014 6.532 2.686 2.693 1.055 6.282 2.45 9.44 2.45 3.173 0 6.754-1.395 9.448-2.45 4.269-1.673 4.477-1.77 6.538-2.686 2.464-1.104 3.152-2.242 3.152-5.227v-8.601zM16.774 19.836c-0.033-0.648 0.439-1.088 0.902-1.039 0.343 0.041 0.791 0.407 0.729 1.289l2.259 0.221c0.12-2.282-0.842-4-2.913-4.036-1.605-0.021-3.155 1.361-3.106 3.443 0.081 3.73 4.147 3.135 4.176 6.231 0.003 0.464-0.256 0.934-0.733 0.887-0.601-0.114-1.052-0.531-1.093-1.806l-2.114-0.518c-0.021 1.949 0.682 4.009 2.746 4.455 2.005 0.44 3.843-1.179 3.408-3.962-0.512-3.236-4.169-3.43-4.261-5.166zM27.287 15.431h5.001v-1.957l-2.937-0.2v-1.997l2.437 0.328v-1.987l-2.437-0.5v-1.872l2.937 0.779v-1.977l-5.003-1.66 0.001 11.042z"/></svg>'

# ── CM Brand CSS injected into every dashboard ───────────────
CM_CSS = """
/* ══════════════════════════════════════════════
   CM BRAND — Hub Palette Override + Components
══════════════════════════════════════════════ */

/* Force Hub palette via variable override */
:root {
  --bg:            #09090b;
  --bg-primary:    #09090b;
  --bg2:           #18181b;
  --bg-secondary:  #18181b;
  --bg3:           #1c1c1f;
  --bg-card:       #1c1c1f;
  --border:        #27272a;
  --text:          #fafafa;
  --text-primary:  #fafafa;
  --text-secondary:#a1a1aa;
  --text-muted:    #71717a;
  --muted:         #a1a1aa;
  --blue:          #3b82f6;
  --purple:        #7c3aed;
  --cm-blue:       #7c3aed;
  --cm-light:      #2e1065;
  --green-dim:     rgba(34,197,94,0.12);
  --blue-dim:      rgba(59,130,246,0.12);
  --yellow-dim:    rgba(234,179,8,0.12);
  --red-dim:       rgba(239,68,68,0.12);
  --purple-dim:    rgba(124,58,237,0.12);
  --orange-dim:    rgba(251,146,60,0.12);
}

body {
  background: #09090b !important;
  color: #fafafa !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #27272a; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #3f3f46; }

/* ── CM Brand Header ── */
.cm-brand-header {
  background: #09090b;
  border-bottom: 1px solid #27272a;
  padding: 22px 32px 18px;
  position: relative;
  z-index: 200;
}
.cm-brand-inner {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}
.cm-brand-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.cm-logo-wrap { display: flex; align-items: center; opacity: 0.92; flex-shrink: 0; }
.cm-logo-wrap svg { height: 30px; width: auto; }
.cm-brand-divider { width: 1px; height: 30px; background: #27272a; flex-shrink: 0; }
.cm-brand-title {
  font-size: 1rem; font-weight: 650; color: #fafafa;
  letter-spacing: -0.2px; line-height: 1.2;
}
.cm-brand-subtitle {
  font-size: 0.7rem; color: #71717a; margin-top: 2px;
  display: flex; align-items: center; gap: 6px;
}
.cm-status-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #22c55e; box-shadow: 0 0 0 2px rgba(34,197,94,.15);
  animation: cmPulse 2.5s ease-in-out infinite; flex-shrink: 0;
}
@keyframes cmPulse { 0%,100%{opacity:1} 50%{opacity:.4} }
.cm-back-link {
  font-size: 0.72rem; color: #71717a; text-decoration: none;
  padding: 6px 14px; border: 1px solid #27272a; border-radius: 7px;
  transition: color .15s, border-color .15s, background .15s;
  white-space: nowrap; display: flex; align-items: center; gap: 6px;
}
.cm-back-link:hover { color: #fafafa !important; border-color: #3f3f46; background: #18181b; text-decoration: none; }

/* ── CM Brand Footer ── */
.cm-brand-footer {
  border-top: 1px solid #27272a; padding: 16px 32px;
  margin-top: 48px; background: #09090b;
}
.cm-footer-inner {
  max-width: 1600px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
}
.cm-footer-brand { font-size: 0.72rem; color: #71717a; }
.cm-footer-brand strong { color: #a1a1aa; font-weight: 500; }
.cm-footer-link { font-size: 0.72rem; color: #71717a; text-decoration: none; }
.cm-footer-link:hover { color: #fafafa; }

@media (max-width: 768px) {
  .cm-brand-header { padding: 16px 20px 14px; }
  .cm-brand-footer { padding: 14px 20px; }
  .cm-brand-left { gap: 12px; }
  .cm-logo-wrap svg { height: 24px; }
}
"""

# ── Header/Footer HTML ────────────────────────────────────────
def make_header(title, subtitle):
    return (
        '\n<!-- ══ CM Brand Header ══ -->\n'
        '<header class="cm-brand-header">\n'
        '  <div class="cm-brand-inner">\n'
        '    <div class="cm-brand-left">\n'
        '      <div class="cm-logo-wrap" title="Cooler Master">' + CM_SVG + '</div>\n'
        '      <div class="cm-brand-divider"></div>\n'
        '      <div>\n'
        '        <div class="cm-brand-title">' + title + '</div>\n'
        '        <div class="cm-brand-subtitle"><span class="cm-status-dot"></span>' + subtitle + '</div>\n'
        '      </div>\n'
        '    </div>\n'
        '    <a href="CM_Brasil_Hub.html" class="cm-back-link">← Command Center</a>\n'
        '  </div>\n'
        '</header>\n'
    )

CM_FOOTER = (
    '\n<!-- ══ CM Brand Footer ══ -->\n'
    '<footer class="cm-brand-footer">\n'
    '  <div class="cm-footer-inner">\n'
    '    <div class="cm-footer-brand">🐧 <strong>Jubinha AI</strong> &nbsp;·&nbsp; Cooler Master Brasil Intelligence Platform</div>\n'
    '    <a href="CM_Brasil_Hub.html" class="cm-footer-link">← Voltar ao Hub</a>\n'
    '  </div>\n'
    '</footer>\n'
)

# ── Color substitution map (old → new Hub palette) ───────────
COLOR_MAP = [
    ('#0d1117', '#09090b'), ('#0a0a0f', '#09090b'), ('#0f0f0f', '#09090b'),
    ('#161b22', '#18181b'), ('#111827', '#18181b'), ('#0f172a', '#18181b'),
    ('#1a1f2e', '#18181b'), ('#1c2128', '#1c1c1f'), ('#21262d', '#1c1c1f'),
    ('#162032', '#1a1a1e'), ('#1a2332', '#1c1c1f'),
    ('#30363d', '#27272a'), ('#1e293b', '#27272a'),
    ('#e6edf3', '#fafafa'), ('#c9d1d9', '#fafafa'), ('#e2e8f0', '#fafafa'),
    ('#94a3b8', '#a1a1aa'), ('#8b949e', '#a1a1aa'),
    ('#64748b', '#71717a'), ('#475569', '#71717a'), ('#334155', '#71717a'), ('#656d76', '#71717a'),
    ('#58a6ff', '#3b82f6'), ('#4fc3f7', '#3b82f6'),
]

def sub_colors_in_style(html, cmap=COLOR_MAP):
    """Replace colors only within <style>…</style> blocks."""
    def fix(m):
        s = m.group(0)
        for o, n in cmap:
            s = s.replace(o, n).replace(o.upper(), n)
        return s
    return re.sub(r'<style[^>]*>.*?</style>', fix, html, flags=re.DOTALL | re.IGNORECASE)

def sub_colors_in_scripts(html, cmap=COLOR_MAP):
    """Replace color literals in <script> blocks (chart colors, etc.)."""
    def fix(m):
        s = m.group(0)
        for o, n in cmap:
            s = s.replace(f"'{o}'", f"'{n}'")
            s = s.replace(f'"{o}"', f'"{n}"')
        return s
    return re.sub(r'<script[^>]*>.*?</script>', fix, html, flags=re.DOTALL | re.IGNORECASE)

def inject_css(html, extra_css=''):
    """Inject CM CSS + optional extra CSS before first </style>."""
    return html.replace('</style>', CM_CSS + extra_css + '\n  </style>', 1)

def inject_header(html, title, subtitle):
    """Inject CM header right after <body> tag."""
    hdr = make_header(title, subtitle)
    # Try <body> with no attributes first, then any <body...>
    if '<body>' in html:
        return html.replace('<body>', '<body>' + hdr, 1)
    return re.sub(r'(<body[^>]*>)', r'\1' + hdr.replace('\\', '\\\\'), html, count=1)

def inject_footer(html):
    return html.replace('</body>', CM_FOOTER + '</body>', 1)

# ════════════════════════════════════════════════════════════════
#  1. CM_FollowUp_Tracker.html
# ════════════════════════════════════════════════════════════════
def transform_followup():
    path = f"{WS}/CM_FollowUp_Tracker.html"
    with open(path) as f: html = f.read()

    html = sub_colors_in_style(html)
    html = inject_css(html, extra_css='\n  /* Hide old header */\n  .header { display:none !important; }\n')
    html = inject_header(html, "Follow-up Tracker",
                         "Cooler Master Brasil — Pendências &amp; Deadlines")
    # Remove old footer content, keep the div stub
    html = re.sub(r'(<div class="footer">).*?(</div>)', r'\1\2', html, flags=re.DOTALL)
    html = inject_footer(html)

    with open(path, 'w') as f: f.write(html)
    print("✅ CM_FollowUp_Tracker.html")

# ════════════════════════════════════════════════════════════════
#  2. dashboard_sellin.html
# ════════════════════════════════════════════════════════════════
def transform_sellin():
    path = f"{WS}/dashboard_sellin.html"
    with open(path) as f: html = f.read()

    html = sub_colors_in_style(html)
    html = sub_colors_in_scripts(html)
    html = inject_css(html, extra_css='\n  /* Hide old header */\n  .header { display:none !important; }\n')
    html = inject_header(html, "Dashboard Sell-In",
                         "Cooler Master Brasil — Pipeline, Pedidos &amp; Buffer Q1 2026")
    html = inject_footer(html)

    with open(path, 'w') as f: f.write(html)
    print("✅ dashboard_sellin.html")

# ════════════════════════════════════════════════════════════════
#  3. dashboard_sellout.html
# ════════════════════════════════════════════════════════════════
def transform_sellout():
    path = f"{WS}/dashboard_sellout.html"
    with open(path) as f: html = f.read()

    html = sub_colors_in_style(html)
    html = sub_colors_in_scripts(html)
    html = inject_css(html, extra_css='\n  /* Hide old header */\n  .header { display:none !important; }\n')
    html = inject_header(html, "Dashboard Sell-Out",
                         "Cooler Master Brasil — KaBuM · Pichau · Terabyte · W01-W06 FY2026")
    html = inject_footer(html)

    with open(path, 'w') as f: f.write(html)
    print("✅ dashboard_sellout.html")

# ════════════════════════════════════════════════════════════════
#  4. CM_Brasil_MasterDeck.html
# ════════════════════════════════════════════════════════════════
def transform_masterdeck():
    path = f"{WS}/CM_Brasil_MasterDeck.html"
    with open(path) as f: html = f.read()

    # Replace :root variable values (keep var names, change values)
    root_subs = [
        ('--bg-primary: #0d1117',   '--bg-primary: #09090b'),
        ('--bg-secondary: #161b22', '--bg-secondary: #18181b'),
        ('--bg-card: #21262d',      '--bg-card: #1c1c1f'),
        ('--border: #30363d',       '--border: #27272a'),
        ('--text-primary: #e6edf3', '--text-primary: #fafafa'),
        ('--text-secondary: #8b949e','--text-secondary: #a1a1aa'),
        ('--text-muted: #656d76',   '--text-muted: #71717a'),
        ('--blue: #58a6ff',         '--blue: #3b82f6'),
        ('--purple: #bc8cff',       '--purple: #7c3aed'),
    ]
    for o, n in root_subs: html = html.replace(o, n)

    html = sub_colors_in_scripts(html)
    # Hide .header-top (title area), keep tabs; inject CM header before sticky header
    html = inject_css(html, extra_css='\n  /* Hide old title row, keep tabs */\n  .header-top { display:none !important; }\n')
    html = inject_header(html, "MasterDeck",
                         "Cooler Master Brasil — Sell-In · Sell-Out · Clientes · Pipeline · Insights")
    html = inject_footer(html)

    with open(path, 'w') as f: f.write(html)
    print("✅ CM_Brasil_MasterDeck.html")

# ════════════════════════════════════════════════════════════════
#  5. CM_Simulador_Precos.html
# ════════════════════════════════════════════════════════════════
def transform_simulador():
    path = f"{WS}/CM_Simulador_Precos.html"
    with open(path) as f: html = f.read()

    root_subs = [
        ('--bg-primary: #0d1117',   '--bg-primary: #09090b'),
        ('--bg-secondary: #161b22', '--bg-secondary: #18181b'),
        ('--bg-card: #21262d',      '--bg-card: #1c1c1f'),
        ('--border: #30363d',       '--border: #27272a'),
        ('--text-primary: #e6edf3', '--text-primary: #fafafa'),
        ('--text-secondary: #8b949e','--text-secondary: #a1a1aa'),
        ('--text-muted: #656d76',   '--text-muted: #71717a'),
        ('--blue: #58a6ff',         '--blue: #3b82f6'),
        ('--purple: #bc8cff',       '--purple: #7c3aed'),
    ]
    for o, n in root_subs: html = html.replace(o, n)

    html = inject_css(html, extra_css='\n  /* Hide old title row, keep tabs */\n  .header-top { display:none !important; }\n')
    html = inject_header(html, "Simulador de Preços",
                         "Cooler Master Brasil — FOB→Varejo · Reverse · FUNDAP · TTD")
    html = inject_footer(html)

    with open(path, 'w') as f: f.write(html)
    print("✅ CM_Simulador_Precos.html")

# ════════════════════════════════════════════════════════════════
#  6. CM_Catalogo_Dashboard.html
# ════════════════════════════════════════════════════════════════
def transform_catalogo():
    path = f"{WS}/CM_Catalogo_Dashboard.html"
    with open(path) as f: html = f.read()

    root_subs = [
        ('--bg: #0d1117',     '--bg: #09090b'),
        ('--bg2: #161b22',    '--bg2: #18181b'),
        ('--bg3: #21262d',    '--bg3: #1c1c1f'),
        ('--border: #30363d', '--border: #27272a'),
        ('--text: #e6edf3',   '--text: #fafafa'),
        ('--muted: #8b949e',  '--muted: #a1a1aa'),
        ('--blue: #58a6ff',   '--blue: #3b82f6'),
        ('--purple: #bc8cff', '--purple: #7c3aed'),
        ('--cm-blue: #0066CC','--cm-blue: #7c3aed'),
        ('--cm-light: #1a3a5c','--cm-light: #2e1065'),
    ]
    for o, n in root_subs: html = html.replace(o, n)

    html = sub_colors_in_scripts(html)
    # Hide old blue gradient header
    html = inject_css(html, extra_css='\n  /* Hide old CM-blue gradient header */\n  .header { display:none !important; }\n')
    html = inject_header(html, "Catálogo de Produtos",
                         "Cooler Master Brasil — Packing List · KaBuM · Fabricantes")
    html = inject_footer(html)

    with open(path, 'w') as f: f.write(html)
    print("✅ CM_Catalogo_Dashboard.html (palette done)")

# ════════════════════════════════════════════════════════════════
#  RUN ALL
# ════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("🎨 Starting CM Brasil dashboard transformation...\n")
    transform_followup()
    transform_sellin()
    transform_sellout()
    transform_masterdeck()
    transform_simulador()
    transform_catalogo()
    print("\n✅ All 6 dashboards transformed!")
