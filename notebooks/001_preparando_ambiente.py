# Databricks notebook source
# MAGIC %md
# MAGIC # 001 - Preparando o Ambiente — Lakehouse Medalhão
# MAGIC
# MAGIC **Objetivo:** Criar os schemas (databases) e o volume de landing no Unity Catalog.
# MAGIC
# MAGIC | Camada | Tipo | Finalidade |
# MAGIC |--------|------|------------|
# MAGIC | `landing.dados` | Volume | Arquivos CSV brutos da origem |
# MAGIC | `bronze` | Schema Delta | Ingestão raw em Delta Lake |
# MAGIC | `silver` | Schema Delta | Dados tratados com Data Quality |
# MAGIC | `gold`   | Schema Delta | Modelagem dimensional (Kimball) |
# MAGIC
# MAGIC > **⚠️ Atenção:** Substitua `workspace` pelo nome do seu catálogo, caso seja diferente.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Verificar o catálogo ativo

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_catalog(), current_database();

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Criar os Schemas e o Volume de Landing

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- Schema para armazenar os arquivos CSV brutos (landing zone)
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.landing
# MAGIC   COMMENT 'Schema para a zona de pouso — arquivos CSV brutos da origem';
# MAGIC
# MAGIC -- Volume gerenciado onde os CSVs serão carregados manualmente
# MAGIC CREATE VOLUME IF NOT EXISTS workspace.landing.dados
# MAGIC   COMMENT 'Volume para upload dos arquivos CSV do sistema de seguro de veículos';
# MAGIC
# MAGIC -- Schema Bronze: dados brutos em formato Delta Lake
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.bronze
# MAGIC   COMMENT 'Camada Bronze — dados brutos ingeridos em Delta Lake (sem transformação)';
# MAGIC
# MAGIC -- Schema Silver: dados tratados e com Data Quality aplicado
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.silver
# MAGIC   COMMENT 'Camada Silver — dados tratados, padronizados e com regras de qualidade';
# MAGIC
# MAGIC -- Schema Gold: modelagem dimensional Ralph Kimball
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.gold
# MAGIC   COMMENT 'Camada Gold — modelo dimensional (Star Schema) para análise e BI';

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Verificar schemas criados

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN workspace;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Verificar o volume criado

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES IN workspace.landing;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Listar arquivos no volume (após upload dos CSVs)
# MAGIC
# MAGIC > **📌 Próximo passo manual:**
# MAGIC > 1. No menu lateral, acesse **Catalog → workspace → landing → dados**
# MAGIC > 2. Clique em **Upload to this volume**
# MAGIC > 3. Faça o upload de todos os arquivos `.csv` da pasta `data/` do repositório
# MAGIC > 4. Execute a célula abaixo para confirmar

# COMMAND ----------

display(dbutils.fs.ls('/Volumes/workspace/landing/dados/'))
