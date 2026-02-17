# Jarvis Legacy Review
> Antigo assistente AI — Revisão do conteúdo em 2026/Jarvis/
> Gerado: 2026-02-17

## Estrutura

```
Jarvis/
├── README.md (291B) — não consegui ler (OneDrive lock)
├── Analises/
│   ├── meeting_minutes_teams_2026-02-11_1756.md (937B) — ata de reunião Teams
│   ├── sellout_2026_fob_insights.json (5.7KB) — insights de sellout FOB
│   ├── sellout_fob_insights_w06_2026.json (8.7KB) — insights W06 mais detalhados
│   └── teams_call_2026-02-11_1756.txt (607B) — transcrição/notas de call
├── Apresentacoes/
│   └── CM_BR_SellOut_2026_FOB_Diretoria.pptx (6.6MB) — apresentação para diretoria
├── Dados/
│   ├── teams_call_2026-02-11_1756.mov (171MB!) — gravação de call Teams
│   ├── *.log, *.pid — arquivos de controle de gravação
│   └── test_record_10s.log — teste de gravação
└── Templates/
    └── CM_2024VI_PPT Template_V2.02.pptx (6.8MB) — template PowerPoint CM
```

## O que o Jarvis fazia (inferido)

1. **Gravação de calls Teams** — capturava tela com screen recording (.mov), gerava logs
2. **Análise de Sellout** — processava dados FOB e gerava insights em JSON
3. **Geração de apresentações** — usava template CM para criar PPTX de sellout para diretoria
4. **Atas de reunião** — transcrição e minutes de calls

## O que vale migrar para Jubinha

| Item | Valor | Ação |
|------|-------|------|
| Template PPTX | ✅ Alto | Já está em `Jarvis/Templates/` e duplicado na raiz. Jubinha pode usar para gerar apresentações |
| Insights JSON | ✅ Médio | Formato de dados útil como referência para análises futuras |
| Apresentação Diretoria | ✅ Alto | Referência de formato/conteúdo para futuras apresentações |
| Gravação .mov 171MB | ⚠️ Baixo | Ocupa muito espaço. Mover para backup ou deletar |
| Logs/PIDs | ❌ Nenhum | Artefatos técnicos, podem ser deletados |
| Meeting minutes | ✅ Médio | Referência de formato para Jubinha gerar atas |

## Recomendações

1. **Migrar templates e apresentações** para `Jubinha/templates/` 
2. **Mover .mov para backup externo** (171MB no OneDrive é desperdício)
3. **Deletar logs/pids** — sem valor
4. **Manter Jarvis/ como arquivo** por enquanto, até confirmar que tudo foi migrado

## ⚠️ Nota: OneDrive Lock
Vários arquivos em Jarvis/ retornaram "Resource deadlock avoided" ao tentar ler. O conteúdo do README.md e dos arquivos de análise não pôde ser lido diretamente. O OneDrive pode estar sincronizando ou os arquivos são "on-demand" e não estão baixados localmente.
