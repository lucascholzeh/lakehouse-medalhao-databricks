# 📊 Camadas da Arquitetura Medalhão

## 🟫 LANDING — Zona de Pouso

**Camada de entrada.** Nenhuma transformação é feita aqui.

| Atributo | Valor |
|----------|-------|
| Tipo | Unity Catalog **Volume** |
| Caminho | `/Volumes/workspace/landing/dados/` |
| Formato | CSV |
| Notebook | `001_preparando_ambiente.py` |

```sql
-- Criação do Volume
CREATE VOLUME IF NOT EXISTS workspace.landing.dados
  COMMENT 'Volume para upload dos arquivos CSV do sistema de seguro de veículos';
```

---

## 🥉 BRONZE — Ingestão Raw

**Dados brutos em Delta Lake.** Preserva o dado original com metadados.

| Atributo | Valor |
|----------|-------|
| Tipo | Tabelas Delta Lake **MANAGED** |
| Schema | `workspace.bronze` |
| Formato | Delta |
| Notebook | `002_bronze.py` |

### O que é adicionado no Bronze?

Duas colunas de auditoria são adicionadas a cada tabela:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `data_hora_bronze` | TIMESTAMP | Momento da ingestão |
| `nome_arquivo` | STRING | Nome do CSV de origem |

```python
# Exemplo de código do Bronze
df_cliente = spark.read.option("inferSchema","true").option("header","true").csv(f"{caminho}/cliente.csv")
df_cliente = df_cliente.withColumn("data_hora_bronze", current_timestamp())
                       .withColumn("nome_arquivo", lit("cliente.csv"))
df_cliente.write.format("delta").mode("overwrite").saveAsTable("bronze.cliente")
```

---

## 🥈 SILVER — Dados Confiáveis com Data Quality

**Dados tratados e validados.** Aplica regras de qualidade e padroniza nomenclatura.

| Atributo | Valor |
|----------|-------|
| Tipo | Tabelas Delta Lake **MANAGED** |
| Schema | `workspace.silver` |
| Formato | Delta |
| Notebook | `003_silver.py` |

### Regras de Data Quality aplicadas

| Regra | Implementação |
|-------|--------------|
| Remover duplicatas | `df.dropDuplicates()` |
| Filtrar PKs nulas | `df.filter(col(pk).isNotNull())` |
| Padronizar nomes de colunas | Expansão de prefixos (CD_→CODIGO_, VL_→VALOR_…) |
| Colunas em maiúsculo | `.upper()` em todos os nomes |
| Rastreabilidade | `NOME_TABELA_BRONZE`, `DATA_HORA_SILVER` |

### Mapeamento de prefixos

| Prefixo | Expansão |
|---------|---------|
| `CD_` | `CODIGO_` |
| `VL_` | `VALOR_` |
| `DT_` | `DATA_` |
| `NM_` | `NOME_` |
| `DS_` | `DESCRICAO_` |
| `NR_` | `NUMERO_` |
| `_UF` | `_SIGLA_ESTADO` |

---

## 🥇 GOLD — Modelagem Dimensional (Kimball)

**Star Schema pronto para análise.** Dimensões desnormalizadas + tabela fato com métricas.

| Atributo | Valor |
|----------|-------|
| Tipo | Tabelas Delta Lake **MANAGED** |
| Schema | `workspace.gold` |
| Formato | Delta |
| Notebook | `004_gold.py` |

### Tabelas criadas

| Tabela | Tipo | SK | Descrição |
|--------|------|-----|-----------|
| `dim_carro` | Dimensão | `SK_CARRO` (IDENTITY) | Veículos com marca e modelo |
| `dim_cliente` | Dimensão | `SK_CLIENTE` (IDENTITY) | Clientes segurados |
| `dim_localidade` | Dimensão | `SK_LOCALIDADE` (IDENTITY) | Hierarquia geográfica |
| `dim_tempo` | Dimensão | `DATA` (NK) | Calendário 2023–2026 |
| `fato_sinistro` | Fato | — | Sinistros com FKs e métricas |

### Métricas da Tabela Fato

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| `QTDE_SINISTRO` | INT | Quantidade de sinistros agrupados |
| `VALOR_PREJUIZO` | DECIMAL(15,2) | Soma do valor de prejuízo |

### Estratégia de carga: MERGE (SCD Type 1)

Todas as dimensões usam `MERGE INTO` para:
- **Inserir** novos registros
- **Atualizar** registros existentes que tiveram alterações
- **Não deletar** registros históricos (SCD Type 1)
