#!/usr/bin/env python3
"""
hub_rewrite.py — Real rewrite of all CM Brasil dashboards to match Hub design system.
Approach: Replace style block with clean Hub CSS + adapted page CSS.
         Inject Hub header (logo SVG + title + clock + back link).
         Inject Hub footer (🐧 Jubinha AI).
         Preserve ALL JS and functional HTML.
"""

import re, os, shutil

WORKSPACE = os.path.expanduser("~/.openclaw/workspace-main")
ONEDRIVE  = os.path.expanduser("~/Library/CloudStorage/OneDrive-CoolerMaster/2026/Dashboards")

# ─── CM Logo SVG ──────────────────────────────────────────────────────────────
CM_SVG = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="124" height="32" viewBox="0 0 124 32"><path fill="#ffffff" d="M61.768 12.164v1.437h-0.614v5.007h0.614v1.437h-3.083v-1.437h0.626v-3.153h-0.023l-1.658 4.59h-1.17l-1.797-4.59h-0.023v3.153h0.672v1.437h-2.99v-1.437h0.626v-5.007h-0.626v-1.437h2.875l1.959 4.822h0.024l1.773-4.822h2.816zM62.439 16.117v-1.704c0.846-0.174 1.739-0.278 2.469-0.278 1.519 0 2.365 0.359 2.365 1.959v2.515h0.614v1.437h-2.353v-0.58h-0.024c-0.487 0.522-1.055 0.73-1.738 0.684-1.020-0.012-1.681-0.742-1.681-1.785 0-1.542 1.426-1.855 2.423-1.855h1.020v-0.313c0-0.522-0.371-0.626-1.032-0.626-0.21 0-0.419 0.016-0.626 0.046v0.498h-1.437zM65.534 17.543h-0.742c-0.533 0-0.974 0.081-0.974 0.649 0 0.452 0.382 0.638 0.742 0.638 0.382 0 0.776-0.151 0.974-0.301v-0.985zM68.222 11.932h2.364v4.949l1.6-1.194h-0.429v-1.437h3.014v1.437h-0.638l-1.124 0.835 1.426 2.086h0.452v1.437h-3.013v-1.437h0.371l-0.707-1.136-0.951 0.73v0.406h0.626v1.437h-2.991v-1.437h0.626v-5.239h-0.626v-1.437zM76.95 17.543c0.046 0.719 0.568 1.182 1.484 1.182 0.464 0 1.020 0 1.796-0.232l0.209 1.391c-0.788 0.22-1.507 0.278-2.26 0.278-2.272 0-3.072-1.171-3.072-3.014s0.8-3.014 3.060-3.014c2.516 0 2.701 1.634 2.457 3.408h-3.674zM76.95 16.465h1.959c0.081-0.556-0.058-0.997-0.846-0.997-0.684 0-1.055 0.359-1.112 0.997zM83.892 18.609v-5.007h-0.626v-1.437h3.095v1.437h-0.626v5.007h0.626v1.437h-3.095v-1.437h0.626zM87.080 15.479h-0.742v-1.124l0.742-0.104 0.208-1.623h1.53v1.623h1.368v1.229h-1.368v2.62c0 0.44 0.232 0.684 0.765 0.684 0.168-0.005 0.334-0.024 0.498-0.058l0.162 1.333c-0.418 0.063-0.84 0.098-1.263 0.104-1.38 0-1.901-0.579-1.901-1.762v-2.921zM98.090 18.609v1.437h-3.083v-1.437h0.626v-0.939l-2.063-4.069h-0.707v-1.437h3.431v1.437h-0.776l1.171 2.376h0.023l1.159-2.376h-0.753v-1.437h3.106v1.437h-0.603l-2.156 4.069v0.939h0.626zM99.179 17.149c0-1.843 0.788-3.014 2.887-3.014s2.886 1.171 2.886 3.014-0.788 3.014-2.886 3.014c-2.098 0-2.887-1.171-2.887-3.014zM101.022 17.149c0 0.997 0.232 1.576 1.044 1.576s1.043-0.579 1.043-1.576-0.232-1.576-1.043-1.576c-0.812 0-1.044 0.579-1.044 1.576zM105.206 14.251h2.364v3.547c0 0.626 0.302 0.927 0.812 0.927 0.383 0 0.753-0.185 1.020-0.336v-2.701h-0.672v-1.437h2.411v4.358h0.614v1.437h-2.353v-0.719h-0.023c-0.475 0.522-1.078 0.835-1.808 0.835-1.159 0-1.739-0.777-1.739-1.959v-2.515h-0.626v-1.437zM112.091 14.251h2.365v0.927h0.023c0.206-0.322 0.491-0.587 0.828-0.77s0.714-0.277 1.096-0.274v1.634c-0.742 0-1.484 0.128-1.947 0.348v2.492h0.649v1.437h-3.014v-1.437h0.626v-2.921h-0.626v-1.437zM120.308 16.117v-0.522c-0.314-0.056-0.632-0.083-0.95-0.081-0.522 0-0.73 0.174-0.73 0.371 0 0.22 0.197 0.301 0.788 0.44 1.043 0.232 2.538 0.487 2.538 1.913 0 1.333-0.939 1.924-2.364 1.924-0.962 0-2.017-0.104-2.712-0.278v-1.704h1.437v0.522c0.353 0.056 0.709 0.083 1.067 0.081 0.579 0 0.835-0.209 0.835-0.417 0-0.243-0.336-0.313-0.846-0.406-1.356-0.232-2.481-0.684-2.481-2.028 0-1.321 0.939-1.797 2.365-1.797 0.962 0 1.796 0.104 2.492 0.278v1.704h-1.437zM124.4 18.285v1.762h-1.739v-1.762h1.739zM2.408 11.951c-0.061-2.206 0.689-4.273 2.575-4.698 1.23-0.277 2.454 0.778 2.716 2.35l-1.716 0.32c-0.122-0.606-0.469-0.991-0.976-0.849-0.786 0.22-1.066 1.295-1.039 2.639 0.027 1.325 0.339 2.195 1.107 2.141 0.505-0.036 0.97-0.561 1.052-1.287 0 0 1.343-0.111 1.647-0.138 0 1.64-1.226 3.136-2.676 3.136-1.62 0-2.631-1.468-2.692-3.613zM14.295 10.004c-0.142-3.199 0.64-6.178 2.661-6.948 2.105-0.803 3.611 2.106 3.675 5.78 0.077 4.465-1.264 6.729-3.275 6.729-1.8 0-2.917-2.288-3.061-5.56zM16.294 9.796c0.066 1.955 0.448 3.382 1.090 3.32 0.709-0.070 1.084-1.788 1.026-4.037-0.059-2.31-0.528-3.797-1.248-3.372-0.51 0.301-0.943 1.867-0.868 4.090zM8.083 10.892c-0.098-2.781 0.764-5.114 2.417-5.668 1.847-0.62 3.185 1.725 3.243 4.742 0.065 3.438-0.973 5.599-2.956 5.599-1.621 0-2.607-1.935-2.704-4.672zM9.791 10.592c0.049 1.688 0.417 2.927 1.037 2.875 0.659-0.055 1.053-1.457 1.010-3.285-0.043-1.863-0.505-3.132-1.173-2.912-0.447 0.148-0.93 1.411-0.875 3.322zM23.726 3.223l-2.275-0.764v12.971h5.187v-2.332l-2.912-0.212v-9.663zM36.975 12.394l0.998 3.037h-1.61l-0.89-2.872-0.635-0.073v2.945h-1.891v-9.156l3.031 1.019c1.223 0.411 1.94 1.702 1.94 3.078 0 1.263-0.496 1.83-0.943 2.023zM36.454 10.063c0-0.584-0.299-1.009-0.726-1.122l-0.891-0.236v1.986l0.891 0.166c0.427 0.080 0.726-0.21 0.726-0.794zM21.452 19.094l1.583-0.106 0.001 9.864 2.165-0.722v-9.297l1.422-0.117v-2.322h-5.172v2.699zM27.286 27.437l5.003-1.667v-1.94l-2.937 0.772v-2.038l2.589-0.516v-1.978l-2.589 0.334v-1.849l2.937-0.206v-1.954h-5.003v11.042zM36.985 21.185l0.989 2.692-1.617 0.539-0.879-2.562-0.637 0.139v2.927l-1.894 0.63v-9.156h3.037c1.227 0 1.948 1.057 1.948 2.439 0 1.27-0.499 2.007-0.947 2.351zM36.461 19.017c0-0.587-0.299-0.913-0.728-0.883l-0.893 0.063v1.994l0.893-0.132c0.429-0.063 0.728-0.455 0.728-1.042zM12.501 16.395l2.142 11.434-1.994-0.695-0.265-1.72-1.795-0.511-0.229 1.448-1.642-0.566 1.713-9.389h2.070zM12.070 23.182l-0.636-3.869-0.587 3.59 1.223 0.278zM5.171 20.255l-0.752-3.86h-1.837v7.269l1.283 0.449v-4.596l0.973 4.929 0.553 0.192 1.254-4.712v5.147l1.683 0.584v-9.261h-2.183l-0.975 3.86zM40.502 12.391v7.782c0 3.929-0.597 5.074-4.199 6.643-1.25 0.541-3.138 1.478-7.962 3.304-2.124 0.805-5.318 1.881-8.108 1.881-2.776 0-5.969-1.076-8.1-1.881-4.818-1.826-6.705-2.763-7.955-3.304-3.602-1.569-4.206-2.714-4.206-6.643v-7.782c0-4.234 1.013-5.914 4.56-7.538 0.729-0.333 1.568-0.75 6.164-2.437 5.268-1.936 7.906-2.416 9.537-2.416 1.638 0 4.276 0.479 9.551 2.416 4.596 1.687 5.436 2.104 6.164 2.437 3.547 1.625 4.553 3.304 4.553 7.538zM39.371 11.87c0-3.859-1.735-5.158-4.22-6.192-0.875-0.368-1.236-0.604-5.644-2.235-3.623-1.346-6.941-2.352-9.274-2.352-2.318 0-5.636 1.006-9.267 2.352-4.4 1.632-4.762 1.868-5.643 2.235-2.479 1.034-4.214 2.333-4.214 6.192v8.601c0 2.984 0.687 4.123 3.151 5.227 2.061 0.916 2.27 1.014 6.532 2.686 2.693 1.055 6.282 2.45 9.44 2.45 3.173 0 6.754-1.395 9.448-2.45 4.269-1.673 4.477-1.77 6.538-2.686 2.464-1.104 3.152-2.242 3.152-5.227v-8.601zM16.774 19.836c-0.033-0.648 0.439-1.088 0.902-1.039 0.343 0.041 0.791 0.407 0.729 1.289l2.259 0.221c0.12-2.282-0.842-4-2.913-4.036-1.605-0.021-3.155 1.361-3.106 3.443 0.081 3.73 4.147 3.135 4.176 6.231 0.003 0.464-0.256 0.934-0.733 0.887-0.601-0.114-1.052-0.531-1.093-1.806l-2.114-0.518c-0.021 1.949 0.682 4.009 2.746 4.455 2.005 0.44 3.843-1.179 3.408-3.962-0.512-3.236-4.169-3.43-4.261-5.166zM27.287 15.431h5.001v-1.957l-2.937-0.2v-1.997l2.437 0.328v-1.987l-2.437-0.5v-1.872l2.937 0.779v-1.977l-5.003-1.66 0.001 11.042z"/></svg>'

# ─── Hub CSS (clean) ──────────────────────────────────────────────────────────
HUB_CSS = '''    /* ─── Reset & Base ─── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:           #09090b;
      --surface:      #18181b;
      --surface-hover:#1c1c1f;
      --border:       #27272a;
      --border-hover: #3f3f46;
      --text:         #fafafa;
      --text-2:       #a1a1aa;
      --text-3:       #71717a;
      --accent:       #7c3aed;
      --accent-2:     #6d28d9;
      --accent-glow:  rgba(124,58,237,0.12);
      --blue:         #3b82f6;
      --blue-glow:    rgba(59,130,246,0.10);
      --green:        #22c55e;
      --green-dim:    rgba(34,197,94,0.15);
      --yellow:       #eab308;
      --yellow-dim:   rgba(234,179,8,0.15);
      --red:          #ef4444;
      --red-dim:      rgba(239,68,68,0.15);
      --purple-dim:   rgba(124,58,237,0.15);
      --orange:       #f97316;
      --orange-dim:   rgba(249,115,22,0.15);
    }

    html { scroll-behavior: smooth; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      font-size: 14px;
    }

    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--border-hover); }

    /* ─── Hub Page Header ─── */
    .hub-header {
      border-bottom: 1px solid var(--border);
      padding: 18px 40px;
      position: sticky; top: 0; z-index: 200;
      background: var(--bg);
    }
    .hub-header-inner {
      max-width: 1400px; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between; gap: 20px;
    }
    .hub-header-brand {
      display: flex; align-items: center; gap: 18px;
    }
    .hub-header-logo { display: flex; align-items: center; opacity: 0.92; flex-shrink: 0; }
    .hub-header-logo svg { height: 28px; width: auto; }
    .hub-header-sep { width: 1px; height: 26px; background: var(--border); flex-shrink: 0; }
    .hub-header-title { font-size: 1.05rem; font-weight: 650; letter-spacing: -0.3px; color: var(--text); }
    .hub-header-sub {
      font-size: 0.7rem; color: var(--text-3); margin-top: 2px;
      display: flex; align-items: center; gap: 5px;
    }
    .hub-header-dot {
      width: 5px; height: 5px; border-radius: 50%;
      background: var(--green); box-shadow: 0 0 0 2px var(--green-dim);
      animation: hpulse 2.5s ease-in-out infinite; flex-shrink: 0;
    }
    @keyframes hpulse { 0%,100%{opacity:1} 50%{opacity:0.45} }

    .hub-header-right { display: flex; align-items: center; gap: 14px; flex-shrink: 0; }
    .hub-back-btn {
      font-size: 0.72rem; color: var(--text-3); text-decoration: none;
      display: inline-flex; align-items: center; gap: 5px;
      padding: 4px 10px; border: 1px solid var(--border); border-radius: 999px;
      transition: color 0.15s, border-color 0.15s;
    }
    .hub-back-btn:hover { color: var(--text); border-color: var(--border-hover); }
    .hub-clock-wrap { text-align: right; }
    .hub-clock {
      font-size: 1.2rem; font-weight: 600; font-variant-numeric: tabular-nums;
      color: var(--text); font-family: 'Menlo','SF Mono','Consolas',monospace; letter-spacing: 0.4px;
    }
    .hub-date { font-size: 0.68rem; color: var(--text-3); margin-top: 2px; text-align: right; }

    /* ─── Hub Page Footer ─── */
    .hub-footer-bar {
      border-top: 1px solid var(--border);
      padding: 16px 40px;
      margin-top: 64px;
    }
    .hub-footer-inner {
      max-width: 1400px; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between; gap: 16px;
    }
    .hub-footer-brand { font-size: 0.75rem; color: var(--text-3); display: flex; align-items: center; gap: 6px; }
    .hub-footer-brand strong { color: var(--text-2); font-weight: 500; }
    .hub-footer-meta { font-size: 0.7rem; color: var(--text-3); display: flex; align-items: center; gap: 10px; }
    .hub-footer-dot { width: 2px; height: 2px; border-radius: 50%; background: var(--text-3); }
    .hub-footer-meta a { color: var(--text-3); text-decoration: none; }
    .hub-footer-meta a:hover { color: var(--text-2); }

    /* ─── Page container ─── */
    .page-body {
      max-width: 1400px; margin: 0 auto; padding: 40px 40px 80px;
    }

    /* ─── Section headers (Hub style) ─── */
    .hub-section-head {
      display: flex; align-items: center; gap: 12px; margin-bottom: 20px;
    }
    .hub-section-label {
      font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.1em; color: var(--text-3); white-space: nowrap;
    }
    .hub-section-count {
      font-size: 0.65rem; font-weight: 500; color: var(--text-3);
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 999px; padding: 1px 7px;
    }
    .hub-section-rule { flex: 1; height: 1px; background: var(--border); opacity: 0.7; }

    /* ─── Shared Table styles ─── */
    table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
    th {
      background: #27272a; color: var(--text-2); font-weight: 600;
      font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
      padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    td {
      padding: 9px 14px; border-bottom: 1px solid rgba(39,39,42,0.6);
      color: var(--text-2); vertical-align: middle;
    }
    tr:last-child td { border-bottom: none; }
    tbody tr:hover td { background: var(--surface-hover); color: var(--text); }

    /* ─── Shared Card/Badge styles ─── */
    .badge {
      display: inline-flex; align-items: center;
      font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.06em; padding: 2px 8px; border-radius: 999px;
      border: 1px solid transparent; white-space: nowrap;
    }
    .badge-green   { background: var(--green-dim);  color: var(--green);  border-color: rgba(34,197,94,0.25); }
    .badge-blue    { background: var(--blue-glow);  color: var(--blue);   border-color: rgba(59,130,246,0.25); }
    .badge-yellow  { background: var(--yellow-dim); color: var(--yellow); border-color: rgba(234,179,8,0.25); }
    .badge-red     { background: var(--red-dim);    color: var(--red);    border-color: rgba(239,68,68,0.25); }
    .badge-purple  { background: var(--purple-dim); color: #a78bfa;       border-color: rgba(124,58,237,0.3); }
    .badge-orange  { background: var(--orange-dim); color: var(--orange); border-color: rgba(249,115,22,0.25); }
    .badge-gray    { background: var(--surface);    color: var(--text-3); border-color: var(--border); }

    /* ─── Shared Input styles ─── */
    input, select, textarea {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 8px; color: var(--text); padding: 8px 12px;
      font-size: 0.85rem; font-family: inherit; outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    input:focus, select:focus, textarea:focus {
      border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow);
    }
    input::placeholder, textarea::placeholder { color: var(--text-3); }
    input[type="range"] {
      -webkit-appearance: none; background: var(--border);
      height: 4px; border-radius: 2px; padding: 0; border: none; box-shadow: none;
    }
    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none; width: 14px; height: 14px;
      border-radius: 50%; background: var(--accent); cursor: pointer;
    }
    input[type="checkbox"] { width: 16px; height: 16px; cursor: pointer; accent-color: var(--accent); }

    /* ─── Animations ─── */
    @keyframes fadeUp { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
    .fade-up { animation: fadeUp 0.35s ease both; }

    /* ─── Responsive ─── */
    @media (max-width: 768px) {
      .hub-header { padding: 14px 20px; }
      .hub-footer-bar { padding: 12px 20px; }
      .page-body { padding: 28px 20px 60px; }
      .hub-header-inner { flex-wrap: wrap; }
      .hub-clock { font-size: 1rem; }
      .hub-footer-inner { flex-direction: column; align-items: flex-start; gap: 4px; }
    }
    @media (max-width: 480px) {
      .hub-header-brand { flex-wrap: wrap; }
      .hub-header-sep { display: none; }
    }
'''

# ─── Hub Header HTML ──────────────────────────────────────────────────────────
def make_header(title, subtitle):
    return f'''<!-- ══════ HUB HEADER ══════ -->
<header class="hub-header">
  <div class="hub-header-inner">
    <div class="hub-header-brand">
      <div class="hub-header-logo" title="Cooler Master">{CM_SVG}</div>
      <div class="hub-header-sep"></div>
      <div>
        <div class="hub-header-title">{title}</div>
        <div class="hub-header-sub">
          <span class="hub-header-dot"></span>
          {subtitle}
        </div>
      </div>
    </div>
    <div class="hub-header-right">
      <a href="CM_Brasil_Hub.html" class="hub-back-btn">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 5l-7 7 7 7"/></svg>
        Hub
      </a>
      <div class="hub-clock-wrap">
        <div class="hub-clock" id="hub-clock">--:--:--</div>
        <div class="hub-date" id="hub-date">carregando…</div>
      </div>
    </div>
  </div>
</header>
<script>
(function(){{
  var W=['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'];
  var M=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
  function p(n){{return String(n).padStart(2,'0');}}
  function tick(){{
    var n=new Date(),c=document.getElementById('hub-clock'),d=document.getElementById('hub-date');
    if(c)c.textContent=p(n.getHours())+':'+p(n.getMinutes())+':'+p(n.getSeconds());
    if(d)d.textContent=W[n.getDay()]+', '+p(n.getDate())+' '+M[n.getMonth()]+' '+n.getFullYear();
  }}
  tick();setInterval(tick,1000);
}})();
</script>
<!-- ══════ END HUB HEADER ══════ -->'''

# ─── Hub Footer HTML ──────────────────────────────────────────────────────────
def make_footer(label):
    return f'''<!-- ══════ HUB FOOTER ══════ -->
<footer class="hub-footer-bar">
  <div class="hub-footer-inner">
    <div class="hub-footer-brand">🐧 <strong>Jubinha AI</strong> &nbsp;·&nbsp; {label}</div>
    <div class="hub-footer-meta">
      <span>Cooler Master Brasil</span>
      <span class="hub-footer-dot"></span>
      <span>2026</span>
      <span class="hub-footer-dot"></span>
      <a href="CM_Brasil_Hub.html">← Command Center</a>
    </div>
  </div>
</footer>
<!-- ══════ END HUB FOOTER ══════ -->'''

# ─── CSS Extraction ───────────────────────────────────────────────────────────
def extract_page_css(style_block):
    """Extract only the page-specific CSS, stripping hub overlay and hide rules."""
    css = style_block
    
    # Remove the hub overlay header comment + all hub overlay content
    # The hub overlay ends after the hub-footer CSS block
    # Strategy: find "hub-footer a:hover" and take everything after
    m = re.search(r'\.hub-footer a:hover\s*\{[^}]+\}\s*\n', css, re.DOTALL)
    if m:
        css = css[m.end():]
    else:
        # Try alternate: find end of the overlay :root block
        m2 = re.search(r'--blue-start\s*:[^}]+\}', css, re.DOTALL)
        if m2:
            css = css[m2.end():]
        else:
            # Fallback: try to find where original CSS starts
            # Look for first CSS rule after lots of root overrides
            m3 = re.search(r'/\*.*?\*/\s*\n\s*\*\s*\{', css, re.DOTALL)
            if m3:
                css = css[m3.start():]
            else:
                # Just use the original
                pass
    
    # Remove hide-header rules
    css = re.sub(r'/\* Hide original header[^*]*\*/', '', css)
    css = re.sub(r'\.header:not\(\.hub-nav\)\s*\{[^}]*\}', '', css)
    css = re.sub(r'header:not\(\.hub-nav\)\s*\{[^}]*\}', '', css)
    css = re.sub(r'#header\s*\{[^}]*\}', '', css)
    css = re.sub(r'\.topbar:not\(\.hub-nav\)\s*\{[^}]*\}', '', css)
    css = re.sub(r'\.navbar:not\(\.hub-nav\)\s*\{[^}]*\}', '', css)
    css = re.sub(r'\.top-bar:not\(\.hub-nav\)\s*\{[^}]*\}', '', css)
    
    # Remove old :root overrides
    css = re.sub(r':root\s*\{[^}]+\}', '', css)
    
    # Remove old body{} block
    css = re.sub(r'\*\s*\{[^}]*\}', '', css)
    css = re.sub(r'body\s*\{\s*(?:font-family|background|color|min-height|line-height|font-size|margin|padding)[^}]*\}', '', css)
    
    # Remove old scrollbar rules
    css = re.sub(r'::-webkit-scrollbar[^{]*\{[^}]*\}', '', css)
    
    # Remove the old .header CSS rule (card-style background)
    # But be careful not to remove all .header rules - just the outer card definition
    css = re.sub(
        r'\.header\s*\{[^}]*(?:background|border-radius|gradient)[^}]*\}',
        '', css, flags=re.DOTALL
    )
    
    return css.strip()

# ─── Body Transformation ──────────────────────────────────────────────────────
def transform_body(body, has_tabs_in_header=False):
    """
    Strip hub-nav/footer injections from body.
    Returns cleaned body content.
    """
    # Remove hub-nav injection
    body = re.sub(
        r'<!-- ══ HUB NAV ══ -->.*?<!-- ══ END HUB NAV ══ -->',
        '', body, flags=re.DOTALL
    )
    # Remove hub-footer injection
    body = re.sub(
        r'<!-- ══ HUB FOOTER ══ -->.*?<!-- ══ END HUB FOOTER ══ -->',
        '', body, flags=re.DOTALL
    )
    # Remove old hub clock script
    body = re.sub(
        r'<script>\s*\(function\(\)\{[^}]*_hubtick[^<]*</script>',
        '', body, flags=re.DOTALL
    )
    
    return body.strip()

def remove_div_by_class(html, class_name):
    """Remove the first <div class="CLASS"> block (handles nesting)."""
    patterns = [
        rf'<div\s+class="{class_name}"',
        rf"<div\s+class='{class_name}'",
        rf'<div\s+[^>]*class="[^"]*\b{class_name}\b[^"]*"',
    ]
    
    start = -1
    for pat in patterns:
        m = re.search(pat, html)
        if m:
            start = m.start()
            break
    
    if start < 0:
        return html
    
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
                return html[:start] + html[end:]
            pos = cl_pos + 6
    return html

# ─── Main Rewrite ─────────────────────────────────────────────────────────────
def rewrite(filepath, title, subtitle, footer_label, extra_css=''):
    fname = os.path.basename(filepath)
    print(f"\n{'─'*60}")
    print(f"  Rewriting: {fname}")
    print(f"{'─'*60}")

    with open(filepath, encoding='utf-8') as f:
        html = f.read()

    # ── Extract CDN scripts from <head> ──
    cdn_scripts = re.findall(
        r'<script\s+src=["\'][^"\']*(?:cdn|jsdelivr|cdnjs|unpkg)[^"\']*["\'][^>]*/?>',
        html, re.IGNORECASE
    )
    cdn_html = '\n  '.join(cdn_scripts)

    # ── Extract original page title ──
    t = re.search(r'<title>(.*?)</title>', html)
    page_title = t.group(1) if t else title

    # ── Extract style block ──
    sm = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    raw_style = sm.group(1) if sm else ''
    page_css = extract_page_css(raw_style)

    # ── Extract body content ──
    bm = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
    body = bm.group(1) if bm else html
    body = transform_body(body)

    # ── Remove old .header div from body ──
    body = remove_div_by_class(body, 'header')

    # ── Remove old .footer div from body (simple non-Hub footer) ──
    # Only remove if it's a simple text footer, not a complex one
    body = remove_div_by_class(body, 'footer')

    # ── Build output ──
    out = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  {cdn_html}
  <style>
/* ══════════════════════════════════════════════
   CM Brasil — Hub Design System
   Rewrite: {fname}
══════════════════════════════════════════════ */

{HUB_CSS}

/* ══════════════════════════════════════════════
   PAGE-SPECIFIC STYLES — {title}
══════════════════════════════════════════════ */
{page_css}

/* ══════════════════════════════════════════════
   EXTRA OVERRIDES
══════════════════════════════════════════════ */
{extra_css}

/* ─── Container/wrapper reset ─── */
.container, .wrapper, .app, #app {{
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}}
  </style>
</head>
<body>

{make_header(title, subtitle)}

<div class="page-body">

{body}

</div>

{make_footer(footer_label)}

</body>
</html>'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(out)

    size = os.path.getsize(filepath)
    print(f"  ✓ Done — {size:,} bytes")


# ─── Dashboard configs ────────────────────────────────────────────────────────
DASHBOARDS = [
    {
        'file': 'CM_Brasil_MasterDeck.html',
        'title': 'MasterDeck',
        'subtitle': 'Cooler Master Brasil — Visão 360° do Negócio',
        'footer_label': 'Sell-In · Sell-Out · Clientes · Pipeline · Insights',
        'extra_css': '''
/* MasterDeck: restore tab bar styling */
.tabs { display:flex; gap:0; border-bottom:1px solid var(--border); margin-bottom:0; padding:8px 0 0; background:var(--bg); position:sticky; top:72px; z-index:100; }
.tab-btn { padding:9px 18px; font-size:0.82rem; font-weight:500; color:var(--text-3); background:transparent; border:none; border-bottom:2px solid transparent; margin-bottom:-1px; cursor:pointer; transition:color 0.15s,border-color 0.15s; font-family:inherit; white-space:nowrap; }
.tab-btn:hover { color:var(--text-2); }
.tab-btn.active { color:var(--text); border-bottom-color:var(--accent); }

/* KPI cards */
.grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px; }
.grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:24px; }
.grid-2 { display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin-bottom:24px; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; position:relative; overflow:hidden; }
.card::before { content:''; position:absolute; top:0;left:0;right:0; height:1px; background:linear-gradient(90deg,transparent,var(--accent),transparent); opacity:0; transition:opacity 0.2s; }
.card:hover { border-color:var(--border-hover); background:var(--surface-hover); box-shadow:0 4px 20px rgba(0,0,0,0.3); }
.card:hover::before { opacity:1; }
.card-value { font-size:1.8rem; font-weight:700; letter-spacing:-0.5px; color:var(--text); }
.card-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; }
.card-title { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-3); }
.card-sub { font-size:0.75rem; color:var(--text-3); margin-top:6px; }
.kpi-card.green .accent-bar { background:var(--green); }
.kpi-card.blue .accent-bar { background:var(--blue); }
.kpi-card.red .accent-bar { background:var(--red); }
.kpi-card.orange .accent-bar { background:var(--orange); }
.kpi-card.yellow .accent-bar { background:var(--yellow); }
.kpi-card.purple .accent-bar { background:var(--accent); }
.accent-bar { width:3px; position:absolute; left:0; top:0; bottom:0; border-radius:12px 0 0 12px; }

/* Alert boxes */
.alert { display:flex; gap:14px; padding:16px; border-radius:12px; margin-bottom:20px; border:1px solid; }
.alert-red { background:var(--red-dim); border-color:rgba(239,68,68,0.3); }
.alert-yellow { background:var(--yellow-dim); border-color:rgba(234,179,8,0.3); }
.alert-green { background:var(--green-dim); border-color:rgba(34,197,94,0.3); }
.alert-blue { background:var(--blue-glow); border-color:rgba(59,130,246,0.3); }
.alert-icon { font-size:1.5rem; flex-shrink:0; }
.alert-title { font-size:0.9rem; font-weight:600; color:var(--text); margin-bottom:4px; }
.alert-text { font-size:0.8rem; color:var(--text-2); }

/* Section title */
.section { margin-bottom:32px; }
.section-title { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; color:var(--text-3); margin-bottom:14px; display:flex; align-items:center; gap:8px; }
.section-title::after { content:''; flex:1; height:1px; background:var(--border); opacity:0.7; }

/* Chart containers */
.chart-container { position:relative; }
.chart-card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:16px; }
.chart-title { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-3); margin-bottom:16px; }

/* Tab content */
.tab-content { display:none; padding-top:28px; }
.tab-content.active { display:block; }

/* Period filter */
.period-filter { display:flex; gap:6px; align-items:center; flex-wrap:wrap; }
.filter-btn { padding:4px 12px; font-size:0.78rem; color:var(--text-3); background:transparent; border:1px solid var(--border); border-radius:999px; cursor:pointer; transition:all 0.15s; font-family:inherit; font-weight:500; }
.filter-btn:hover { color:var(--text-2); border-color:var(--border-hover); }
.filter-btn.active { color:var(--text); background:var(--surface); border-color:var(--accent); box-shadow:0 0 0 1px var(--accent); }

/* Tables */
.table-wrap { background:var(--surface); border:1px solid var(--border); border-radius:12px; overflow:hidden; margin-bottom:16px; }

/* Insight boxes */
.insight-box, .insight { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--blue); border-radius:0 8px 8px 0; padding:12px 16px; font-size:0.82rem; color:var(--text-2); margin:8px 0; }
.insight-box.warn, .insight.warn { border-left-color:var(--yellow); }
.insight-box.danger, .insight.danger { border-left-color:var(--red); }
.insight-box.success, .insight.success { border-left-color:var(--green); }

@media(max-width:900px){ .grid-4{grid-template-columns:repeat(2,1fr);} .grid-3{grid-template-columns:repeat(2,1fr);} }
@media(max-width:480px){ .grid-4,.grid-3,.grid-2{grid-template-columns:1fr;} .tabs{flex-wrap:wrap;} }
''',
    },
    {
        'file': 'CM_Simulador_Precos.html',
        'title': 'Simulador de Preços',
        'subtitle': 'Cooler Master Brasil — Precificação Completa',
        'footer_label': 'FOB · Varejo · Reverse · FUNDAP · TTD · Regimes Fiscais',
        'extra_css': '''
/* Simulador: tab bar */
.tabs { display:flex; gap:0; border-bottom:1px solid var(--border); margin-bottom:24px; }
.tab-btn { padding:9px 18px; font-size:0.82rem; font-weight:500; color:var(--text-3); background:transparent; border:none; border-bottom:2px solid transparent; margin-bottom:-1px; cursor:pointer; transition:all 0.15s; font-family:inherit; }
.tab-btn:hover { color:var(--text-2); }
.tab-btn.active { color:var(--text); border-bottom-color:var(--accent); }
.tab-content { display:none; }
.tab-content.active { display:block; }

/* Input/form styles */
.form-group { margin-bottom:16px; }
.form-label { font-size:0.78rem; font-weight:600; color:var(--text-2); margin-bottom:6px; display:block; }
.form-row { display:grid; grid-template-columns:repeat(2,1fr); gap:16px; margin-bottom:16px; }
.form-row-3 { grid-template-columns:repeat(3,1fr); }
input[type=number], input[type=text], select { width:100%; }

/* Result card */
.result-card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:16px; }
.result-title { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-3); margin-bottom:12px; }
.result-value { font-size:1.6rem; font-weight:700; color:var(--text); }

/* Breakdown table */
.breakdown { background:var(--surface); border:1px solid var(--border); border-radius:12px; overflow:hidden; }

/* Section */
.section { margin-bottom:28px; }
.section-title { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; color:var(--text-3); margin-bottom:14px; display:flex; align-items:center; gap:8px; }
.section-title::after { content:''; flex:1; height:1px; background:var(--border); opacity:0.7; }

/* Card */
.card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:16px; }
''',
    },
    {
        'file': 'CM_FollowUp_Tracker.html',
        'title': 'Follow-up Tracker',
        'subtitle': 'Cooler Master Brasil — Pendências & Deadlines',
        'footer_label': 'Pendências · Deadlines · Follow-ups · Alertas',
        'extra_css': '''
/* FollowUp tracker-specific */
.section { margin-bottom:28px; }
.section-header { font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; color:var(--text-3); margin-bottom:14px; display:flex; align-items:center; gap:8px; }
.section-header::after { content:''; flex:1; height:1px; background:var(--border); opacity:0.7; }

/* Stats grid */
.stats { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:28px; }
.stat-card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; text-align:center; }
.stat-number { font-size:2.2rem; font-weight:700; color:var(--text); letter-spacing:-0.5px; }
.stat-label { font-size:0.72rem; color:var(--text-3); margin-top:6px; font-weight:500; }
.s-total { border-color: rgba(59,130,246,0.3); }
.s-total .stat-number { color: var(--blue); }
.s-critica { border-color: rgba(239,68,68,0.3); }
.s-critica .stat-number { color: var(--red); }
.s-overdue { border-color: rgba(234,179,8,0.3); }
.s-overdue .stat-number { color: var(--yellow); }
.s-done { border-color: rgba(34,197,94,0.3); }
.s-done .stat-number { color: var(--green); }

/* Two-col layout */
.two-col { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:28px; }

/* Timeline */
.timeline { display:flex; flex-direction:column; gap:10px; }
.timeline-item { display:flex; align-items:flex-start; gap:12px; padding:10px 0; border-bottom:1px solid var(--border); }
.timeline-date { min-width:100px; flex-shrink:0; }
.tl-date { font-size:0.8rem; color:var(--text-2); font-family:'Menlo','SF Mono',monospace; }
.tl-days { font-size:0.72rem; margin-top:2px; font-weight:600; }
.tl-title { font-size:0.85rem; color:var(--text-2); }

/* Companies */
.companies-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; }
.company-card { background:var(--bg); border:1px solid var(--border); border-radius:8px; padding:12px; }
.company-name { font-size:0.85rem; font-weight:600; color:var(--text); margin-bottom:6px; }
.company-items { list-style:none; padding:0; }
.company-items li { font-size:0.78rem; color:var(--text-3); padding:2px 0; }
.muted { color:var(--text-3); }
.small { font-size:0.72em; }
.mini-badge { display:inline-flex; font-size:0.6rem; padding:1px 6px; border-radius:999px; margin-left:4px; }
.mini-badge.crit { background:var(--red-dim); color:var(--red); }
.mini-badge.alta { background:var(--orange-dim); color:var(--orange); }
.mini-badge.media { background:var(--yellow-dim); color:var(--yellow); }

/* Main table */
.table-wrapper { background:var(--surface); border:1px solid var(--border); border-radius:12px; overflow:auto; }

/* Status pills */
.status-pill { display:inline-flex; font-size:0.68rem; font-weight:600; padding:2px 8px; border-radius:999px; text-transform:uppercase; letter-spacing:0.05em; }
.status-critica { background:var(--red-dim); color:var(--red); }
.status-alta { background:var(--orange-dim); color:var(--orange); }
.status-media { background:var(--yellow-dim); color:var(--yellow); }
.status-baixa { background:var(--blue-glow); color:var(--blue); }
.status-done { background:var(--green-dim); color:var(--green); }

@media(max-width:900px){ .stats{grid-template-columns:repeat(2,1fr);} .two-col{grid-template-columns:1fr;} .companies-grid{grid-template-columns:1fr;} }
@media(max-width:480px){ .stats{grid-template-columns:1fr;} }
''',
    },
    {
        'file': 'CM_Catalogo_Dashboard.html',
        'title': 'Catálogo de Produtos',
        'subtitle': 'Cooler Master Brasil — Packing List & KaBuM',
        'footer_label': 'Catálogo · SKUs · Fabricantes · Preços · Estoque',
        'extra_css': '''
/* Catalogo: search bar */
.search-bar { position:relative; margin-bottom:24px; }
.search-bar input { width:100%; max-width:480px; padding:10px 16px 10px 40px; border-radius:999px; }
.search-bar-icon { position:absolute; left:14px; top:50%; transform:translateY(-50%); color:var(--text-3); pointer-events:none; }
.filters { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:20px; }

/* Table styles */
.table-container { background:var(--surface); border:1px solid var(--border); border-radius:12px; overflow:auto; }

/* Chart wrap */
.chart-wrap { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:16px; }

/* KPI row */
.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px; }
.kpi-card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px 20px; }
.kpi-value { font-size:1.7rem; font-weight:700; letter-spacing:-0.4px; }
.kpi-label { font-size:0.72rem; color:var(--text-3); font-weight:500; margin-top:4px; }
.kpi-value.green { color:var(--green); }
.kpi-value.blue { color:var(--blue); }
.kpi-value.yellow { color:var(--yellow); }
.kpi-value.red { color:var(--red); }
.kpi-value.purple { color:var(--accent); }

/* Tabs */
.tab-nav { display:flex; gap:0; border-bottom:1px solid var(--border); margin-bottom:24px; }
.tab-btn, .tab { padding:9px 18px; font-size:0.82rem; font-weight:500; color:var(--text-3); background:transparent; border:none; border-bottom:2px solid transparent; margin-bottom:-1px; cursor:pointer; transition:all 0.15s; font-family:inherit; }
.tab-btn:hover, .tab:hover { color:var(--text-2); }
.tab-btn.active, .tab.active { color:var(--text); border-bottom-color:var(--accent); }
.tab-content { display:none; }
.tab-content.active { display:block; }

@media(max-width:900px){ .kpi-row{grid-template-columns:repeat(2,1fr);} }
@media(max-width:480px){ .kpi-row{grid-template-columns:1fr;} }
''',
    },
    {
        'file': 'Organograma_CM.html',
        'title': 'Organograma CM',
        'subtitle': 'Cooler Master Brasil — Estrutura Organizacional',
        'footer_label': 'Organograma · Equipe · Hierarquia · Responsabilidades',
        'extra_css': '''
/* Organograma dark theme */
.org-container { padding:28px; }
.org-tree { display:flex; flex-direction:column; align-items:center; }

/* Org boxes — Hub card style */
.org-box, .org-node {
  background:var(--surface); border:1px solid var(--border); border-radius:10px;
  padding:14px 20px; text-align:center; min-width:160px; max-width:220px;
  transition:border-color 0.15s, box-shadow 0.15s;
  position:relative;
}
.org-box:hover, .org-node:hover {
  border-color:var(--border-hover);
  box-shadow:0 4px 16px rgba(0,0,0,0.3);
}
.org-box.root, .org-node.root {
  background:linear-gradient(135deg,#18181b,#1a1625);
  border-color:rgba(124,58,237,0.35);
  min-width:200px;
}
.org-name { font-size:0.88rem; font-weight:600; color:var(--text); }
.org-title, .org-role { font-size:0.72rem; color:var(--text-3); margin-top:3px; }
.org-dept { font-size:0.68rem; color:var(--accent); font-weight:500; margin-top:2px; }

/* Connector lines */
.org-connector { width:2px; height:24px; background:var(--border); margin:0 auto; }
.org-row { display:flex; gap:16px; justify-content:center; align-items:flex-start; }
.org-col { display:flex; flex-direction:column; align-items:center; }

/* Chart */
.chart-wrap { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; }
''',
    },
    {
        'file': 'dashboard_sellin.html',
        'title': 'Dashboard Sell-In',
        'subtitle': 'Cooler Master Brasil — Vendas, Buffer & Backorders',
        'footer_label': 'Sell-In · Buffer · Backorders · Pedidos por Período',
        'extra_css': '''
/* Sellin: grid and card styles */
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin-bottom:24px; }
.card, .card-box { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; }
.card:hover, .card-box:hover { border-color:var(--border-hover); box-shadow:0 4px 16px rgba(0,0,0,0.25); }
h2 { font-size:0.9rem; font-weight:600; color:var(--text); margin-bottom:12px; }
h3 { font-size:0.8rem; color:var(--blue); margin:12px 0 6px; }
.full { grid-column:1/-1; }
.kpi-row { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:24px; }
.kpi { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; text-align:center; }
.kpi .value { font-size:1.8rem; font-weight:700; color:var(--text); }
.kpi .label { color:var(--text-3); font-size:0.75rem; margin-top:4px; }
.kpi.green .value { color:var(--green); }
.kpi.red .value { color:var(--red); }
.kpi.yellow .value { color:var(--yellow); }
.kpi.blue .value { color:var(--blue); }
.chart-container { position:relative; height:280px; }
.insight-box, .insight { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--blue); border-radius:0 8px 8px 0; padding:12px 16px; font-size:0.82rem; color:var(--text-2); margin:8px 0; }
.insight-box.warn { border-left-color:var(--yellow); }
.insight-box.danger { border-left-color:var(--red); }
.insight-box.success { border-left-color:var(--green); }
.timeline { position:relative; }
.timeline-item { display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid var(--border); }
.timeline-dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
.progress-bar { background:var(--border); border-radius:6px; height:16px; overflow:hidden; }
.progress-fill { height:100%; border-radius:6px; transition:width 0.5s; }
.tabs { display:flex; gap:4px; margin-bottom:12px; }
.tab { padding:6px 14px; border-radius:8px 8px 0 0; cursor:pointer; background:var(--surface); color:var(--text-3); border:1px solid var(--border); border-bottom:none; font-size:0.82rem; font-family:inherit; }
.tab.active { color:var(--text); border-color:var(--accent); border-bottom-color:var(--surface); }
.tab-content { display:none; } .tab-content.active { display:block; }
''',
    },
    {
        'file': 'dashboard_sellout.html',
        'title': 'Dashboard Sell-Out',
        'subtitle': 'Cooler Master Brasil — KaBuM · Pichau · Terabyte',
        'footer_label': 'Sell-Out · KaBuM · Pichau · Terabyte · Semanal por Canal',
        'extra_css': '''
/* Sellout: same as sellin */
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin-bottom:24px; }
.card, .card-box { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; }
.card:hover { border-color:var(--border-hover); box-shadow:0 4px 16px rgba(0,0,0,0.25); }
h2 { font-size:0.9rem; font-weight:600; color:var(--text); margin-bottom:12px; }
h3 { font-size:0.8rem; color:var(--blue); margin:12px 0 6px; }
.full { grid-column:1/-1; }
.kpi-row { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:24px; }
.kpi { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; text-align:center; }
.kpi .value { font-size:1.8rem; font-weight:700; color:var(--text); }
.kpi .label { color:var(--text-3); font-size:0.75rem; margin-top:4px; }
.kpi.green .value { color:var(--green); }
.kpi.red .value { color:var(--red); }
.kpi.yellow .value { color:var(--yellow); }
.kpi.blue .value { color:var(--blue); }
.chart-container { position:relative; height:280px; }
.insight-box, .insight { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--blue); border-radius:0 8px 8px 0; padding:12px 16px; font-size:0.82rem; color:var(--text-2); margin:8px 0; }
.insight-box.warn { border-left-color:var(--yellow); }
.insight-box.danger { border-left-color:var(--red); }
.insight-box.success { border-left-color:var(--green); }
.badge { display:inline-flex; font-size:0.68rem; padding:2px 8px; border-radius:999px; border:1px solid transparent; }
.badge.green { background:var(--green-dim); color:var(--green); border-color:rgba(34,197,94,0.25); }
.badge.red { background:var(--red-dim); color:var(--red); }
.badge.yellow { background:var(--yellow-dim); color:var(--yellow); }
.badge.blue { background:var(--blue-glow); color:var(--blue); }
''',
    },
    {
        'file': 'Dashboard_CM_Brasil_2026.html',
        'title': 'Dashboard 2026',
        'subtitle': 'Cooler Master Brasil — Visão Consolidada do Ano',
        'footer_label': 'Metas 2026 · Tendências · Performance · Forecasts',
        'extra_css': '''
/* 2026 dashboard */
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin-bottom:24px; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; }
.card:hover { border-color:var(--border-hover); box-shadow:0 4px 16px rgba(0,0,0,0.25); }
h2 { font-size:0.9rem; font-weight:600; color:var(--text); margin-bottom:12px; }
h3 { font-size:0.8rem; color:var(--blue); margin:12px 0 6px; }
.full { grid-column:1/-1; }
.kpi-row { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:24px; }
.kpi { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; text-align:center; }
.kpi .value { font-size:1.8rem; font-weight:700; color:var(--text); }
.kpi .label { color:var(--text-3); font-size:0.75rem; margin-top:4px; }
.kpi.green .value { color:var(--green); }
.kpi.red .value { color:var(--red); }
.kpi.yellow .value { color:var(--yellow); }
.kpi.blue .value { color:var(--blue); }
.chart-container { position:relative; height:280px; }
.insight-box { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--blue); border-radius:0 8px 8px 0; padding:12px 16px; font-size:0.82rem; color:var(--text-2); margin:8px 0; }
.insight-box.warn { border-left-color:var(--yellow); }
.insight-box.danger { border-left-color:var(--red); }
.insight-box.success { border-left-color:var(--green); }
''',
    },
    {
        'file': 'CM_Forecast_Dashboard.html',
        'title': 'Forecast & Reorder',
        'subtitle': 'Cooler Master Brasil — Timeline, Alertas & Projeções',
        'footer_label': 'Forecast · Reorder · 218 SKUs · 7 Canais · Timeline',
        'extra_css': '''
/* Forecast dashboard */
.tabs { display:flex; gap:0; border-bottom:1px solid var(--border); margin-bottom:24px; }
.tab-btn, .tab { padding:9px 18px; font-size:0.82rem; font-weight:500; color:var(--text-3); background:transparent; border:none; border-bottom:2px solid transparent; margin-bottom:-1px; cursor:pointer; transition:all 0.15s; font-family:inherit; }
.tab-btn:hover, .tab:hover { color:var(--text-2); }
.tab-btn.active, .tab.active { color:var(--text); border-bottom-color:var(--accent); }
.tab-content { display:none; }
.tab-content.active { display:block; }

.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin-bottom:24px; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; }
h2 { font-size:0.9rem; font-weight:600; color:var(--text); margin-bottom:12px; }
.full { grid-column:1/-1; }
.kpi-row { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:24px; }
.kpi { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; text-align:center; }
.kpi .value { font-size:1.8rem; font-weight:700; color:var(--text); }
.kpi .label { color:var(--text-3); font-size:0.75rem; margin-top:4px; }
.kpi.green .value { color:var(--green); }
.kpi.red .value { color:var(--red); }
.kpi.yellow .value { color:var(--yellow); }
.kpi.blue .value { color:var(--blue); }
.chart-container { position:relative; height:280px; }
.insight-box { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--blue); border-radius:0 8px 8px 0; padding:12px 16px; font-size:0.82rem; color:var(--text-2); margin:8px 0; }
.insight-box.warn { border-left-color:var(--yellow); }
.insight-box.danger { border-left-color:var(--red); }
.insight-box.success { border-left-color:var(--green); }
.timeline-item { display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid var(--border); }
.timeline-dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
.progress-bar { background:var(--border); border-radius:6px; height:16px; overflow:hidden; }
.progress-fill { height:100%; border-radius:6px; transition:width 0.5s; }
''',
    },
    {
        'file': 'CM_Playbook_Processos.html',
        'title': 'Playbook de Processos',
        'subtitle': 'Cooler Master Brasil — SOPs, Workflows & Automações',
        'footer_label': 'Processos · SOPs · Workflows · Automações · Checklists',
        'extra_css': '''
/* Playbook */
.tabs { display:flex; gap:0; border-bottom:1px solid var(--border); margin-bottom:24px; }
.tab-btn, .tab { padding:9px 18px; font-size:0.82rem; font-weight:500; color:var(--text-3); background:transparent; border:none; border-bottom:2px solid transparent; margin-bottom:-1px; cursor:pointer; transition:all 0.15s; font-family:inherit; }
.tab-btn:hover, .tab:hover { color:var(--text-2); }
.tab-btn.active, .tab.active { color:var(--text); border-bottom-color:var(--accent); }
.tab-content { display:none; }
.tab-content.active { display:block; }

.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin-bottom:24px; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:20px; }
.card:hover { border-color:var(--border-hover); }
h2 { font-size:0.9rem; font-weight:600; color:var(--text); margin-bottom:12px; }
h3 { font-size:0.8rem; color:var(--blue); margin:12px 0 6px; }

/* Process steps */
.step { display:flex; gap:14px; padding:12px 0; border-bottom:1px solid var(--border); }
.step-num { width:26px; height:26px; border-radius:50%; background:var(--accent); display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:700; color:#fff; flex-shrink:0; }
.step-content { flex:1; }
.step-title { font-size:0.88rem; font-weight:600; color:var(--text); }
.step-desc { font-size:0.78rem; color:var(--text-3); margin-top:3px; }

/* Checklist */
.checklist { list-style:none; padding:0; }
.checklist li { display:flex; align-items:flex-start; gap:8px; padding:6px 0; font-size:0.85rem; color:var(--text-2); border-bottom:1px solid rgba(39,39,42,0.5); }
.checklist li:last-child { border-bottom:none; }
.check-icon { color:var(--green); flex-shrink:0; margin-top:1px; }

/* Alert */
.alert-box { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--blue); border-radius:0 8px 8px 0; padding:12px 16px; font-size:0.82rem; color:var(--text-2); margin:8px 0; }
.alert-box.warn { border-left-color:var(--yellow); }
.alert-box.danger { border-left-color:var(--red); }
.alert-box.success { border-left-color:var(--green); }
''',
    },
]


def main():
    print("CM Brasil — Hub Design System Rewrite")
    print(f"Workspace : {WORKSPACE}")
    print(f"OneDrive  : {ONEDRIVE}")

    success, errors = [], []

    for cfg in DASHBOARDS:
        fp = os.path.join(WORKSPACE, cfg['file'])
        if not os.path.exists(fp):
            print(f"\n⚠  File not found: {cfg['file']}")
            errors.append(cfg['file'])
            continue
        try:
            rewrite(fp, cfg['title'], cfg['subtitle'],
                    cfg['footer_label'], cfg.get('extra_css', ''))
            success.append(cfg['file'])
        except Exception as e:
            import traceback
            print(f"\n✗ Error — {cfg['file']}: {e}")
            traceback.print_exc()
            errors.append(cfg['file'])

    # ── Copy to OneDrive ──
    print(f"\n{'─'*60}")
    print("Syncing to OneDrive...")
    os.makedirs(ONEDRIVE, exist_ok=True)
    for fn in success:
        src = os.path.join(WORKSPACE, fn)
        dst = os.path.join(ONEDRIVE, fn)
        try:
            shutil.copy2(src, dst)
            print(f"  ✓ {fn}")
        except Exception as e:
            print(f"  ✗ {fn}: {e}")

    print(f"\n{'─'*60}")
    print(f"COMPLETE — ✓ {len(success)} rewrites, ✗ {len(errors)} errors")
    if errors:
        print(f"Errors: {', '.join(errors)}")


if __name__ == '__main__':
    main()
