#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║  Cooler Master Brasil — Follow-up Tracker        ║
║  tracker.py  |  v1.0  |  2026-02-17              ║
╚══════════════════════════════════════════════════╝

Uso:
  python tracker.py --status
  python tracker.py --alertas
  python tracker.py --add
  python tracker.py --add --json '{"titulo": "...", "prioridade": "alta", ...}'
  python tracker.py --update 215d63f1 --status aguardando --notas "Enviado email"
  python tracker.py --complete 215d63f1
  python tracker.py --relatorio
  python tracker.py --relatorio --output relatorio.md
  python tracker.py --dashboard
  python tracker.py --dashboard --output ../CM_FollowUp_Tracker.html
"""

import json
import uuid
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path
import sys
import textwrap

# ─── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
DATA_FILE   = SCRIPT_DIR / "followups.json"
DEFAULT_HTML = SCRIPT_DIR.parent / "CM_FollowUp_Tracker.html"

# ─── Constants ────────────────────────────────────────────────────────────────
PRIORITY_WEIGHT = {"critica": 4, "alta": 3, "media": 2, "baixa": 1}

TIPO_LABELS = {
    "deadline":           "📅 Deadline",
    "aguardando_resposta": "⏳ Aguardando Resposta",
    "cobranca":           "💰 Cobrança",
    "acao_interna":       "🔧 Ação Interna",
}

STATUS_LABELS = {
    "aberto":    "⬤ ABERTO",
    "aguardando": "⏳ AGUARDANDO",
    "concluido": "✅ CONCLUÍDO",
    "cancelado": "✖ CANCELADO",
}

# ─── Terminal Colors ───────────────────────────────────────────────────────────
class C:
    RED     = "\033[91m"
    ORANGE  = "\033[38;5;208m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"

def c_priority(p):
    m = {"critica": C.RED + C.BOLD, "alta": C.ORANGE, "media": C.YELLOW, "baixa": C.GRAY}
    l = {"critica": "🔴 CRÍTICA", "alta": "🟠 ALTA", "media": "🟡 MÉDIA", "baixa": "🟢 BAIXA"}
    return f"{m.get(p, C.WHITE)}{l.get(p, p.upper())}{C.RESET}"

def c_status(s):
    m = {"aberto": C.RED, "aguardando": C.YELLOW, "concluido": C.GREEN, "cancelado": C.GRAY}
    return f"{m.get(s, C.WHITE)}{STATUS_LABELS.get(s, s.upper())}{C.RESET}"

# ─── Data Helpers ─────────────────────────────────────────────────────────────
def load_data():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{C.DIM}💾 Salvo em {DATA_FILE}{C.RESET}")

def calc_days_since(date_str):
    """Days elapsed since date_str (positive = past)"""
    if not date_str:
        return None
    try:
        return (date.today() - date.fromisoformat(date_str)).days
    except Exception:
        return None

def calc_days_until(date_str):
    """Days remaining until date_str (negative = overdue)"""
    if not date_str:
        return None
    try:
        return (date.fromisoformat(date_str) - date.today()).days
    except Exception:
        return None

def find_item(data, id_prefix):
    """Find item by full UUID or short prefix."""
    for item in data:
        if item["id"] == id_prefix or item["id"].startswith(id_prefix):
            return item
    return None

# ─── Urgency & Alerts ─────────────────────────────────────────────────────────
def urgency_score(item):
    """Higher score = more urgent. Used for sorting."""
    score = PRIORITY_WEIGHT.get(item.get("prioridade", "media"), 2) * 100

    days_dl = calc_days_until(item.get("deadline"))
    if days_dl is not None:
        if days_dl < 0:    score += 600   # overdue
        elif days_dl == 0: score += 500   # today
        elif days_dl == 1: score += 450   # tomorrow
        elif days_dl <= 3: score += 350   # ≤3 days
        elif days_dl <= 7: score += 200   # ≤7 days

    days_no_reply = calc_days_since(item.get("ultimo_contato"))
    if days_no_reply is not None:
        if days_no_reply >= 10: score += 150
        elif days_no_reply >= 5: score += 75

    return score

def get_alerts(item):
    """Return list of (level, message) tuples sorted by severity."""
    alerts = []
    days_dl = calc_days_until(item.get("deadline"))
    days_nr = calc_days_since(item.get("ultimo_contato"))

    if days_dl is not None:
        if days_dl < 0:
            alerts.append((0, "CRÍTICO 🔴", f"Deadline VENCIDO há {abs(days_dl)} dia(s)!"))
        elif days_dl == 0:
            alerts.append((0, "CRÍTICO 🔴", "Deadline é HOJE!"))
        elif days_dl == 1:
            alerts.append((1, "CRÍTICO",   "Deadline AMANHÃ!"))
        elif days_dl <= 3:
            alerts.append((2, "ALTO",      f"Deadline em {days_dl} dias"))

    if days_nr is not None:
        if days_nr >= 10:
            alerts.append((2, "ALTO",  f"Sem resposta há {days_nr} dias"))
        elif days_nr >= 5:
            alerts.append((3, "MÉDIO", f"Sem resposta há {days_nr} dias"))

    alerts.sort(key=lambda x: x[0])
    return [(lv, msg) for (_, lv, msg) in alerts]

def top_alert(item):
    """Return (level, message) of highest-priority alert, or (None, None)."""
    alerts = get_alerts(item)
    return alerts[0] if alerts else (None, None)

# ─── Commands ─────────────────────────────────────────────────────────────────
def cmd_status(args):
    data = load_data()
    active = [i for i in data if i.get("status") in ("aberto", "aguardando")]
    if not active:
        print(f"\n{C.GREEN}✅  Nenhuma pendência aberta!{C.RESET}")
        return

    active.sort(key=urgency_score, reverse=True)
    today_str = date.today().strftime("%d/%m/%Y")

    print(f"\n{C.BOLD}{C.CYAN}╔══════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}║  🎯  COOLER MASTER BRASIL — FOLLOW-UP TRACKER            ║{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}║  {today_str}  •  {len(active)} pendência(s) aberta(s)                   ║{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}╚══════════════════════════════════════════════════════════╝{C.RESET}\n")

    for idx, item in enumerate(active, 1):
        days_dl  = calc_days_until(item.get("deadline"))
        days_nr  = calc_days_since(item.get("ultimo_contato"))
        al_level, al_msg = top_alert(item)

        # Header
        print(f"{C.BOLD}[{idx:02d}] {item['titulo']}{C.RESET}")
        short_id = item["id"][:8]
        print(f"      {C.GRAY}#{short_id}{C.RESET}  {c_priority(item.get('prioridade','media'))}  {c_status(item.get('status','aberto'))}")

        # Contact / company
        contact = item.get("contato", "")
        empresa = item.get("empresa", "")
        if contact or empresa:
            line = "👤 " + " | ".join(x for x in [contact, empresa] if x)
            print(f"      {line}")

        # Deadline
        if item.get("deadline"):
            if days_dl is None:
                dl_str = f"📅 {item['deadline']}"
            elif days_dl < 0:
                dl_str = f"{C.RED}📅 {item['deadline']} — VENCIDO há {abs(days_dl)}d{C.RESET}"
            elif days_dl <= 1:
                dl_str = f"{C.RED}📅 {item['deadline']} — {days_dl}d{C.RESET}"
            elif days_dl <= 3:
                dl_str = f"{C.YELLOW}📅 {item['deadline']} — {days_dl}d{C.RESET}"
            else:
                dl_str = f"📅 {item['deadline']} — {days_dl}d"
            print(f"      {dl_str}")

        # Days without reply
        if days_nr is not None and days_nr > 0:
            nr_color = C.RED if days_nr >= 10 else C.YELLOW if days_nr >= 5 else C.DIM
            print(f"      {nr_color}⏱  Sem resposta: {days_nr} dias{C.RESET}")

        # Notes (wrapped)
        if item.get("notas"):
            note = item["notas"][:120] + ("…" if len(item.get("notas","")) > 120 else "")
            print(f"      {C.DIM}📝 {note}{C.RESET}")

        # Alert
        if al_level:
            ac = C.RED if "CRÍT" in al_level else C.YELLOW
            print(f"      {ac}⚠️  {al_level}: {al_msg}{C.RESET}")

        print()

    # Summary footer
    criticos = sum(1 for i in active if i.get("prioridade") == "critica")
    altos    = sum(1 for i in active if i.get("prioridade") == "alta")
    vencidos = sum(1 for i in active if calc_days_until(i.get("deadline")) is not None
                                         and calc_days_until(i.get("deadline")) < 0)
    print(f"{C.DIM}─── Resumo: {len(active)} abertas · {C.RED}{criticos} críticas{C.DIM} · "
          f"{C.ORANGE}{altos} altas{C.DIM} · {C.RED}{vencidos} vencidas{C.RESET}")
    print()


def cmd_alertas(args):
    data  = load_data()
    today = date.today().strftime("%d/%m/%Y")
    active = [i for i in data if i.get("status") in ("aberto", "aguardando")]

    buckets = {"CRÍTICO 🔴": [], "CRÍTICO": [], "ALTO": [], "MÉDIO": []}
    for item in active:
        for level, msg in get_alerts(item):
            if level in buckets:
                buckets[level].append((item, msg))
                break  # only highest alert per item

    all_alerts = (buckets["CRÍTICO 🔴"] + buckets["CRÍTICO"] +
                  buckets["ALTO"] + buckets["MÉDIO"])

    print(f"\n{C.BOLD}🚨  ALERTAS DO DIA — {today}{C.RESET}\n")

    if not all_alerts:
        print(f"{C.GREEN}✅  Nenhum alerta crítico hoje!{C.RESET}\n")
        return

    for bucket_label, items_list in [
        ("CRÍTICO 🔴", buckets["CRÍTICO 🔴"]),
        ("CRÍTICO",    buckets["CRÍTICO"]),
        ("ALTO",       buckets["ALTO"]),
        ("MÉDIO",      buckets["MÉDIO"]),
    ]:
        if not items_list:
            continue
        color = C.RED if "CRÍT" in bucket_label else C.YELLOW
        print(f"{color}{C.BOLD}{bucket_label} ({len(items_list)}){C.RESET}")
        for item, msg in items_list:
            empresa = f" [{item.get('empresa','')}]" if item.get("empresa") else ""
            print(f"   • {item['titulo']}{C.GRAY}{empresa}{C.RESET}")
            print(f"     {C.DIM}↳ {msg}{C.RESET}")
        print()


def cmd_add(args):
    data = load_data()
    today = date.today().isoformat()
    new_item = {}

    if getattr(args, "json_data", None):
        try:
            new_item = json.loads(args.json_data)
        except json.JSONDecodeError as e:
            print(f"{C.RED}Erro no JSON: {e}{C.RESET}")
            sys.exit(1)
    else:
        print(f"\n{C.CYAN}{C.BOLD}➕  Adicionar nova pendência{C.RESET}")
        print(f"{C.DIM}(Enter para pular campos opcionais){C.RESET}\n")
        new_item["titulo"]     = input("Título *: ").strip()
        if not new_item["titulo"]:
            print(f"{C.RED}Título é obrigatório.{C.RESET}")
            sys.exit(1)
        new_item["contato"]    = input("Contato: ").strip()
        new_item["empresa"]    = input("Empresa: ").strip()
        print("Tipo: deadline | aguardando_resposta | cobranca | acao_interna")
        new_item["tipo"]       = input("Tipo [aguardando_resposta]: ").strip() or "aguardando_resposta"
        print("Prioridade: critica | alta | media | baixa")
        new_item["prioridade"] = input("Prioridade [media]: ").strip() or "media"
        new_item["deadline"]   = input("Deadline YYYY-MM-DD (opcional): ").strip() or None
        new_item["notas"]      = input("Notas: ").strip()

    # Apply defaults
    new_item.setdefault("id",               str(uuid.uuid4()))
    new_item.setdefault("criado_em",        today)
    new_item.setdefault("ultimo_contato",   today)
    new_item.setdefault("dias_sem_resposta", None)
    new_item.setdefault("status",           "aberto")
    new_item.setdefault("alertas_enviados", 0)
    new_item.setdefault("deadline",         None)
    new_item.setdefault("contato",          "")
    new_item.setdefault("empresa",          "")
    new_item.setdefault("notas",            "")

    data.append(new_item)
    save_data(data)
    print(f"\n{C.GREEN}✅  Adicionado!{C.RESET}  ID: {new_item['id'][:8]}")


def cmd_update(args):
    data = load_data()
    item = find_item(data, args.id)
    if not item:
        print(f"{C.RED}Item não encontrado: {args.id}{C.RESET}")
        sys.exit(1)

    changed = False
    print(f"\n{C.CYAN}📝  Atualizando: {item['titulo']}{C.RESET}")

    if args.status:
        valid = ["aberto", "aguardando", "concluido", "cancelado"]
        if args.status not in valid:
            print(f"{C.RED}Status inválido. Use: {', '.join(valid)}{C.RESET}")
            sys.exit(1)
        item["status"] = args.status
        print(f"  status      → {args.status}")
        changed = True

    if args.notas:
        item["notas"] = args.notas
        print(f"  notas       → {args.notas}")
        changed = True

    if args.contato:
        item["ultimo_contato"] = date.today().isoformat()
        print(f"  ultimo_contato → {date.today().isoformat()} (hoje)")
        changed = True

    if args.prioridade:
        valid = ["critica", "alta", "media", "baixa"]
        if args.prioridade not in valid:
            print(f"{C.RED}Prioridade inválida. Use: {', '.join(valid)}{C.RESET}")
            sys.exit(1)
        item["prioridade"] = args.prioridade
        print(f"  prioridade  → {args.prioridade}")
        changed = True

    if args.deadline:
        item["deadline"] = args.deadline
        print(f"  deadline    → {args.deadline}")
        changed = True

    if changed:
        save_data(data)
        print(f"\n{C.GREEN}✅  Atualizado!{C.RESET}")
    else:
        print(f"{C.YELLOW}Nenhuma alteração especificada.{C.RESET}")
        print("Use: --status, --notas, --contato, --prioridade, --deadline")


def cmd_complete(args):
    data = load_data()
    item = find_item(data, args.id)
    if not item:
        print(f"{C.RED}Item não encontrado: {args.id}{C.RESET}")
        sys.exit(1)

    item["status"]         = "concluido"
    item["ultimo_contato"] = date.today().isoformat()
    save_data(data)
    print(f"\n{C.GREEN}✅  Concluído: {item['titulo']}{C.RESET}")


def cmd_relatorio(args):
    data  = load_data()
    today = date.today()

    active   = [i for i in data if i.get("status") in ("aberto", "aguardando")]
    done     = [i for i in data if i.get("status") == "concluido"]
    overdue  = [i for i in active if calc_days_until(i.get("deadline")) is not None
                                      and calc_days_until(i.get("deadline")) < 0]
    criticos = [i for i in active if i.get("prioridade") == "critica"]
    active.sort(key=urgency_score, reverse=True)

    lines = []
    lines.append(f"# 📋 Follow-up Report — Cooler Master Brasil")
    lines.append(f"_Gerado em: {today.strftime('%d/%m/%Y')} às {datetime.now().strftime('%H:%M')}_\n")
    lines.append("---\n")

    # Summary
    lines.append("## 📊 Resumo Executivo\n")
    lines.append("| Métrica | Valor |")
    lines.append("|---------|-------|")
    lines.append(f"| Pendências abertas | **{len(active)}** |")
    lines.append(f"| 🔴 Críticas | **{len(criticos)}** |")
    lines.append(f"| ⏰ Atrasadas | **{len(overdue)}** |")
    lines.append(f"| ✅ Concluídas | **{len(done)}** |")
    lines.append(f"| Total no sistema | **{len(data)}** |\n")

    # Alerts section
    lines.append("## 🚨 Alertas Ativos\n")
    alerta_items = []
    for item in active:
        for lv, msg in get_alerts(item):
            alerta_items.append((item, lv, msg))
            break
    if alerta_items:
        alerta_items.sort(key=lambda x: ["CRÍTICO 🔴","CRÍTICO","ALTO","MÉDIO"].index(x[1])
                         if x[1] in ["CRÍTICO 🔴","CRÍTICO","ALTO","MÉDIO"] else 9)
        for item, lv, msg in alerta_items:
            emoji = "🔴" if "CRÍT" in lv else "🟠" if lv == "ALTO" else "🟡"
            lines.append(f"- {emoji} **{lv}** — {item['titulo']} — _{msg}_")
    else:
        lines.append("_Nenhum alerta ativo._")
    lines.append("")

    # Critical items detail
    if criticos:
        lines.append("## 🔴 Itens Críticos\n")
        for item in criticos:
            lines.append(f"### {item['titulo']}")
            if item.get("contato") or item.get("empresa"):
                lines.append(f"- **Responsável:** {item.get('contato','-')} | {item.get('empresa','-')}")
            if item.get("deadline"):
                days = calc_days_until(item["deadline"])
                suffix = f" ({days}d)" if days is not None else ""
                lines.append(f"- **Deadline:** {item['deadline']}{suffix}")
            if item.get("notas"):
                lines.append(f"- **Notas:** {item['notas']}")
            lv, msg = top_alert(item)
            if lv:
                lines.append(f"- **⚠️ Alerta:** {lv} — {msg}")
            lines.append("")

    # All open items
    lines.append("## 📋 Todas as Pendências Abertas\n")
    p_emoji = {"critica": "🔴", "alta": "🟠", "media": "🟡", "baixa": "🟢"}
    for item in active:
        days_nr = calc_days_since(item.get("ultimo_contato"))
        lv, msg = top_alert(item)
        pe = p_emoji.get(item.get("prioridade","media"), "⚪")
        lines.append(f"### {pe} {item['titulo']}")
        lines.append(f"- **ID:** `{item['id'][:8]}`  |  "
                     f"**Tipo:** {TIPO_LABELS.get(item.get('tipo',''),item.get('tipo',''))}  |  "
                     f"**Status:** {item.get('status','').upper()}")
        lines.append(f"- **Prioridade:** {item.get('prioridade','').upper()}  |  "
                     f"**Empresa:** {item.get('empresa','-')}  |  "
                     f"**Contato:** {item.get('contato','-')}")
        if item.get("deadline"):
            lines.append(f"- **Deadline:** {item['deadline']}")
        if item.get("ultimo_contato"):
            lines.append(f"- **Último contato:** {item['ultimo_contato']}"
                         + (f" ({days_nr}d atrás)" if days_nr else ""))
        if item.get("notas"):
            lines.append(f"- **Notas:** {item['notas']}")
        if lv:
            lines.append(f"- **⚠️ Alerta:** {lv} — {msg}")
        lines.append("")

    # Done items
    if done:
        lines.append("## ✅ Concluídos\n")
        for item in done:
            lines.append(f"- ~~{item['titulo']}~~ _(concluído {item.get('ultimo_contato','')})_")
        lines.append("")

    lines.append("---")
    lines.append(f"_Follow-up Tracker • Cooler Master Brasil • {today.strftime('%d/%m/%Y')}_")

    report = "\n".join(lines)

    if getattr(args, "output", None):
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"{C.GREEN}✅  Relatório salvo: {args.output}{C.RESET}")
    else:
        print(report)


def cmd_dashboard(args):
    """Generate HTML dashboard with embedded data."""
    data  = load_data()
    today = date.today()
    active   = [i for i in data if i.get("status") in ("aberto", "aguardando")]
    done     = [i for i in data if i.get("status") == "concluido"]
    overdue  = [i for i in active if calc_days_until(i.get("deadline")) is not None
                                      and calc_days_until(i.get("deadline")) < 0]
    criticos = [i for i in active if i.get("prioridade") == "critica"]
    active.sort(key=urgency_score, reverse=True)

    data_json = json.dumps(data, ensure_ascii=False, indent=2)

    output_path = Path(getattr(args, "output", None) or DEFAULT_HTML)
    html = build_html(data, data_json, today, active, done, overdue, criticos)
    output_path.write_text(html, encoding="utf-8")
    print(f"{C.GREEN}✅  Dashboard gerado: {output_path}{C.RESET}")
    return output_path


# ─── HTML Builder ─────────────────────────────────────────────────────────────
def build_html(data, data_json, today, active, done, overdue, criticos):
    """Build the full HTML dashboard."""

    today_iso = today.isoformat()
    today_br  = today.strftime("%d/%m/%Y")

    # Build timeline data (next 14 days)
    timeline_items = []
    for item in active:
        if item.get("deadline"):
            d = calc_days_until(item["deadline"])
            if d is not None and d >= 0 and d <= 14:
                timeline_items.append({
                    "titulo": item["titulo"],
                    "deadline": item["deadline"],
                    "prioridade": item.get("prioridade", "media"),
                    "days": d,
                    "empresa": item.get("empresa", ""),
                })
    timeline_items.sort(key=lambda x: x["days"])

    # Build rows HTML
    rows_html = ""
    for item in active:
        days_dl = calc_days_until(item.get("deadline"))
        days_nr = calc_days_since(item.get("ultimo_contato"))
        lv, msg = top_alert(item)

        p = item.get("prioridade", "media")
        p_class = {"critica": "priority-critica", "alta": "priority-alta",
                   "media": "priority-media", "baixa": "priority-baixa"}.get(p, "")
        p_badge = {"critica": "🔴 CRÍTICA", "alta": "🟠 ALTA",
                   "media": "🟡 MÉDIA", "baixa": "🟢 BAIXA"}.get(p, p)

        s = item.get("status", "aberto")
        s_badge = STATUS_LABELS.get(s, s)
        s_class = {"aberto": "status-aberto", "aguardando": "status-aguardando",
                   "concluido": "status-concluido", "cancelado": "status-cancelado"}.get(s, "")

        dl_html = ""
        if item.get("deadline"):
            if days_dl is None:
                dl_html = item["deadline"]
            elif days_dl < 0:
                dl_html = f'<span class="deadline-overdue">📅 {item["deadline"]} (VENCIDO {abs(days_dl)}d)</span>'
            elif days_dl <= 1:
                dl_html = f'<span class="deadline-critical">📅 {item["deadline"]} ({days_dl}d)</span>'
            elif days_dl <= 3:
                dl_html = f'<span class="deadline-warn">📅 {item["deadline"]} ({days_dl}d)</span>'
            else:
                dl_html = f'📅 {item["deadline"]} ({days_dl}d)'
        else:
            dl_html = '<span class="muted">—</span>'

        nr_html = ""
        if days_nr is not None and days_nr > 0:
            nr_class = "nr-critical" if days_nr >= 10 else "nr-warn" if days_nr >= 5 else "nr-ok"
            nr_html = f'<span class="{nr_class}">{days_nr}d</span>'
        else:
            nr_html = '<span class="muted">—</span>'

        alert_html = ""
        if lv:
            a_class = "alert-critico" if "CRÍT" in lv else "alert-alto"
            alert_html = f'<span class="{a_class}">⚠️ {lv}</span>'

        notas_short = (item.get("notas", "")[:80] + "…") if len(item.get("notas","")) > 80 else item.get("notas","")

        rows_html += f"""
        <tr class="{p_class}">
          <td class="titulo-cell">
            <div class="titulo">{item['titulo']}</div>
            <div class="notas-small">{notas_short}</div>
            {alert_html}
          </td>
          <td><span class="badge {p_class}">{p_badge}</span></td>
          <td>{item.get('empresa','—')}<br><span class="muted small">{item.get('contato','')}</span></td>
          <td>{dl_html}</td>
          <td>{nr_html}</td>
          <td><span class="status-badge {s_class}">{s_badge}</span></td>
        </tr>"""

    # Timeline HTML
    timeline_html = ""
    if timeline_items:
        for t in timeline_items:
            p_color = {"critica": "#e63946", "alta": "#f97316",
                       "media": "#fbbf24", "baixa": "#22c55e"}.get(t["prioridade"], "#888")
            timeline_html += f"""
          <div class="timeline-item">
            <div class="timeline-date" style="border-left: 3px solid {p_color};">
              <div class="tl-date">{t['deadline']}</div>
              <div class="tl-days" style="color:{p_color}">+{t['days']}d</div>
            </div>
            <div class="tl-title">{t['titulo']}<span class="muted small"> [{t['empresa']}]</span></div>
          </div>"""
    else:
        timeline_html = '<div class="muted" style="padding:16px">Nenhum deadline nos próximos 14 dias</div>'

    # By company grouping
    companies = {}
    for item in active:
        emp = item.get("empresa") or "Sem empresa"
        companies.setdefault(emp, []).append(item)

    company_html = ""
    for emp, items_list in sorted(companies.items(), key=lambda x: -len(x[1])):
        c_criticas = sum(1 for i in items_list if i.get("prioridade") == "critica")
        c_altas    = sum(1 for i in items_list if i.get("prioridade") == "alta")
        badges = ""
        if c_criticas: badges += f'<span class="mini-badge crit">{c_criticas} crítica(s)</span>'
        if c_altas:    badges += f'<span class="mini-badge alta">{c_altas} alta(s)</span>'
        company_html += f"""
        <div class="company-card">
          <div class="company-name">{emp} <span class="muted small">({len(items_list)} pend.)</span> {badges}</div>
          <ul class="company-items">"""
        for it in sorted(items_list, key=urgency_score, reverse=True):
            p = it.get("prioridade","media")
            dot_color = {"critica":"#e63946","alta":"#f97316","media":"#fbbf24","baixa":"#22c55e"}.get(p,"#888")
            company_html += f'<li><span style="color:{dot_color}">●</span> {it["titulo"]}</li>'
        company_html += "</ul></div>"

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CM Brasil — Follow-up Tracker</title>
<style>
/* ── Reset & Base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: #0a0a0f;
  color: #e2e8f0;
  min-height: 100vh;
  font-size: 14px;
}}

/* ── Layout ── */
.container {{ max-width: 1400px; margin: 0 auto; padding: 24px 20px; }}

/* ── Header ── */
.header {{
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 28px; padding-bottom: 20px;
  border-bottom: 1px solid #1e293b;
}}
.header-left h1 {{
  font-size: 22px; font-weight: 700; letter-spacing: -0.5px;
  background: linear-gradient(135deg, #00d4ff, #4fc3f7);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.header-left .subtitle {{ color: #64748b; font-size: 12px; margin-top: 4px; }}
.header-right {{ text-align: right; color: #64748b; font-size: 12px; }}
.header-right .date {{ font-size: 16px; color: #94a3b8; font-weight: 600; }}

/* ── Stat Cards ── */
.stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }}
.stat-card {{
  background: #111827; border: 1px solid #1e293b;
  border-radius: 10px; padding: 18px; position: relative;
  overflow: hidden;
}}
.stat-card::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
}}
.stat-card.s-total::before {{ background: #4fc3f7; }}
.stat-card.s-critica::before {{ background: #e63946; }}
.stat-card.s-overdue::before {{ background: #f97316; }}
.stat-card.s-done::before {{ background: #22c55e; }}
.stat-number {{ font-size: 36px; font-weight: 800; line-height: 1; }}
.stat-card.s-total .stat-number {{ color: #4fc3f7; }}
.stat-card.s-critica .stat-number {{ color: #e63946; }}
.stat-card.s-overdue .stat-number {{ color: #f97316; }}
.stat-card.s-done .stat-number {{ color: #22c55e; }}
.stat-label {{ font-size: 11px; color: #64748b; margin-top: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}

/* ── Section headers ── */
.section {{ margin-bottom: 28px; }}
.section-header {{
  font-size: 13px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1px; color: #64748b; margin-bottom: 12px;
  display: flex; align-items: center; gap: 8px;
}}
.section-header::after {{
  content: ''; flex: 1; height: 1px; background: #1e293b;
}}

/* ── Main Table ── */
.table-wrapper {{ overflow-x: auto; border-radius: 10px; border: 1px solid #1e293b; }}
table {{
  width: 100%; border-collapse: collapse;
  background: #0f172a;
}}
thead tr {{ background: #111827; }}
th {{
  padding: 12px 14px; text-align: left;
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.8px; color: #475569;
  border-bottom: 1px solid #1e293b;
}}
tbody tr {{
  border-bottom: 1px solid #1a2332;
  transition: background 0.15s;
}}
tbody tr:hover {{ background: #162032; }}
tbody tr:last-child {{ border-bottom: none; }}
td {{ padding: 12px 14px; vertical-align: top; }}

/* Priority row accents */
tr.priority-critica td:first-child {{ border-left: 3px solid #e63946; }}
tr.priority-alta td:first-child {{ border-left: 3px solid #f97316; }}
tr.priority-media td:first-child {{ border-left: 3px solid #fbbf24; }}
tr.priority-baixa td:first-child {{ border-left: 3px solid #22c55e; }}

.titulo {{ font-weight: 600; color: #e2e8f0; font-size: 13px; }}
.notas-small {{ color: #64748b; font-size: 11px; margin-top: 3px; line-height: 1.4; }}

/* ── Badges ── */
.badge {{
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
}}
.badge.priority-critica {{ background: #3d1a1d; color: #e63946; }}
.badge.priority-alta {{ background: #2d1a0e; color: #f97316; }}
.badge.priority-media {{ background: #2d2210; color: #fbbf24; }}
.badge.priority-baixa {{ background: #0f2d1a; color: #22c55e; }}

.status-badge {{
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 600;
}}
.status-aberto {{ background: #3d1a1d; color: #e63946; }}
.status-aguardando {{ background: #2d2210; color: #fbbf24; }}
.status-concluido {{ background: #0f2d1a; color: #22c55e; }}
.status-cancelado {{ background: #1a1a1a; color: #64748b; }}

/* ── Deadline colors ── */
.deadline-overdue {{ color: #e63946; font-weight: 700; }}
.deadline-critical {{ color: #ff6b6b; font-weight: 600; }}
.deadline-warn {{ color: #fbbf24; }}

.nr-critical {{ color: #e63946; font-weight: 700; }}
.nr-warn {{ color: #fbbf24; }}
.nr-ok {{ color: #64748b; }}

/* ── Alert badges ── */
.alert-critico {{
  display: inline-block; margin-top: 4px; padding: 2px 7px;
  background: #3d1a1d; color: #e63946; border-radius: 4px;
  font-size: 10px; font-weight: 700;
}}
.alert-alto {{
  display: inline-block; margin-top: 4px; padding: 2px 7px;
  background: #2d1a0e; color: #f97316; border-radius: 4px;
  font-size: 10px; font-weight: 700;
}}

/* ── Utilities ── */
.muted {{ color: #64748b; }}
.small {{ font-size: 11px; }}

/* ── Two-column layout ── */
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }}

/* ── Timeline ── */
.timeline {{
  background: #0f172a; border: 1px solid #1e293b;
  border-radius: 10px; padding: 16px; max-height: 320px; overflow-y: auto;
}}
.timeline-item {{
  display: flex; gap: 12px; align-items: flex-start;
  padding: 8px 0; border-bottom: 1px solid #1a2332;
}}
.timeline-item:last-child {{ border-bottom: none; }}
.timeline-date {{
  min-width: 80px; padding-left: 8px; text-align: left;
}}
.tl-date {{ font-size: 11px; color: #94a3b8; font-weight: 600; }}
.tl-days {{ font-size: 16px; font-weight: 800; }}
.tl-title {{ font-size: 13px; color: #e2e8f0; padding-top: 2px; }}

/* ── Company cards ── */
.companies-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
.company-card {{
  background: #0f172a; border: 1px solid #1e293b;
  border-radius: 8px; padding: 12px 14px;
}}
.company-name {{ font-weight: 700; font-size: 13px; margin-bottom: 8px; }}
.company-items {{ list-style: none; padding: 0; }}
.company-items li {{ font-size: 12px; color: #94a3b8; padding: 2px 0; }}

.mini-badge {{
  display: inline-block; padding: 1px 6px; border-radius: 3px;
  font-size: 10px; font-weight: 700; margin-left: 4px;
}}
.mini-badge.crit {{ background: #3d1a1d; color: #e63946; }}
.mini-badge.alta {{ background: #2d1a0e; color: #f97316; }}

/* ── Footer ── */
.footer {{
  margin-top: 40px; padding-top: 16px; border-top: 1px solid #1e293b;
  color: #334155; font-size: 11px; text-align: center;
}}
</style>
</head>
<body>
<div class="container">

  <!-- HEADER -->
  <div class="header">
    <div class="header-left">
      <h1>🎯 CM Brasil — Follow-up Tracker</h1>
      <div class="subtitle">Pendências · Deadlines · Follow-ups · Alertas</div>
    </div>
    <div class="header-right">
      <div class="date">{today_br}</div>
      <div>Atualizado em {datetime.now().strftime('%H:%M')}</div>
    </div>
  </div>

  <!-- STATS -->
  <div class="stats">
    <div class="stat-card s-total">
      <div class="stat-number">{len(active)}</div>
      <div class="stat-label">⬤ Pendências Abertas</div>
    </div>
    <div class="stat-card s-critica">
      <div class="stat-number">{len(criticos)}</div>
      <div class="stat-label">🔴 Críticas</div>
    </div>
    <div class="stat-card s-overdue">
      <div class="stat-number">{len(overdue)}</div>
      <div class="stat-label">⏰ Atrasadas</div>
    </div>
    <div class="stat-card s-done">
      <div class="stat-number">{len(done)}</div>
      <div class="stat-label">✅ Concluídas</div>
    </div>
  </div>

  <!-- TIMELINE + COMPANIES -->
  <div class="two-col">
    <div class="section">
      <div class="section-header">📅 Deadlines — próximos 14 dias</div>
      <div class="timeline">
        {timeline_html}
      </div>
    </div>
    <div class="section">
      <div class="section-header">🏢 Por Empresa</div>
      <div class="companies-grid">
        {company_html}
      </div>
    </div>
  </div>

  <!-- MAIN TABLE -->
  <div class="section">
    <div class="section-header">📋 Todas as Pendências (ordenadas por urgência)</div>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Pendência</th>
            <th>Prioridade</th>
            <th>Empresa / Contato</th>
            <th>Deadline</th>
            <th>Sem Resp.</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    Follow-up Tracker · Cooler Master Brasil · Jubinha 🐧 · Gerado em {today_br}
    &nbsp;·&nbsp; <code>python tracker.py --dashboard</code> para atualizar
  </div>

</div>
</body>
</html>"""

    return html


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Cooler Master Brasil — Follow-up Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
          Exemplos:
            python tracker.py --status
            python tracker.py --alertas
            python tracker.py --add
            python tracker.py --add --json '{"titulo":"Teste","prioridade":"alta"}'
            python tracker.py --update 215d63f1 --status aguardando
            python tracker.py --update 215d63f1 --contato --notas "Email enviado"
            python tracker.py --complete 215d63f1
            python tracker.py --relatorio
            python tracker.py --relatorio --output relatorio.md
            python tracker.py --dashboard
        """)
    )

    # Actions (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--status",    action="store_true", help="Pendências abertas por urgência")
    action_group.add_argument("--alertas",   action="store_true", help="Alertas do dia")
    action_group.add_argument("--add",       action="store_true", help="Adicionar nova pendência")
    action_group.add_argument("--update",    metavar="ID",        help="Atualizar pendência (ID ou prefixo)")
    action_group.add_argument("--complete",  metavar="ID",        help="Marcar como concluído")
    action_group.add_argument("--relatorio", action="store_true", help="Relatório markdown completo")
    action_group.add_argument("--dashboard", action="store_true", help="Gerar dashboard HTML")

    # Optional modifiers
    parser.add_argument("--json",       dest="json_data", metavar="JSON",  help="JSON para --add")
    parser.add_argument("--status-val", dest="status",   metavar="STATUS", help="Novo status (para --update)")
    parser.add_argument("--notas",                       metavar="TEXTO",  help="Novas notas (para --update)")
    parser.add_argument("--contato",    action="store_true",                help="Atualizar último contato para hoje (para --update)")
    parser.add_argument("--prioridade",                  metavar="P",      help="Nova prioridade (para --update)")
    parser.add_argument("--deadline",                    metavar="DATE",   help="Novo deadline YYYY-MM-DD (para --update)")
    parser.add_argument("--output", "-o",                metavar="FILE",   help="Arquivo de saída (--relatorio / --dashboard)")

    args = parser.parse_args()

    if args.status:
        cmd_status(args)
    elif args.alertas:
        cmd_alertas(args)
    elif args.add:
        cmd_add(args)
    elif args.update:
        args.id = args.update
        cmd_update(args)
    elif args.complete:
        args.id = args.complete
        cmd_complete(args)
    elif args.relatorio:
        cmd_relatorio(args)
    elif args.dashboard:
        cmd_dashboard(args)


if __name__ == "__main__":
    main()
