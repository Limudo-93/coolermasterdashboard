# NCM Cooler Master — Tabela Completa de Alíquotas

> **Atualização:** Fevereiro 2026  
> **Base legal:** TEC vigente (Resolução GECEX nº 812/2025), TIPI (Decreto 11.158/2022 e atualizações), Lei 10.865/2004 (PIS/COFINS importação)  
> **Verificação:** Consultar Portal Único Siscomex Classif (portalunico.siscomex.gov.br/classif) para alíquotas atualizadas por NCM

---

## Como Calcular o Imposto Total na Importação

A base de cálculo dos tributos na importação é **em cascata**:

```
Base II  = Valor Aduaneiro (CIF em R$)
Base IPI = (Valor Aduaneiro + II)
Base PIS/COFINS = Valor Aduaneiro + II + IPI + CIDE + ISS (se aplicável)
Base ICMS = (Valor Aduaneiro + II + IPI + PIS + COFINS + ICMS) ← por dentro = circular

Fórmula ICMS por dentro:
ICMS = Base ICMS × alíquota_ICMS / (1 - alíquota_ICMS)
```

---

## 1. Coolers CPU — Air Cooler (Hyper 212, MasterAir)

| Campo | Valor |
|-------|-------|
| **NCM** | **8414.51.00** |
| Descrição oficial | Ventiladores de mesa, assoalho, parede, teto, telhado ou janela, com motor elétrico incorporado |
| Capítulo SH | 84 — Reatores nucleares, caldeiras, máquinas, aparelhos e instrumentos mecânicos |
| **II** | **20%** |
| **IPI** | **15%** |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Antidumping | Não identificado para esta posição |
| Observações | Coolers que combinam heatsink + fan; classificar pelo componente principal (motor/fan). Ex-tarifário possível se sem similar nacional |

**Carga tributária estimada "por dentro" (sem ICMS):**
- Base: 100
- II: +20 → 120
- IPI: 15% × 120 = +18 → 138
- PIS: 2,10% × 138 = +2,90 → 140,90
- COFINS: 9,65% × 138 = +13,32 → 154,22
- **Carga federal total: ~54%** sobre valor aduaneiro

---

## 2. Coolers Líquidos AIO (MasterLiquid, MasterLiquid Pro)

| Campo | Valor |
|-------|-------|
| **NCM** | **8419.89.99** |
| Descrição oficial | Outros aparelhos e dispositivos para tratamento de matérias por processo que implica mudança de temperatura — outros, não especificados |
| Capítulo SH | 84 |
| **II** | **14%** |
| **IPI** | **10%** |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Antidumping | Não identificado |
| Observações | Classificação debatida. Alguns despachantes usam 8414.51.00. Recomenda-se consulta formal à RFB para coolers AIO mais complexos. A posição 8419 contempla melhor o sistema de troca de calor por líquido. |

> ⚠️ **ATENÇÃO:** A classificação de coolers líquidos AIO é controversa. Uma consulta formal à Receita Federal (via e-CAC) ou ADI pode ser necessária para segurança jurídica.

---

## 3. Fontes de Alimentação / PSU (MWE Gold, V Gold, XG, MWE Bronze)

| Campo | Valor |
|-------|-------|
| **NCM** | **8504.40.40** |
| Descrição oficial | Conversores estáticos — outros (conversores de frequência, de tensão) |
| Capítulo SH | 85 — Máquinas, aparelhos e materiais elétricos |
| **II** | **20%** |
| **IPI** | **15%** |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Antidumping | Verificar DECOM — pode haver medidas para PSU com origem China |
| Observações | PSUs para PC são conversores estáticos CA→CC. Verificar se há ex-tarifário aplicável (Portaria MDIC). Nobreaks se enquadram em 8504.40.10 ou 8504.40.20 |

**NCMs alternativos:**
- 8504.40.21 — Carregadores de acumuladores (NÃO se aplica a PSUs padrão)
- 8504.10.00 — Balastros para lâmpadas (NÃO se aplica)

---

## 4. Gabinetes / Cases (MasterBox, MasterCase, HAF, TD500, Q500L, Elite)

| Campo | Valor |
|-------|-------|
| **NCM** | **8473.30.90** |
| Descrição oficial | Partes e acessórios das máquinas da posição 84.71 (computadores) — outros |
| Capítulo SH | 84 |
| **II** | **0%** |
| **IPI** | **0%** (NT - Não-tributado) |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Antidumping | Não identificado |
| Observações | Gabinetes são "acessórios para computadores" na TEC. II = 0% beneficia a importação. Verificar se algum gabinete com painel LCD/displays tem classificação diferente. |

> ✅ **Destaque:** NCM 8473.30.90 tem **II = 0%**, reduzindo significativamente o custo de importação de cases vs. outras categorias.

---

## 5. Teclados Mecânicos e de Membrana (CK550, CK552, SK650, MK730)

| Campo | Valor |
|-------|-------|
| **NCM** | **8471.60.52** |
| Descrição oficial | Unidades de entrada — teclados |
| Capítulo SH | 84 |
| **II** | **20%** |
| **IPI** | **0%** (NT) |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Antidumping | Não identificado |
| Observações | O IPI zero deriva da TIPI para periféricos de computador. Teclados gaming com funcionalidades RGB/mecânicas são classificados da mesma forma. Teclados sem fio: mesma NCM. |

> **Lei de Informática (Lei 8.248/1991):** Se o produto for fabricado no Brasil com PPB, pode ter IPI reduzido na venda doméstica. Importações NÃO se beneficiam da redução de II da Lei de Informática — apenas isenção de IPI e tributação diferenciada de PIS/COFINS para produtos nacionais.

---

## 6. Mouses Gaming (MM711, MM720, MM530, MM731)

| Campo | Valor |
|-------|-------|
| **NCM** | **8471.60.53** |
| Descrição oficial | Unidades de entrada — unidades de cursor (mouses) |
| Capítulo SH | 84 |
| **II** | **20%** |
| **IPI** | **0%** (NT) |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Antidumping | Não identificado |
| Observações | Mouses sem fio, com receptor USB dongle, geralmente mantêm a mesma classificação. Verificar se o dongle USB vem como acessório incluído no valor. |

---

## 7. Headsets (MH630, MH650, MH670, MH751)

| Campo | Valor |
|-------|-------|
| **NCM** | **8518.30.00** |
| Descrição oficial | Fones de ouvido, mesmo combinados com microfone, e conjuntos ou "kits" de microfone e alto-falante |
| Capítulo SH | 85 |
| **II** | **20%** |
| **IPI** | **12%** |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Antidumping | Verificar — setor de áudio pode ter medidas antidumping para China |
| Observações | Headsets "gaming" com microfone boom se enquadram em 8518.30. Headphones sem microfone: 8518.30.00 também (comb. com mic.) ou 8518.10.00 para earbuds. |

---

## 8. Mousepads (MP510, MP750, MP860, MP860 RGB, Desk Pad)

### Mousepad de superfície dura (alumínio, borracha rígida):
| Campo | Valor |
|-------|-------|
| **NCM** | **3926.90.90** |
| Descrição | Outras obras de plástico e de outras matérias das posições 3901 a 3914 — outras |
| **II** | **20%** |
| **IPI** | **0%** (NT) ou variável |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |

### Mousepad de superfície em tecido/pano (soft pad):
| Campo | Valor |
|-------|-------|
| **NCM** | **6307.90.90** |
| Descrição | Outros artefatos confeccionados — outros (inclui artigos de tecido) |
| **II** | **35%** |
| **IPI** | **0%** (NT) |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |

> ⚠️ **ATENÇÃO:** Mousepads de tecido têm **II = 35%** — substancialmente maior. Classificar corretamente pode fazer diferença significativa de custo.

---

## 9. Ventoinhas / Fans (SickleFlow, MasterFan MF120, MF140, A-RGB)

| Campo | Valor |
|-------|-------|
| **NCM** | **8414.51.00** |
| Descrição oficial | Ventiladores de mesa, assoalho, parede, teto, telhado ou janela, com motor elétrico incorporado |
| Capítulo SH | 84 |
| **II** | **20%** |
| **IPI** | **15%** |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Antidumping | Verificar — ventiladores industriais podem ter antidumping; PC fans de 120/140mm geralmente não |
| Observações | Fans com controlador RGB/ARGB incluído: mesma NCM. Hub de controle de fans separado pode ser 8537.10.90. |

> **Nota:** Fans de PC (120/140mm) são ventiladores de mesa pela funcionalidade, mesmo que destinados a uso interno em gabinetes.

---

## 10. Cooler para GPU (VNXX, MasterAir MA410M GPU Edition)

| Campo | Valor |
|-------|-------|
| **NCM** | **8473.50.90** |
| Descrição | Partes e acessórios para as máquinas da posição 8471 — outros |
| **II** | **0%** |
| **IPI** | **0%** (NT) |
| **PIS Importação** | **2,10%** |
| **COFINS Importação** | **9,65%** |
| Observações | NCM alternativo: 8414.51.00 se considerado como fan assembly. Coolers de reposição para GPU são acessórios de informática. |

---

## Resumo Comparativo de Carga Tributária

| Categoria | NCM | II | IPI | PIS | COFINS | Carga Total* |
|-----------|-----|-----|-----|-----|--------|-------------|
| Air Cooler (CPU) | 8414.51.00 | 20% | 15% | 2,10% | 9,65% | ~66% |
| Liquid Cooler AIO | 8419.89.99 | 14% | 10% | 2,10% | 9,65% | ~55% |
| PSU / Fonte | 8504.40.40 | 20% | 15% | 2,10% | 9,65% | ~66% |
| Gabinete / Case | 8473.30.90 | 0% | 0% | 2,10% | 9,65% | ~18%** |
| Teclado | 8471.60.52 | 20% | 0% | 2,10% | 9,65% | ~47% |
| Mouse | 8471.60.53 | 20% | 0% | 2,10% | 9,65% | ~47% |
| Headset | 8518.30.00 | 20% | 12% | 2,10% | 9,65% | ~59% |
| Mousepad duro | 3926.90.90 | 20% | 0% | 2,10% | 9,65% | ~47% |
| Mousepad tecido | 6307.90.90 | 35% | 0% | 2,10% | 9,65% | ~66% |
| Fan 120/140mm | 8414.51.00 | 20% | 15% | 2,10% | 9,65% | ~66% |
| GPU Cooler | 8473.50.90 | 0% | 0% | 2,10% | 9,65% | ~18%** |

*Carga total aproximada sobre valor aduaneiro (CIF), sem ICMS, calculada em cascata.  
**Carga muito reduzida pela isenção de II, tornando estes produtos mais competitivos na importação.

---

## Antidumping — Produtos Potencialmente Afetados

Consultar o DECOM (Departamento de Defesa Comercial / SECEX) para medidas vigentes:
- **Portal:** https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial
- **Busca:** Por NCM no sistema SALI (Sistema de Acompanhamento de Investigações)

Produtos de eletroeletrônicos com origem China que historicamente tiveram investigação:
- Ventiladores (8414): verificar periodicamente
- Fontes de alimentação (8504): histórico de investigações
- Headsets (8518): sem medidas ativas recentes identificadas

---

## Ex-Tarifários (Redução de II)

Ex-tarifários permitem importar bens de capital e de informática com II reduzido (geralmente 0%) quando não há produção nacional similar.

**Como verificar:**
1. Acessar: https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/ex-tarifarios
2. Buscar por NCM no SISEX
3. Verificar se o produto CM se enquadra na descrição do ex-tarifário vigente

**Exemplos de ex-tarifários relevantes para CM:**
- Sistemas de resfriamento líquido especializados (8419): podem ter ex-tarifário
- Conversores de tensão industriais (8504): verificar no SISEX

---

## Fontes e Referências

- **TEC vigente:** Resolução GECEX nº 812/2025 (vigente em 16/02/2026)
- **TIPI:** Decreto nº 11.158, de 29 de julho de 2022 (com alterações posteriores)
- **PIS/COFINS importação:** Lei nº 10.865, de 30 de abril de 2004
- **Consulta NCM:** https://portalunico.siscomex.gov.br/classif/#/sumario?perfil=publico
- **Classificação fiscal (consulta formal):** Instrução Normativa RFB nº 1.464/2014
- **DECOM (antidumping):** https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial

> **AVISO IMPORTANTE:** As alíquotas indicadas são as alíquotas nominais da TEC e TIPI. Alíquotas específicas podem variar por:
> - Ex-tarifários vigentes (redução de II)
> - Acordos comerciais (Mercosul, ALADI)
> - Medidas antidumping ou compensatórias
> - Regimes especiais de importação
> 
> **Sempre verificar no Portal Classif antes de cada importação.**
