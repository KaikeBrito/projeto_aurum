# 🗺️ Sistema de Mapeamento Ticker ↔ CNPJ

Sistema profissional e automatizado para mapear tickers da B3 (ABEV3, PETR4, etc.) com CNPJs da CVM, essencial para juntar dados de preços com dados fundamentalistas.

## 📋 Índice

- [Características](#características)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Uso Rápido](#uso-rápido)
- [Uso Avançado](#uso-avançado)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Níveis de Matching](#níveis-de-matching)
- [Validações](#validações)
- [Casos Especiais](#casos-especiais)
- [Troubleshooting](#troubleshooting)

---

## ✨ Características

### 🎯 **Matching Inteligente Multi-Nível**
- ✅ 5 níveis de matching com scores de confiança (70-100%)
- ✅ Validação de CNPJ com dígitos verificadores
- ✅ Fuzzy matching por razão social (similaridade de strings)
- ✅ Suporte a overrides manuais (prioridade máxima)
- ✅ Tratamento de casos especiais (UNITs, ON/PN, BDRs)

### 📊 **Qualidade e Auditoria**
- ✅ Relatório detalhado de qualidade
- ✅ Audit log completo (todas as operações)
- ✅ Versionamento automático
- ✅ Detecção de problemas (CNPJs inválidos, baixa confiança)

### 🔄 **Múltiplas Fontes de Dados**
- ✅ CVM (dados fundamentalistas)
- ✅ B3 (tickers IBRX100)
- ✅ Dados históricos (validação de tickers ativos)
- ✅ Override manual (correções)

### 🚀 **Performance e Escalabilidade**
- ✅ Processamento em lote otimizado
- ✅ Cache de resultados
- ✅ Índices para buscas rápidas
- ✅ Suporte a 1000+ tickers

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                      CAMADA DE CONFIGURAÇÃO                      │
│  config.py - Parâmetros centralizados, paths, casos especiais   │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                      CAMADA DE EXTRAÇÃO                          │
│  extractors.py                                                   │
│  ├─ CVMExtractor: CNPJs da CVM                                  │
│  ├─ B3Extractor: Tickers IBRX100                                │
│  ├─ ManualOverrideExtractor: Correções manuais                  │
│  └─ HistoricalExtractor: Validação de tickers ativos            │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                      CAMADA DE VALIDAÇÃO                         │
│  validators.py                                                   │
│  ├─ CNPJValidator: Dígitos verificadores                        │
│  ├─ TickerValidator: Formato e classes                          │
│  └─ DataValidator: Consistência temporal                        │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                      MOTOR DE MATCHING                           │
│  matching_engine.py                                              │
│  ├─ Nível 1: Manual Override (100%)                             │
│  ├─ Nível 2: Grupos mesmo CNPJ (98%)                            │
│  ├─ Nível 3: Mapeamento existente (95%)                         │
│  ├─ Nível 4: Fuzzy matching (75-90%)                            │
│  └─ Nível 5: Histórico (80%)                                    │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                      ORQUESTRADOR                                │
│  create_map.py                                                   │
│  ├─ Fase 1: Extração de dados                                   │
│  ├─ Fase 2: Matching inteligente                                │
│  ├─ Fase 3: Enriquecimento de metadados                         │
│  ├─ Fase 4: Validação de resultados                             │
│  ├─ Fase 5: Salvamento de arquivos                              │
│  └─ Fase 6: Geração de relatórios                               │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                      OUTPUTS                                     │
│  ├─ ticker_cnpj_master.parquet - Dataset master completo        │
│  ├─ ticker_cnpj_map.parquet - Formato compatível (legacy)       │
│  ├─ quality_report.txt - Relatório de qualidade                 │
│  ├─ audit_log.json - Log de auditoria                           │
│  └─ versions/ - Histórico de versões                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Instalação

### Dependências

```bash
pip install pandas pyarrow fuzzywuzzy python-Levenshtein yfinance
```

### Estrutura de Diretórios

```
aurum/
├── mapeadores/
│   ├── __init__.py
│   ├── config.py
│   ├── validators.py
│   ├── extractors.py
│   ├── matching_engine.py
│   ├── create_map.py
│   ├── cli.py
│   ├── README.md
│   └── manual_reference_example.json
├── data/
│   ├── tickers_ibrx100_full.parquet  # Tickers B3
│   ├── cvm/
│   │   └── final/
│   │       └── fundamentals_wide.parquet  # Dados CVM
│   └── mapping/  # Outputs serão salvos aqui
│       ├── ticker_cnpj_master.parquet
│       ├── quality_report.txt
│       └── audit_log.json
```

---

## 🚀 Uso Rápido

### 1️⃣ Criar Mapa Completo (CLI)

```bash
# Comando mais simples - cria mapa completo
python -m aurum.mapeadores.cli create

# Com versão específica
python -m aurum.mapeadores.cli create --version 1.1.0
```

### 2️⃣ Criar Mapa (Python)

```python
from aurum.mapeadores import create_ticker_cnpj_map

# Criar mapa completo
success = create_ticker_cnpj_map(version="1.0.0")

if success:
    print("✅ Mapa criado com sucesso!")
```

### 3️⃣ Usar o Mapa

```python
import pandas as pd

# Carregar mapa
df_map = pd.read_parquet("aurum/data/mapping/ticker_cnpj_master.parquet")

# Consultar CNPJ de um ticker
cnpj_abev3 = df_map[df_map['ticker_simple'] == 'ABEV3']['CNPJ_CIA'].values[0]
print(f"CNPJ da ABEV3: {cnpj_abev3}")

# Filtrar apenas matches de alta confiança
df_high_confidence = df_map[df_map['confiabilidade'] >= 90]

# Juntar com dados de preços
df_prices = pd.read_parquet("aurum/data/historical/all_histories_cleaned.parquet")
df_merged = df_prices.merge(df_map[['ticker', 'CNPJ_CIA', 'DENOM_CIA']], on='ticker')
```

---

## 🔧 Uso Avançado

### CLI Completo

```bash
# Validar CNPJ
python -m aurum.mapeadores.cli validate-cnpj "07.526.557/0001-00"

# Validar Ticker
python -m aurum.mapeadores.cli validate-ticker ABEV3

# Adicionar override manual
python -m aurum.mapeadores.cli add-override BBAS3 "00.000.000/0001-91" "BANCO DO BRASIL S.A." \
    --observacao "CNPJ corrigido manualmente"

# Formatar CNPJ
python -m aurum.mapeadores.cli format-cnpj 07526557000100

# Informações do sistema
python -m aurum.mapeadores.cli info
```

### Pipeline Customizado

```python
from aurum.mapeadores.create_map import TickerCNPJMapper

# Criar instância
mapper = TickerCNPJMapper(version="1.0.0")

# Executar fases individualmente
mapper.extract_data()          # Fase 1: Extração
mapper.perform_matching()      # Fase 2: Matching
mapper.enrich_metadata()       # Fase 3: Enriquecimento
mapper.validate_results()      # Fase 4: Validação
mapper.save_results()          # Fase 5: Salvamento
mapper.generate_quality_report()  # Fase 6: Relatório

# Ou executar tudo de uma vez
mapper.run_full_pipeline()
```

### Adicionar Override Manual

```python
from aurum.mapeadores.extractors import ManualOverrideExtractor

extractor = ManualOverrideExtractor()

extractor.add_override(
    ticker_simple="BBAS3",
    cnpj="00.000.000/0001-91",
    razao_social="BANCO DO BRASIL S.A.",
    observacao="CNPJ corrigido - anterior era de teste"
)
```

### Validações

```python
from aurum.mapeadores.validators import validate_cnpj, validate_ticker

# Validar CNPJ
result = validate_cnpj("07.526.557/0001-00")
print(result)
# {
#     'valid': True,
#     'reason': 'CNPJ válido',
#     'formatted': '07.526.557/0001-00',
#     'clean': '07526557000100'
# }

# Validar Ticker
result = validate_ticker("ABEV3")
print(result)
# {
#     'valid': True,
#     'ticker_full': 'ABEV3.SA',
#     'ticker_simple': 'ABEV3',
#     'base': 'ABEV',
#     'class': '3',
#     'type': 'ON',
#     'is_unit': False,
#     'is_bdr': False
# }
```

---

## 📁 Estrutura de Arquivos

### Outputs

| Arquivo | Descrição | Formato |
|---------|-----------|---------|
| `ticker_cnpj_master.parquet` | **Dataset master completo** com todos os metadados | Parquet + CSV |
| `ticker_cnpj_map.parquet` | Versão simplificada (compatível com código legado) | Parquet + CSV |
| `quality_report.txt` | Relatório de qualidade detalhado | TXT |
| `audit_log.json` | Log completo de todas as operações | JSON |
| `versions/ticker_cnpj_master_v*.parquet` | Histórico de versões | Parquet |

### Colunas do Master Dataset

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `ticker` | str | Ticker completo (ABEV3.SA) |
| `ticker_simple` | str | Ticker sem sufixo (ABEV3) |
| `CNPJ_CIA` | str | CNPJ formatado (00.000.000/0001-00) |
| `DENOM_CIA` | str | Razão social da empresa |
| `tipo_ativo` | str | ON, PN, UNIT, BDR, etc. |
| `classe` | str | 3, 4, 5, 6, 11, etc. |
| `is_unit` | bool | É UNIT? |
| `is_bdr` | bool | É BDR? |
| `is_ibrx100` | bool | Faz parte do IBRX100? |
| `tem_dados_recentes` | bool | Tem dados históricos recentes (30 dias)? |
| `fonte_match` | str | Método de matching usado |
| `confiabilidade` | int | Score 0-100 |
| `status_qualidade` | str | EXCELENTE, BOM, ACEITAVEL, REQUER_REVISAO |
| `cnpj_validado` | bool | CNPJ passou na validação? |
| `versao` | str | Versão do dataset |
| `data_criacao` | str | Timestamp de criação |
| `hash_registro` | str | Hash MD5 para controle de mudanças |

---

## 🎯 Níveis de Matching

### Nível 1: Manual Override (100% confiança)
- **Fonte**: `manual_reference.json`
- **Uso**: Correções manuais validadas
- **Exemplo**: BBAS3 → CNPJ corrigido manualmente

### Nível 2: Grupos com Mesmo CNPJ (98% confiança)
- **Fonte**: `config.SAME_CNPJ_GROUPS`
- **Uso**: ON e PN da mesma empresa
- **Exemplo**: BBDC3 e BBDC4 têm o mesmo CNPJ

### Nível 3: Mapeamento Existente (95% confiança)
- **Fonte**: `ticker_cnpj_map.parquet` (versão anterior)
- **Uso**: Reutilizar matches já validados
- **Exemplo**: Match encontrado em mapeamento anterior

### Nível 4: Fuzzy Matching (75-90% confiança)
- **Fonte**: Similaridade de strings (Levenshtein)
- **Uso**: Matching por razão social
- **Exemplo**: "AMBEV S.A." ≈ "AMBEV SA" (score: 95)

### Nível 5: Histórico (80% confiança)
- **Fonte**: `config.TICKER_HISTORY`
- **Uso**: Mudanças conhecidas de ticker
- **Exemplo**: ITUB3 era ITUB4

---

## ✅ Validações

### Validação de CNPJ

```python
# Validações realizadas:
✅ Tamanho (14 dígitos)
✅ Dígitos verificadores (algoritmo da Receita Federal)
✅ CNPJs conhecidos como inválidos (00.000.000/0001-91, etc.)
✅ Padrões suspeitos (todos os dígitos iguais)
```

### Validação de Ticker

```python
# Validações realizadas:
✅ Formato correto (4 letras + 1-2 dígitos)
✅ Classe válida (3, 4, 5, 6, 11, 32, 33, 34)
✅ Tipo de ativo (ON, PN, UNIT, BDR)
```

---

## 🔧 Casos Especiais

### 1️⃣ UNITs (Pacotes de Ações)

Tickers terminados em **11** são UNITs (pacotes de ON + PN):

```python
# Exemplos de UNITs
BPAC11  # BTG Pactual Unit
ENGI11  # Energisa Unit
IGTI11  # Iguatemi Unit
SANB11  # Santander Unit
TAEE11  # Taesa Unit
```

**Tratamento**: Usa CNPJ da empresa principal.

### 2️⃣ Múltiplas Classes (ON/PN)

Mesmo CNPJ para diferentes classes:

```python
# Mesmo CNPJ
BBDC3 (ON)  e BBDC4 (PN)  → 60.746.948/0001-12
PETR3 (ON)  e PETR4 (PN)  → 33.000.167/0001-01
CMIG3 (ON)  e CMIG4 (PN)  → 17.155.730/0001-64
ELET3 (ON)  e ELET6 (PNB) → 00.001.180/0001-26
```

**Tratamento**: Sistema detecta automaticamente e usa mesmo CNPJ.

### 3️⃣ BDRs (Brazilian Depositary Receipts)

Tickers terminados em **32, 33, 34**:

```python
# Exemplos de BDRs
AAPL34  # Apple BDR
MSFT34  # Microsoft BDR
GOGL34  # Google BDR
```

**Tratamento**: Identificados como BDRs, podem não ter CNPJ brasileiro.

---

## 📊 Exemplo de Relatório de Qualidade

```
================================================================================
RELATÓRIO DE QUALIDADE - SISTEMA DE MAPEAMENTO TICKER ↔ CNPJ
================================================================================
Versão: 1.0.0
Data: 2025-12-11 14:30:00
Total de registros: 98
================================================================================

📊 ESTATÍSTICAS GERAIS
--------------------------------------------------------------------------------
Total de tickers: 98
Com CNPJ mapeado: 95
Sem CNPJ: 3
Taxa de cobertura: 96.9%

Confiança média: 94.2%
Confiança mediana: 95.0%
Confiança mínima: 75.0%
Confiança máxima: 100.0%


🔍 DISTRIBUIÇÃO POR MÉTODO DE MATCHING
--------------------------------------------------------------------------------
existing_map.................... 85 (86.7%)
manual_override.................  8 ( 8.2%)
fuzzy_name......................  3 ( 3.1%)
same_cnpj_group.................  2 ( 2.0%)


⭐ DISTRIBUIÇÃO POR STATUS DE QUALIDADE
--------------------------------------------------------------------------------
EXCELENTE....................... 85 (86.7%)
BOM.............................  8 ( 8.2%)
ACEITAVEL.......................  3 ( 3.1%)
SEM_CNPJ........................  2 ( 2.0%)


⚠️ PROBLEMAS IDENTIFICADOS
--------------------------------------------------------------------------------

🔴 Tickers SEM CNPJ (2):
   • XPTO3
   • XYZW4

💡 RECOMENDAÇÕES
--------------------------------------------------------------------------------
• Adicionar 2 ticker(s) ao arquivo de override manual

================================================================================
FIM DO RELATÓRIO
================================================================================
```

---

## 🛠️ Troubleshooting

### Problema: "Arquivo não encontrado: tickers_ibrx100_full.parquet"

**Solução**: Verificar se o arquivo existe no caminho correto:

```python
from aurum.mapeadores.config import config
print(config.TICKERS_FILE.exists())
```

### Problema: "CNPJ inválido no mapeamento"

**Solução**: Adicionar override manual:

```bash
python -m aurum.mapeadores.cli add-override BBAS3 "00.000.000/0001-91" "BANCO DO BRASIL S.A."
```

### Problema: "Baixa taxa de matching"

**Solução**: Ajustar threshold de fuzzy matching:

```python
from aurum.mapeadores.config import config
config.FUZZY_THRESHOLD = 80  # Reduzir de 85 para 80
```

### Problema: "Ticker não encontrado"

**Verificações**:
1. Ticker está no arquivo IBRX100?
2. Formato está correto (ABEV3, não ABEV3.SA)?
3. Empresa está nos dados da CVM?

---

## 📚 Referências

- [CVM - Dados Abertos](https://dados.cvm.gov.br/)
- [B3 - Empresas Listadas](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm)
- [Receita Federal - Validação CNPJ](http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/Cnpjreva_Solicitacao.asp)

---

## 📝 Changelog

### v1.0.0 (2025-12-11)
- ✅ Implementação inicial completa
- ✅ 5 níveis de matching inteligente
- ✅ Validações de CNPJ e Ticker
- ✅ Sistema de auditoria e versionamento
- ✅ Relatórios de qualidade
- ✅ CLI completa
- ✅ Suporte a casos especiais (UNITs, ON/PN, BDRs)

---

## 👤 Autor

**Projeto Aurum**
Sistema de Análise Quantitativa de Ações Brasileiras

---

## 📄 Licença

MIT License - Uso livre para fins educacionais e comerciais.

---

**🎉 Sistema pronto para produção!**
