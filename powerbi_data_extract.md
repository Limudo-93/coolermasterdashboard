# Power BI Data Extract — RP-CMT CH Operational
**Extraído em:** 2026-02-17  
**Report:** RP-CMT CH Operational — Summary  
**As of Date:** 2026-02-16  
**Currency:** USD  
**ACCT_CD:** 51110000 (Sell-In)  
**Region:** BR (Brazil only)

---

## Como o Filtro de Mês Funciona

O filtro "Month" é **cumulativo (YTD)**:
- Month=1 → somente Janeiro
- Month=2 → Janeiro + Fevereiro (acumulado)
- Month=3 → Janeiro + Fevereiro + Março (Q1 acumulado)
- etc.

---

## KPIs Globais — Q1 2026 YTD (Month=3, YTD até 16/02)

| Métrica | Valor |
|---|---|
| **AF (Annual Forecast Q1)** | $1,421K |
| **AC (Actual Shipped)** | $124.74K |
| **Achv% (AC/AF)** | **8.78%** |
| **AC+BO w DN** | $124.74K |
| **AC+BO w DN + BO** | $197.76K |
| **Total Achv% (w/ BO)** | **13.91%** |
| **Growth vs LY** | **-46.64%** |
| **LY (Q1 2025 actual)** | $234K |
| **BO (Backorder)** | $73.02K |
| **ASP** | $26.34 |
| **Units Sold** | 4,740 |
| **GP Target** | $318.85K |
| **GP Actual** | $22.55K |
| **GP Achv% (GP/Target)** | **7.07%** |
| **GP%** | **18.08%** |
| **GP% LY** | 9.96% |
| **GP% Growth** | +81.50% |
| **Inv Amt** | $45.76K |
| **New Product Contri%** | 92.51% |
| **Growth Rate (Headline)** | -46.64% |

---

## Por BU — Q1 2026 (Month=3 YTD, Brazil)

| BU | AF | AC | Achv% | AC-LY | Growth | BO | ASP | GP Target | GP | GP Achv% | GP% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **RP-Power** | $550K | $4K | 0.79% | -$7K | +164.83% | $0 | $98.85 | $94K | $1K | 0.78% | 16.85% |
| **RP-Case** | $492K | $61K | 12.37% | $43K | +42.07% | $32K | $42.33 | $106K | $9K | 8.60% | 14.95% |
| **RP-Thermal** | $335K | $60K | 17.77% | $167K | -64.42% | $41K | $18.30 | $112K | $13K | 11.38% | 21.37% |
| **BU Others** | $44K | $0 | 0% | $40K | -100% | $0 | — | $7K | $0 | 0% | — |
| **BU Others(CH)** | $0 | $0 | — | — | — | $0 | — | $0 | $0 | — | — |
| **Others** | $0 | $0 | — | -$10K | 100% | $0 | — | $0 | $0 | — | — |
| **TOTAL BR** | **$1,421K** | **$125K** | **8.78%** | **$234K** | **-46.64%** | **$73K** | **$26.34** | **$319K** | **$23K** | **7.07%** | **18.08%** |

---

## AF Mensal Breakdown (Derivado dos Filtros Cumulativos)

| Mês | AF Mensal | AF Acumulado |
|---|---|---|
| Janeiro | $461K | $461K |
| Fevereiro | $474K | $935K |
| Março | $486K | $1,421K |
| **Q1 Total** | **$1,421K** | — |

### AF por BU — Breakdown Mensal
| BU | Jan AF | Fev AF (cum) | Q1 AF (cum) |
|---|---|---|---|
| RP-Power | $173K | $358K | $550K |
| RP-Case | $163K | $327K | $492K |
| RP-Thermal | $111K | $221K | $335K |
| BU Others | $15K | $29K | $44K |
| **Total** | **$461K** | **$935K** | **$1,421K** |

---

## Dados Mensais por Período

### Mês 1 — Janeiro 2026 (somente Jan)
- AF: $461K | AC: $0 | Achv%: 0.00%
- LY: -$10K | Growth: +100.00%
- GP Target: $104K | GP: $0 | GP%: NaN
- Units Sold: 0 | ASP: NaN

### Mês 2 — YTD Fev 2026 (Jan+Feb acumulado)
- AF: $934.77K | AC: $124.74K | Achv%: 13.34%
- LY: $262K | Growth: -52.37%
- GP Target: $210.19K | GP: $22.55K | GP%: 18.08% (LY: 19.63%, gth: -7.91%)
- Units Sold: 4,740 | ASP: $26.34

By BU (Month=2 YTD):
| BU | AF | AC | Achv% | LY | Growth |
|---|---|---|---|---|---|
| RP-Power | $358K | $4K | 1.22% | $11K | -61.75% |
| RP-Case | $327K | $61K | 18.63% | $43K | +42.07% |
| RP-Thermal | $221K | $60K | 26.90% | $171K | -65.26% |
| BU Others | $29K | $0 | 0% | $46K | -100% |
| **Total** | **$935K** | **$125K** | **13.34%** | **$262K** | **-52.37%** |

### Mês 3 — YTD Q1 2026 (Jan+Feb+Mar acumulado)
- AF: $1,421K | AC: $124.74K | Achv%: 8.78%
- LY: $234K | Growth: -46.64%
- BO: $73K | AC+BO: $197.76K | Total Achv%: 13.91%
- GP Target: $318.85K | GP: $22.55K | Achv%(GP): 7.07% | GP%: 18.08%
- Units Sold: 4,740 | ASP: $26.34 | Inv Amt: $45.76K

---

## Q2-Q4 2026
**Sem dados de AC ainda** (só AF/plano disponível)  
Para mostrar no MasterDeck: **"Forecast"** ou **"TBD"** conforme instrução.

---

## Notas Importantes
1. **Power BI é a fonte de verdade** para todos os dados de sell-in
2. O filtro "Month" neste report é **cumulativo (YTD)**, não mês individual
3. Brazil (BR) = única entrada em LATAM: toda data do report é Brasil
4. "AC" = Actual Shipped/Invoiced (não inclui backorders)
5. "BO" = Backorder (pedido não entregue ainda)
6. "AF" = Annual Forecast / Plano anual
7. "LY" = Last Year comparativo
8. **AC para Fevereiro inclui dados até 16/02/2026 apenas**
9. RP-Power: AC muito baixo ($4K) vs AF ($550K) — PowerBUs (PSU/Cases) tendem a ship em bulk no final do quarter
10. RP-Case: melhor performer em valor absoluto ($61K)
11. RP-Thermal: melhor performer em % achv (17.77%) mas forte queda vs LY (-64.42%)
