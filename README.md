<div align="center">

# 🏆 Lakehouse com Databricks — Arquitetura Medalhão

**Trabalho Prático — Engenharia de Dados**
Curso de Engenharia de Software

[![Databricks](https://img.shields.io/badge/Databricks-Free%20Edition-FF3621?logo=databricks&logoColor=white)](https://community.cloud.databricks.com)
[![Delta Lake](https://img.shields.io/badge/Delta%20Lake-3.0-003366?logo=apachespark&logoColor=white)](https://delta.io)
[![PySpark](https://img.shields.io/badge/PySpark-3.5-E25A1C?logo=apachespark&logoColor=white)](https://spark.apache.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Sobre o Projeto

Implementação de um **Lakehouse** completo na plataforma **Databricks Community Edition** utilizando a **Arquitetura Medalhão** (Landing → Bronze → Silver → Gold) sobre um domínio de **Seguro de Veículos**.

O projeto demonstra todo o pipeline de dados desde a extração bruta de CSVs até a modelagem dimensional **Star Schema (Ralph Kimball)**, com automação via **Jobs & Pipelines** do Databricks.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATABRICKS UNITY CATALOG                        │
│                                                                         │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────┐ │
│  │   LANDING   │    │    BRONZE    │    │   SILVER    │    │  GOLD   │ │
│  │─────────────│    │──────────────│    │─────────────│    │─────────│ │
│  │ Volume com  │───▶│ Delta Lake   │───▶│ Delta Lake  │───▶│  Star   │ │
│  │ CSVs brutos │    │ Dados brutos │    │ DQ aplicado │    │ Schema  │ │
│  │             │    │ + metadados  │    │ padronizado │    │ Kimball │ │
│  └─────────────┘    └──────────────┘    └─────────────┘    └─────────┘ │
│       ↑                  ↑                    ↑                  ↑      │
│  Notebook 001       Notebook 002         Notebook 003       Notebook 004│
└─────────────────────────────────────────────────────────────────────────┘
                                    ↑
                         JOB: Execução sequencial automática
```

---

## 📁 Estrutura do Repositório

```
lakehouse-project/
│
├── 📂 notebooks/
│   ├── 001_preparando_ambiente.py   # Criação de schemas e volumes
│   ├── 002_bronze.py                # Ingestão CSV → Delta Lake
│   ├── 003_silver.py                # Data Quality Bronze → Silver
│   └── 004_gold.py                  # Modelagem Dimensional Silver → Gold
│
├── 📂 data/
│   ├── apolice.csv      # Apólices de seguro (40 registros)
│   ├── carro.csv        # Veículos segurados (40 registros)
│   ├── cliente.csv      # Clientes (20 registros)
│   ├── endereco.csv     # Endereços (20 registros)
│   ├── estado.csv       # Estados brasileiros (15 registros)
│   ├── marca.csv        # Marcas de veículos (8 registros)
│   ├── modelo.csv       # Modelos de veículos (16 registros)
│   ├── municipio.csv    # Municípios (20 registros)
│   ├── regiao.csv       # Regiões do Brasil (5 registros)
│   ├── sinistro.csv     # Sinistros ocorridos (80 registros)
│   └── telefone.csv     # Telefones dos clientes (20 registros)
│
├── 📂 docs/             # Documentação MkDocs
│   ├── mkdocs.yml
│   └── docs/
│       ├── index.md
│       ├── arquitetura/
│       ├── notebooks/
│       └── guias/
│
└── README.md
```

---

## 🗄️ Modelo de Dados

### Modelo Relacional (Landing/Bronze/Silver)

```
regiao ──< estado ──< municipio ──< endereco ──< cliente ──< apolice ──< sinistro
                                                                │
                                      modelo ──< carro ───────┘
                                      marca ─/
```

### Star Schema — Gold (Ralph Kimball)

```
                   ┌──────────────────┐
                   │    DIM_TEMPO     │
                   │  PK: DATA        │
                   │  ANO, MES,       │
                   │  NOME_MES, DIA,  │
                   │  TRIMESTRE, ...  │
                   └────────┬─────────┘
                            │ FK_TEMPO
 ┌───────────────┐  ┌───────┴──────────┐  ┌──────────────────┐
 │   DIM_CARRO   │  │  FATO_SINISTRO   │  │  DIM_LOCALIDADE  │
 │  PK: SK_CARRO │──│  FK_TEMPO        │──│  PK: SK_LOCAL.   │
 │  PLACA        │  │  FK_LOCALIDADE   │  │  CODIGO_MUNICIPIO│
 │  MARCA        │  │  FK_CARRO        │  │  NOME_MUNICIPIO  │
 │  MODELO       │  │  FK_CLIENTE      │  │  SIGLA_ESTADO    │
 │  COR, ANO     │  │  QTDE_SINISTRO   │  │  NOME_ESTADO     │
 └───────────────┘  │  VALOR_PREJUIZO  │  │  NOME_REGIAO     │
                    └────────┬─────────┘  └──────────────────┘
                             │ FK_CLIENTE
                   ┌─────────┴────────┐
                   │   DIM_CLIENTE    │
                   │  PK: SK_CLIENTE  │
                   │  CODIGO_CLIENTE  │
                   │  NOME, CPF       │
                   │  SEXO, DT_NASC   │
                   └──────────────────┘
```

---

## 🚀 Como Executar

### Pré-requisitos
- Conta no [Databricks Community Edition](https://community.cloud.databricks.com) (gratuita)
- Cluster ativo (DBR 13.x ou superior)
- Git instalado localmente

### Passo 1 — Clonar o repositório
```bash
git clone https://github.com/seu-usuario/lakehouse-databricks-medaliao.git
```

### Passo 2 — Fazer upload dos CSVs no Databricks

1. Acesse **Catalog** no menu lateral
2. Navegue até **workspace → landing → dados**
3. Clique em **Upload to this volume**
4. Selecione todos os arquivos da pasta `data/`

> Se o volume ainda não existir, execute o Notebook 001 primeiro.

### Passo 3 — Importar os notebooks

1. No Databricks, vá em **Workspace → Import**
2. Escolha **URL** e importe cada arquivo `.py` da pasta `notebooks/`

   Ou use o **Repos** do Databricks:
   - Vá em **Repos → Add Repo**
   - Cole a URL do seu repositório GitHub
   - Sincronize automaticamente

### Passo 4 — Executar os notebooks em ordem

Execute sequencialmente na ordem numérica:

| # | Notebook | Ação |
|---|----------|------|
| 1 | `001_preparando_ambiente.py` | Cria schemas e volume |
| 2 | `002_bronze.py` | Ingere CSVs → Delta Lake Bronze |
| 3 | `003_silver.py` | Aplica DQ → Delta Lake Silver |
| 4 | `004_gold.py` | Modela Star Schema → Gold |

### Passo 5 — Criar o JOB de automação

1. Vá em **Workflows → Create Job**
2. Adicione as 4 tasks na ordem abaixo:
   ```
   Task 1: preparando_ambiente  → Notebook 001
   Task 2: ingestao_bronze      → Notebook 002  [depende de: Task 1]
   Task 3: data_quality_silver  → Notebook 003  [depende de: Task 2]
   Task 4: modelagem_gold       → Notebook 004  [depende de: Task 3]
   ```
3. Configure o cluster para cada task
4. Clique em **Run Now** para executar o pipeline completo

---

## 📊 Camadas da Arquitetura Medalhão

### 🟫 LANDING — Zona de Pouso
- Armazenamento de arquivos CSV brutos no **Volume** do Unity Catalog
- **Nenhuma transformação** aplicada
- Caminho: `/Volumes/workspace/landing/dados/`

### 🥉 BRONZE — Ingestão Raw
- Leitura dos CSVs com inferência de schema
- Adição de metadados: `data_hora_bronze` e `nome_arquivo`
- Formato: **Delta Lake** (tabelas MANAGED)
- **11 tabelas** criadas

### 🥈 SILVER — Dados Confiáveis
- **Regras de Data Quality:**
  - Remoção de duplicatas (`dropDuplicates`)
  - Filtro de registros com chave primária nula
  - Padronização de nomes de colunas (CD_ → CODIGO_, VL_ → VALOR_, etc.)
  - Adição de metadados Silver (`DATA_HORA_SILVER`, `NOME_TABELA_BRONZE`)
- Formato: **Delta Lake** (tabelas MANAGED)
- **11 tabelas** criadas

### 🥇 GOLD — Análise e BI
- **Modelagem dimensional Ralph Kimball** (Star Schema)
- Surrogate Keys geradas automaticamente (IDENTITY)
- **Merge SCD Type 1** para atualização incremental
- **4 dimensões + 1 fato**
- Formato: **Delta Lake** (tabelas MANAGED)

---

## 🔧 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Databricks Community | Free | Plataforma de execução |
| Apache Spark | 3.5 | Engine de processamento |
| Delta Lake | 3.0 | Formato de armazenamento |
| PySpark | 3.5 | Transformações Python |
| Unity Catalog | — | Governança e metadados |
| SQL | — | DDL/DML das camadas |

---

## 📚 Conceitos Aplicados

- **Lakehouse Architecture** — unificação de Data Lake + Data Warehouse
- **Arquitetura Medalhão** — camadas Landing, Bronze, Silver, Gold
- **Delta Lake** — ACID transactions, time travel, schema evolution
- **Data Quality** — validação, padronização e rastreabilidade
- **Star Schema (Kimball)** — dimensões, fato, surrogate keys, SCD Type 1
- **Unity Catalog** — catálogo centralizado, volumes, schemas
- **Databricks Jobs** — orquestração e automação de pipelines

---

## 👨‍💻 Autor

Desenvolvido como atividade prática da disciplina de **Engenharia de Dados**
Curso de Engenharia de Software

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
