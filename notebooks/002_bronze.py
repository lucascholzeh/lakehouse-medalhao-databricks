# Databricks notebook source
# MAGIC %md
# MAGIC # 002 - Camada Bronze — Ingestão de Dados (Landing → Bronze)
# MAGIC
# MAGIC **Objetivo:** Ler os arquivos CSV do volume `landing.dados` e gravar como tabelas **Delta Lake** no schema `bronze`.
# MAGIC
# MAGIC ### O que acontece nesta camada?
# MAGIC - Leitura dos CSVs brutos sem nenhuma transformação de negócio
# MAGIC - Adição de colunas de **metadados de auditoria** (`data_hora_bronze`, `nome_arquivo`)
# MAGIC - Persistência no formato **Delta Lake** como tabelas **MANAGED**
# MAGIC
# MAGIC > **Tabelas geradas:** `bronze.apolice`, `bronze.carro`, `bronze.cliente`, `bronze.endereco`,
# MAGIC > `bronze.estado`, `bronze.marca`, `bronze.modelo`, `bronze.municipio`,
# MAGIC > `bronze.regiao`, `bronze.sinistro`, `bronze.telefone`

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Listar arquivos no volume Landing

# COMMAND ----------

display(dbutils.fs.ls('/Volumes/workspace/landing/dados/'))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Ler os CSVs do Landing para DataFrames Spark

# COMMAND ----------

caminho_landing = '/Volumes/workspace/landing/dados'

df_apolice   = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/apolice.csv")
df_carro     = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/carro.csv")
df_cliente   = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/cliente.csv")
df_endereco  = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/endereco.csv")
df_estado    = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/estado.csv")
df_marca     = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/marca.csv")
df_modelo    = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/modelo.csv")
df_municipio = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/municipio.csv")
df_regiao    = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/regiao.csv")
df_sinistro  = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/sinistro.csv")
df_telefone  = spark.read.option("inferSchema", "true").option("header", "true").csv(f"{caminho_landing}/telefone.csv")

print("DataFrames carregados com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Visualizar schema inferido (exemplo: apolice)

# COMMAND ----------

df_apolice.printSchema()
display(df_apolice.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Adicionar colunas de metadados de auditoria (Bronze)
# MAGIC
# MAGIC Colunas adicionadas:
# MAGIC - `data_hora_bronze` → timestamp de quando o dado foi ingerido
# MAGIC - `nome_arquivo`     → nome do arquivo CSV de origem (rastreabilidade)

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

df_apolice   = df_apolice.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("apolice.csv"))
df_carro     = df_carro.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("carro.csv"))
df_cliente   = df_cliente.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("cliente.csv"))
df_endereco  = df_endereco.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("endereco.csv"))
df_estado    = df_estado.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("estado.csv"))
df_marca     = df_marca.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("marca.csv"))
df_modelo    = df_modelo.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("modelo.csv"))
df_municipio = df_municipio.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("municipio.csv"))
df_regiao    = df_regiao.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("regiao.csv"))
df_sinistro  = df_sinistro.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("sinistro.csv"))
df_telefone  = df_telefone.withColumn("data_hora_bronze", current_timestamp()).withColumn("nome_arquivo", lit("telefone.csv"))

print("Metadados adicionados!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Gravar como Delta Lake no schema Bronze (tabelas MANAGED)

# COMMAND ----------

df_apolice.write.format('delta').mode("overwrite").saveAsTable("bronze.apolice")
df_carro.write.format('delta').mode("overwrite").saveAsTable("bronze.carro")
df_cliente.write.format('delta').mode("overwrite").saveAsTable("bronze.cliente")
df_endereco.write.format('delta').mode("overwrite").saveAsTable("bronze.endereco")
df_estado.write.format('delta').mode("overwrite").saveAsTable("bronze.estado")
df_marca.write.format('delta').mode("overwrite").saveAsTable("bronze.marca")
df_modelo.write.format('delta').mode("overwrite").saveAsTable("bronze.modelo")
df_municipio.write.format('delta').mode("overwrite").saveAsTable("bronze.municipio")
df_regiao.write.format('delta').mode("overwrite").saveAsTable("bronze.regiao")
df_sinistro.write.format('delta').mode("overwrite").saveAsTable("bronze.sinistro")
df_telefone.write.format('delta').mode("overwrite").saveAsTable("bronze.telefone")

print("✅ Todas as tabelas Bronze gravadas com sucesso!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Verificar tabelas criadas no schema Bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Verificar detalhes da tabela Delta (formato, localização, versão)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL bronze.apolice;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Verificar se é MANAGED ou EXTERNAL

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED bronze.apolice;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Consultar contagem de registros em todas as tabelas Bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'apolice'   AS tabela, COUNT(*) AS qtd FROM bronze.apolice   UNION ALL
# MAGIC SELECT 'carro',              COUNT(*)        FROM bronze.carro       UNION ALL
# MAGIC SELECT 'cliente',            COUNT(*)        FROM bronze.cliente     UNION ALL
# MAGIC SELECT 'endereco',           COUNT(*)        FROM bronze.endereco    UNION ALL
# MAGIC SELECT 'estado',             COUNT(*)        FROM bronze.estado      UNION ALL
# MAGIC SELECT 'marca',              COUNT(*)        FROM bronze.marca       UNION ALL
# MAGIC SELECT 'modelo',             COUNT(*)        FROM bronze.modelo      UNION ALL
# MAGIC SELECT 'municipio',          COUNT(*)        FROM bronze.municipio   UNION ALL
# MAGIC SELECT 'regiao',             COUNT(*)        FROM bronze.regiao      UNION ALL
# MAGIC SELECT 'sinistro',           COUNT(*)        FROM bronze.sinistro    UNION ALL
# MAGIC SELECT 'telefone',           COUNT(*)        FROM bronze.telefone
# MAGIC ORDER BY tabela;
