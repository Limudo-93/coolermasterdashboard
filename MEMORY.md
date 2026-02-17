# MEMORY.md — Memória de Longo Prazo da Jubinha 🐧

_Atualizado: 2026-02-17_

---

## Sobre o Limudo (USER)
- **Nome:** Vinicius Lima Dalbem ("Limudo")
- **Cargo:** Country Manager, Cooler Master Brasil
- **Perfil:** Executivo/analítico, NÃO é dev. Usa Excel, Power BI, Supabase/Next.js/Vercel
- **Timezone:** America/Sao_Paulo
- **Projetos pessoais:** Chama o Músico (P2P músicos), Lima Cargo (logística)
- **Hobbies:** Música (guitarra/vocal), fitness
- **Comunicação:** Português BR, tom divertido/humorístico
- **Canal principal:** Telegram (evita WhatsApp por status "online")

## Infraestrutura
- **Mac mini** (ARM, RAM limitada — cuidado com processos pesados)
- **IPv6 bugado** — gateway precisa de NODE_OPTIONS="--dns-result-order=ipv4first"
- **OneDrive corporativo** — NUNCA escrever direto durante sync; salvar local primeiro, depois copiar
- **REGRA:** SEMPRE copiar entregas finais (HTMLs, Excel, CSV) pro OneDrive (~/Library/CloudStorage/OneDrive-CoolerMaster/2026/Jubinha/) — arquivos .md internos ficam só no workspace
- **Outlook/Exchange 365** — TI bloqueia login fora do Outlook; considerar Microsoft Graph API
- **Apple Calendar** — eventos do Outlook aparecem no iPhone mas NÃO no Mac mini (sync iCloud pendente)

## Agentes
| Agente | Modelo | Workspace | Função |
|--------|--------|-----------|--------|
| Main (Jubinha) | Opus 4.6 | workspace-main | Coordenação geral |
| Pesquisador 🔍 | Haiku 4.5 | workspace-pesquisa | Scripts, scraping, coleta |
| Analista 📊 | Sonnet 4.5 | workspace-dados | Análise, relatórios |
| Criativo 💡 | Sonnet 4.5 | workspace-brainstorm | Ideias, conteúdo |

## KaBuM Scraper
- **API pública** (sem auth): `servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/`
- Categorias: `hardware/fontes`, `perifericos/gabinetes`, `hardware/coolers`
- Detail: `/catalog/v2/products/{id}` — preço, stock, warranty, specs HTML, product_link
- Script: `~/.openclaw/workspace-pesquisa/kabum-scraper/scraper.py` (v4, requests puro)
- Enricher: `enrich.py` — extrai specs do HTML description
- Cron diário 5:00 AM (job `8a874296`)
- 403 produtos, 9 Cooler Master (Feb 16)
- **Gabinetes = `perifericos/gabinetes`** (não hardware/)

## Supabase
- Project: `etexdfjpjvfpptselwdi`
- Tabelas: `produtos`, `precos`, `alertas` + views `v_produtos_ultimo_preco`, `v_variacao_preco`
- REST upsert funciona; import Python causa SIGKILL (usar HTTP leve)

## Contatos CM Importantes
- **Ariel Mai** — LATAM Manager, chefe direto do Limudo. Argentino, Taipei.
- **Claire Chen** — Assistente HQ / Supply Chain. Não gerencia ninguém, mas CRÍTICA na operação. Deadline: Expense MF até 20/02
- **Michael Teng** — MKT, MALA MKT Weekly Catchup (terças 5:30 AM)
- **Vitor Ibanez, Raphael Peterson** — Time Brasil
- **Icaro Marques** — PR/Marketing

## Clientes/Distribuidores
- **KaBuM:** Mariana de Castro (buyer), Thales Vicentini (Gerente HW)
- **VAIP:** William Santos — buffer order/aging
- **Mazer, All Nations, Oderço, Pichau** — distribuidores

## Números Business
- Q1 Brasil: USD $3,132,691.77 confirmado, 91% hit rate, target AC $1,285,541.77
- Budget MKT 2026 congelado pelo presidente da CM
- Sem rebate agreements assinados para Brasil

## TTS/STT
- STT: OpenAI gpt-4o-mini-transcribe (funciona)
- TTS: ElevenLabs, voz custom "Jubinha_2" (ID: `lX67m4YOLsvdtfFFvPHx`)
- Auto-TTS do OpenClaw não funciona — usar API ElevenLabs direta

## Lições Aprendidas
- Playwright/Chromium = SIGKILL no Mac mini (RAM insuficiente)
- Supabase import Python = SIGKILL — usar HTTP REST
- Scraper: escrever incrementalmente (append mode) em vez de acumular em memória
- OneDrive file locking é real — salvar local primeiro
- KaBuM tem API pública completa — não precisa de browser scraping

## Cron Jobs Ativos
| Job | Schedule | ID (prefix) |
|-----|----------|-------------|
| Resumo Matinal | seg-sex 8:30 | c1bb9880 |
| Revisão Semanal | seg 9:00 | fc4c3212 |
| KaBuM Scraper | diário 5:00 | 8a874296 |

## Setup Inspirado em
- Vídeo YouTube do Bruno Camoto sobre OpenClaw
