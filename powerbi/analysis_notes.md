# Power BI — RP-CMT CH Operational Analysis
## Data as of: 2026-02-16 | Account: LATAM_Sales_1

---

## Dashboard Structure (10 pages)
1. Home — Overview
2. Trend — Sales & inventory by month/quarter/half-year (ERRO: visuals não carregam)
3. Summary — KPIs de sales targets por canal e product line
4. CFT Info — YoY customer comparison + rankings
5. Product Info — YoY por product line
6. New Product — Share de produtos novos
7. Inventory Info — Rankings inventário + aging
8. Sales Detail — Dados detalhados vendas (exportável)
9. Order Detail — Dados detalhados pedidos
10. Inventory Detail — Dados detalhados inventário

## Key Metrics (Summary page — view: Quarter)
- **AF (Annual Forecast):** $1.54M USD
- **Full Year LY (2025):** $3.66M USD (corrigido pelo Limudo)
- **AC (Actual 2026):** ainda sem vendas registradas no sistema
- **BO (Backlog Orders):** $624
- **Growth Rate:** -100% (sem AC registrado ainda)
- **GP%:** 15.82%
- **Target GP:** $337K

**NOTA:** "Mil" no Power BI = milhares (K). Os $946K visíveis eram apenas 1 quarter de LY, não o ano todo.

### By Channel (CH)
| CH | CFT | AF | AC | Achv% | AC-LY | Growth% | BO w/ DN | BO | BO w/n ship | All BO | ASP | GP Target | GP | Achv%(GP) | GP% | GP%-LY | Growth%_GP |
|----|-----|----|----|-------|-------|---------|----------|----|-------------|--------|-----|-----------|----|-----------|----|--------|------------|
| LATAM | Total | 1,540 Mil | | | 946 Mil | -100% | 0 Mil | 1 Mil | | | | 337 Mil | | | 15.82% | | -100% |
| | BR | 1,540 Mil | | | 946 Mil | -100% | 0 Mil | 1 Mil | | | | 337 Mil | | | 15.82% | | -100% |

### By BU/ProductLine  
| BUL1 | AF | AC | Achv%(AC) | AC Contri.% | AC-LM | AC-LY | Growth% | Qty | BO w/ DN | BO | BO w/n ship | GP(M) | GP(M)% | GP(M)%-LY | Growth(%) GP |
|------|----|----|-----------|-------------|-------|-------|---------|-----|----------|----|-------------|-------|--------|-----------|-------------|
| Total | | | | | | 946 Mil | -100% | | 0 Mil | 1 Mil | | | | 337 Mil | |
| RP-Power | | 593 Mil | | | | 326 Mil | -100% | | | | | | -6.05% | 100 Mil | |
| RP-Case | | 528 Mil | | | | 236 Mil | -100% | | | | | | 28.37% | 113 Mil | |
| RP-Thermal | | 373 Mil | | | | 285 Mil | -100% | 0 Mil | 1 Mil | | 1 Mil | 116 Mil | | 32.82% | |
| BU Others | | 46 Mil | | | | 99 Mil | -100% | | | | | 7 Mil | | 8.56% | |
| Others | | | | | | 1 Mil | -100% | | | | | | 100% | | |

## CFT Info — Customer Rankings (Quarter view, 2026 Month 6)
| Customer | AC | AC Contri.% | AC-LM | AC-LY | Growth(%) | Qty | BO w/ DN | BO | BO w/n ship | GP(M) | GP(M)% | GP(M)%-LY | Growth(%) GP | ASP | ASP-LY |
|----------|----|----|-------|-------|---------|-----|--------|----|----|-------|-------|-------|------|-----|-------|
| Total | | | | 946 Mil | -100% | | 0 Mil | 1 Mil | | | | | | | |
| GM | | | | 105 Mil | -100% | | | | | | 18.82% | | -100% | 29.02 |
| KABUM | | | | 39 Mil | -100% | | | | | | 14.80% | | -100% | 12.10 |
| MAZER | | | | 663 Mil | -100% | 0 Mil | 1 Mil | | | | 10.36% | | -100% | 44.80 |
| ODERCO | | | | 149 Mil | -100% | | | | | | 43.57% | | -100% | 6.14 |
| PREXX | | | | -10 Mil | 100% | | | | | | 100% | | -100% | -Infinito |

## Sales Detail — FULL DATA (Month=1, All ProductLines, All Metrics)
### RP-Case products (January 2026 — 39 SKUs)
See: powerbi/sales_detail_month1_rpcase.csv

**Top sellers by AC (USD):**
1. Vertical Graphics Card Holder Kit V3 — $16,800 (420 qty, 44.88% GP)
2. MasterBox MB320L — $7,750 (250 qty, 26.23% GP)
3. Vertical GPU Holder Kit V3 White — $6,888 (168 qty, 43.24% GP)
4. MasterBox TD500 Mesh w/ARGB hub — $5,800 (100 qty, 29.69% GP)
5. Qube 500 Flatpack — $5,568 (96 qty, 29.79% GP)
6. HAF 700 — $5,292 (28 qty, 29.22% GP)
7. Qube 500 Flatpack Macaron — $3,174 (46 qty, 28.77% GP)
8. HAF 700 EVO — $2,990 (10 qty, 27.74% GP)

**Best GP% products:**
1. Riser Cable PCIe White 200mm — 50.54%
2. Riser Cable PCIe 300mm — 48.59%
3. Riser Cable PCIe 200mm — 48.57%
4. Riser Cable PCIe White 300mm — 47.45%
5. Vertical GPU Holder Kit V3 — 44.88%
6. Vertical GPU Holder Kit V3 White — 43.24%

**Grand Total (ALL products, ALL months):**
- AC: $7,269,622 USD
- AC (Local): R$ 227,875,379
- Qty: 369,639 units
- COGS: 6,213,751
- GP: $1,055,871
- GP%: 14.52%
- ASC: 17

## Important Notes
- Currency: USD (Trend & Detail pages include local currency BRL)
- Data updated daily at 2:00 AM UTC+8
- Achievement rate colors: Red <80%, Yellow 80-95%, Green >95%
- New product definition: launched within last 2 years, aligns with product differentiation
- Local currency for LATAM: TWD (data provided by SAP) — this is interesting, uses TWD not BRL
- Max export: 30,000 rows to CSV, 150,000 rows to XLSX
- Trend page has errors loading visuals (may be permission issue with LATAM_Sales_1 account)
- Brazil customers: GM, KaBuM, Mazer, Oderço, Prexx
- Mazer is the biggest customer by AC-LY ($663M) — 70% of total!
- Oderço has the best GP% (43.57%)
- KaBuM is relatively small ($39M AC-LY)

## Observations
1. Growth rate shows -100% across the board — NO sales booked yet for 2026 in the system
2. Full Year LY (2025): $3.66M USD total Brasil (confirmed by Limudo)
3. AF (Annual Forecast): $1.54M — ~42% of LY ($3.66M), may be conservative or partial
4. BO (Backlog Orders) = $624 → very small pipeline
5. GP% target is 15.82% — consistent across product lines
6. Mazer dominates (70% of LY revenue) but has lowest GP% (10.36%)
7. Oderço is small but very profitable (43.57% GP%)
8. Riser cables and GPU holder kits have the best margins (45-50% GP)
