# OneDrive 2026 - Mapa Completo da Estrutura
> Gerado em: 2026-02-17 01:16 BRT

## Estrutura de Pastas

```
2026/
├── 6MSF/
│   └── 6MSF_January.xlsx (200KB, Jan 20)
├── Analista/ (vazio)
├── Appraisal/
│   ├── 2025 Performance Appraisal - Vinicius.xlsx (657KB, Jan 28)
│   ├── 2025 Performance Appraisal - Vinicius_FINAL.xlsx (658KB, Jan 29)
│   └── 2025 Performance Appraisal - Vinicius_FINAL_signed.xlsx (754KB, Jan 30)
├── Channel_MKT/
│   ├── MALA Channel MKT _2026AF.xlsx (509KB, Dec 31)
│   └── MF費用-CH_Latam BR-2026 Jan.xlsx (222KB, Jan 21)
├── Criativo/ (vazio)
├── Customers/
│   └── Kabum/
│       ├── ND Cooler Master 18452-01-30 - Clicksign.pdf (185KB)
│       ├── ND Cooler Master 18452-01-30 _signed.pdf (591KB)
│       └── Suggested Orders/
│           ├── Kabum_Chassis_Order.xlsx (11KB)
│           ├── Kabum_Chassis_Q1_Final.xlsx (58KB)
│           ├── Kabum_PSU_Q1_Final.xlsb (4.5MB)
│           ├── Kabum_Thermal_Suggested.xlsb (4.5MB)
│           └── PSU_Q1_Suggested_Order.xlsb (4.5MB)
├── Jarvis/ (antigo assistente - ver jarvis_legacy_review.md)
│   ├── README.md (291B)
│   ├── Analises/
│   │   ├── meeting_minutes_teams_2026-02-11_1756.md (937B)
│   │   ├── sellout_2026_fob_insights.json (5.7KB)
│   │   ├── sellout_fob_insights_w06_2026.json (8.7KB)
│   │   └── teams_call_2026-02-11_1756.txt (607B)
│   ├── Apresentacoes/
│   │   └── CM_BR_SellOut_2026_FOB_Diretoria.pptx (6.6MB)
│   ├── Dados/
│   │   ├── teams_call_2026-02-11_1756.mov (171MB!) ⚠️
│   │   ├── teams_call_2026-02-11_1729.log (1.6KB)
│   │   ├── teams_call_2026-02-11_1756.log (0B)
│   │   ├── teams_call_2026-02-11_1729.pid (6B)
│   │   ├── teams_call_2026-02-11_1756.pid (6B)
│   │   └── test_record_10s.log (1.1KB)
│   └── Templates/
│       └── CM_2024VI_PPT Template_V2.02.pptx (6.8MB) ← DUPLICADO
├── Jubinha/
│   ├── Jubinha-Setup-Day.html (⚠️ 0B - lock impediu cópia)
│   ├── Organograma_CM.html (24KB) ✅
│   ├── Output 1-2.mp3 (18.6MB) ✅
│   └── kabum-scraper/
│       ├── ultimo_resumo.json (3.7KB)
│       ├── alertas/
│       │   └── alertas_2026-02-16.txt (58B)
│       └── historico/
│           ├── kabum_2026-02-16.csv (308KB) ✅ atualizado
│           ├── kabum_2026-02-16.xlsx (266KB)
│           ├── kabum_2026-02-16_enriched.csv (169KB)
│           ├── kabum_2026-02-16_enriched.xlsx (155KB)
│           ├── kabum_2026-02-16_full.csv (991KB)
│           ├── kabum_2026-02-16_full.xlsx (464KB)
│           ├── kabum_2026-02-16_full_clean.csv (386KB)
│           ├── KaBuM_Dashboard_2026-02-16.xlsx (110KB)
│           └── KaBuM_Relatorio_2026-02-16.xlsx (296KB)
├── KPI/
│   ├── KPI Template_VITOR_BRAZIL_2026.xlsx (24KB)
│   └── KPI_VINICIUS_BRAZIL_2026.xlsx (24KB)
├── Pesquisador/ (vazio)
├── PriceList/
│   ├── PriceList LATAM - 20260114.xlsb (4.5MB)
│   └── Buffer_Order_Q1.xlsx (89KB)
├── Reimbursements/
│   └── Jan/ (muitos recibos de viagem CES Las Vegas)
├── Reports/
│   ├── MALA_Meeting/
│   │   └── WK_06_CMT MALA Bi Weekly.xlsx (143KB)
│   ├── Sellout Report/ (11 arquivos de distribuidores: Kabum, GMI, All Nations, etc.)
│   └── Shipping Schedule/
│       ├── S.AMER Order list -0207-BR&MX.xlsx (7.8MB)
│       ├── S.AMER Order list Nola&Sola-0207.xlsx (10.4MB)
│       └── Finished-2026.xlsx (71KB)
├── Sellout/
│   └── Brazil_Sell_Out_W06_FY2026.xlsx (24.3MB)
```

## ⚠️ Arquivos Soltos na Raiz (precisam reorganização)

| Arquivo | Tamanho | Sugestão |
|---------|---------|----------|
| `CM_2024VI_PPT Template_V2.02.pptx` | 6.8MB | → Mover para `Jarvis/Templates/` (já existe lá - DUPLICADO, deletar da raiz) |
| `Finished-2026.xlsx` | 77KB | → Duplicado? Existe em `Reports/Shipping Schedule/` (71KB). Raiz tem versão mais nova (Feb 13 vs Feb 11). Mover para `Reports/Shipping Schedule/` |
| `LA_Inventory.xlsx` | 41KB | → `Reports/` ou criar `Inventory/` |
| `LA_Inventory_TGT.xlsx` | 41KB | → Junto com LA_Inventory |
| `S.AMER Order list -0207-BR&MX.xlsx` | 7.8MB | → `Reports/Shipping Schedule/` (DUPLICADO - já existe lá, mesma versão) |
| `S.AMER Order list Nola&Sola-0213.zip` | 4.3MB | → `Reports/Shipping Schedule/` |
| `W04_MalaWeeklyReport.xlsx` | 387KB | → `Reports/MALA_Meeting/` |
| `RE- LATAM Shipping list update-13-FEB.eml` | 16.8MB | → `Reports/Shipping Schedule/` ou deletar (é email salvo) |

## 🔄 Duplicados Identificados

1. **CM_2024VI_PPT Template_V2.02.pptx** — Raiz (6.8MB) = `Jarvis/Templates/` (6.8MB) → Exatamente iguais
2. **S.AMER Order list -0207-BR&MX.xlsx** — Raiz (7.8MB, Feb 13) ≈ `Reports/Shipping Schedule/` (7.8MB, Feb 11) → Raiz pode ser mais recente
3. **Finished-2026.xlsx** — Raiz (77KB, Feb 13) vs `Reports/Shipping Schedule/` (71KB, Feb 11) → Versões diferentes, raiz mais nova

## 📁 Pastas Vazias
- `Analista/` - novo papel do Jubinha?
- `Criativo/` - novo papel do Jubinha?  
- `Pesquisador/` - novo papel do Jubinha?

## 📊 Estatísticas
- **Total de arquivos:** ~80+
- **Maior arquivo:** `Jarvis/Dados/teams_call_2026-02-11_1756.mov` (171MB) — considerar mover para backup externo
- **Espaço total estimado:** ~300MB+
