# Databricks notebook source
# MAGIC %md
# MAGIC # 003 - Camada Silver — Data Quality (Bronze → Silver)
# MAGIC
# MAGIC **Objetivo:** Aplicar regras de qualidade de dados e mover os dados do `bronze` para o `silver`.
# MAGIC
# MAGIC ### Regras de Data Quality aplicadas:
# MAGIC | Regra | Descrição |
# MAGIC |-------|-----------|
# MAGIC | Padronização de nomes | Colunas renomeadas para padrão legível (CD_ → CODIGO_, VL_ → VALOR_, etc.) |
# MAGIC | Uppercase | Todos os nomes de colunas em maiúsculo |
# MAGIC | Remoção de metadados Bronze | Colunas `data_hora_bronze` e `nome_arquivo` substituídas por metadados Silver |
# MAGIC | Rastreabilidade | Adição de `NOME_ARQUIVO_BRONZE` (origem) e `DATA_ARQUIVO_SILVER` (timestamp) |
# MAGIC | Remoção de duplicatas | `dropDuplicates()` em cada tabela |
# MAGIC | Filtro de nulos críticos | Registros com PKs nulas são removidos |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Ler tabelas Delta da camada Bronze

# COMMAND ----------

df_apolice   = spark.read.format("delta").table("bronze.apolice")
df_carro     = spark.read.format("delta").table("bronze.carro")
df_cliente   = spark.read.format("delta").table("bronze.cliente")
df_endereco  = spark.read.format("delta").table("bronze.endereco")
df_estado    = spark.read.format("delta").table("bronze.estado")
df_marca     = spark.read.format("delta").table("bronze.marca")
df_modelo    = spark.read.format("delta").table("bronze.modelo")
df_municipio = spark.read.format("delta").table("bronze.municipio")
df_regiao    = spark.read.format("delta").table("bronze.regiao")
df_sinistro  = spark.read.format("delta").table("bronze.sinistro")
df_telefone  = spark.read.format("delta").table("bronze.telefone")

print("Tabelas Bronze carregadas!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Definir funções de Data Quality

# COMMAND ----------

from pyspark.sql import functions as F

# ─── Regras de renomeação de prefixos ────────────────────────────────────────
def _apply_name_rules(colname: str) -> str:
    """
    Padroniza os nomes das colunas:
    - Converte para MAIÚSCULO
    - Expande prefixos abreviados (CD_ → CODIGO_, VL_ → VALOR_, etc.)
    """
    n = colname.upper()
    n = n.replace("CD_",  "CODIGO_")
    n = n.replace("VL_",  "VALOR_")
    n = n.replace("DT_",  "DATA_")
    n = n.replace("NM_",  "NOME_")
    n = n.replace("DS_",  "DESCRICAO_")
    n = n.replace("NR_",  "NUMERO_")
    n = n.replace("_UF",  "_SIGLA_ESTADO")
    return n

def _safe_drop(df, cols):
    """Remove colunas somente se existirem no DataFrame."""
    existing = set(df.columns)
    to_drop = [c for c in cols if c in existing]
    return df.drop(*to_drop) if to_drop else df

# ─── Pipeline principal de Data Quality ──────────────────────────────────────
def aplicar_data_quality(src_fqn: str, dest_fqn: str, pk_col: str = None):
    """
    Lê uma tabela Bronze (Delta managed), aplica DQ e salva na Silver.

    Parâmetros:
      src_fqn   : nome qualificado da origem  (ex.: 'bronze.apolice')
      dest_fqn  : nome qualificado do destino (ex.: 'silver.apolice')
      pk_col    : coluna de chave primária — registros com PK nula são descartados
    """
    df = spark.read.format("delta").table(src_fqn)

    # ── Regra 1: Remover duplicatas
    qtd_antes = df.count()
    df = df.dropDuplicates()
    qtd_apos_dedup = df.count()

    # ── Regra 2: Filtrar nulos em PK (se fornecida)
    if pk_col and pk_col.upper() in [c.upper() for c in df.columns]:
        col_real = [c for c in df.columns if c.upper() == pk_col.upper()][0]
        df = df.filter(F.col(col_real).isNotNull())

    qtd_final = df.count()

    # ── Regra 3: Remover colunas de metadados Bronze
    df = _safe_drop(df, ["data_hora_bronze", "nome_arquivo"])

    # ── Regra 4: Renomear colunas (padronizar nomenclatura)
    new_cols = [_apply_name_rules(c) for c in df.columns]
    df = df.toDF(*new_cols)

    # ── Regra 5: Adicionar metadados Silver
    df = (df
          .withColumn("NOME_TABELA_BRONZE",   F.lit(src_fqn))
          .withColumn("DATA_HORA_SILVER",      F.current_timestamp())
         )

    # ── Salvar como Managed Table Delta na Silver
    (df.write
       .format("delta")
       .mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable(dest_fqn))

    # ── Relatório de qualidade
    print(f"✅ {src_fqn} → {dest_fqn}")
    print(f"   Registros antes: {qtd_antes} | Após dedup: {qtd_apos_dedup} | Final: {qtd_final}")
    if qtd_antes > qtd_final:
        print(f"   ⚠️  {qtd_antes - qtd_final} registros descartados pelo DQ")
    print()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Aplicar Data Quality e gravar na Silver

# COMMAND ----------

aplicar_data_quality("bronze.apolice",   "silver.apolice",   pk_col="cd_apolice")
aplicar_data_quality("bronze.carro",     "silver.carro",     pk_col="placa")
aplicar_data_quality("bronze.cliente",   "silver.cliente",   pk_col="cd_cliente")
aplicar_data_quality("bronze.endereco",  "silver.endereco",  pk_col="cd_endereco")
aplicar_data_quality("bronze.estado",    "silver.estado",    pk_col="cd_estado")
aplicar_data_quality("bronze.marca",     "silver.marca",     pk_col="cd_marca")
aplicar_data_quality("bronze.modelo",    "silver.modelo",    pk_col="cd_modelo")
aplicar_data_quality("bronze.municipio", "silver.municipio", pk_col="cd_municipio")
aplicar_data_quality("bronze.regiao",    "silver.regiao",    pk_col="cd_regiao")
aplicar_data_quality("bronze.sinistro",  "silver.sinistro",  pk_col="cd_sinistro")
aplicar_data_quality("bronze.telefone",  "silver.telefone",  pk_col="cd_telefone")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Verificar tabelas criadas na Silver

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN silver;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Inspecionar schema da tabela Silver (exemplo: cliente)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED silver.cliente;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Validar dados — conferir colunas padronizadas

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.cliente LIMIT 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.apolice LIMIT 5;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Contagem final de registros Silver

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'apolice'   AS tabela, COUNT(*) AS qtd FROM silver.apolice   UNION ALL
# MAGIC SELECT 'carro',              COUNT(*)        FROM silver.carro       UNION ALL
# MAGIC SELECT 'cliente',            COUNT(*)        FROM silver.cliente     UNION ALL
# MAGIC SELECT 'endereco',           COUNT(*)        FROM silver.endereco    UNION ALL
# MAGIC SELECT 'estado',             COUNT(*)        FROM silver.estado      UNION ALL
# MAGIC SELECT 'marca',              COUNT(*)        FROM silver.marca       UNION ALL
# MAGIC SELECT 'modelo',             COUNT(*)        FROM silver.modelo      UNION ALL
# MAGIC SELECT 'municipio',          COUNT(*)        FROM silver.municipio   UNION ALL
# MAGIC SELECT 'regiao',             COUNT(*)        FROM silver.regiao      UNION ALL
# MAGIC SELECT 'sinistro',           COUNT(*)        FROM silver.sinistro    UNION ALL
# MAGIC SELECT 'telefone',           COUNT(*)        FROM silver.telefone
# MAGIC ORDER BY tabela;
