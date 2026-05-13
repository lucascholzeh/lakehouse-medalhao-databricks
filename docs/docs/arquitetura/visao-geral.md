# 🏗️ Visão Geral da Arquitetura

## Lakehouse vs. Data Warehouse vs. Data Lake

| Característica | Data Lake | Data Warehouse | **Lakehouse** |
|---------------|-----------|----------------|--------------|
| Formatos suportados | Qualquer | Estruturado | **Qualquer** |
| Transações ACID | ❌ | ✅ | ✅ |
| Performance BI | ❌ | ✅ | ✅ |
| Custo de armazenamento | Baixo | Alto | **Baixo** |
| Governança | Difícil | Fácil | **Fácil** |

O **Lakehouse** combina o melhor dos dois mundos: a flexibilidade e o baixo custo do Data Lake com a confiabilidade e a performance analítica do Data Warehouse.

---

## Arquitetura Medalhão

A Arquitetura Medalhão organiza os dados em **três camadas progressivas de qualidade**:

### 🟫 Landing (Zona de Pouso)
- Ponto de entrada dos dados brutos
- Arquivos CSV armazenados em um **Volume** do Unity Catalog
- **Nenhuma transformação** é aplicada
- Serve como área de staging antes da ingestão

### 🥉 Bronze (Raw)
- Dados ingeridos **sem transformação de negócio**
- Armazenados em formato **Delta Lake**
- Adição de **metadados de auditoria** (timestamp, nome do arquivo)
- Tabelas do tipo **MANAGED** no Unity Catalog

### 🥈 Silver (Confiável)
- Regras de **Data Quality** aplicadas
- Padronização de nomenclatura de colunas
- Remoção de duplicatas e registros inválidos
- Rastreabilidade completa da origem

### 🥇 Gold (Analytics-Ready)
- **Modelagem dimensional** Ralph Kimball
- **Star Schema** com dimensões e tabela fato
- **Surrogate Keys** geradas automaticamente
- Pronto para consumo em ferramentas de BI

---

## Componentes do Databricks utilizados

```
Unity Catalog
├── workspace (catálogo)
│   ├── landing (schema)
│   │   └── dados (volume) ← Upload dos CSVs aqui
│   ├── bronze (schema)
│   │   ├── apolice (tabela Delta)
│   │   ├── carro
│   │   └── ... (11 tabelas)
│   ├── silver (schema)
│   │   └── ... (11 tabelas)
│   └── gold (schema)
│       ├── dim_carro
│       ├── dim_cliente
│       ├── dim_localidade
│       ├── dim_tempo
│       └── fato_sinistro
│
Notebooks
├── 001_preparando_ambiente.py
├── 002_bronze.py
├── 003_silver.py
└── 004_gold.py
│
Workflows (Jobs)
└── pipeline_lakehouse_medaliao (Job com 4 tasks encadeadas)
```
