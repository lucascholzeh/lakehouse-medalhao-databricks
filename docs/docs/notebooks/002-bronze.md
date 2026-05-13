# 📓 Notebook 002 — Camada Bronze

**Arquivo:** `notebooks/002_bronze.py`

## Objetivo

Ler os CSVs do volume `landing.dados` e persistir como tabelas **Delta Lake** no schema `bronze`, adicionando metadados de auditoria.

## Fluxo

```
/Volumes/workspace/landing/dados/*.csv
          ↓  spark.read.csv()
     DataFrame Spark
          ↓  withColumn(metadados)
     DataFrame + data_hora_bronze + nome_arquivo
          ↓  write.format("delta").saveAsTable()
     bronze.{tabela} (Delta MANAGED)
```

## Tabelas geradas

| Tabela Bronze | Registros |
|--------------|-----------|
| `bronze.apolice` | 40 |
| `bronze.carro` | 40 |
| `bronze.cliente` | 20 |
| `bronze.endereco` | 20 |
| `bronze.estado` | 15 |
| `bronze.marca` | 8 |
| `bronze.modelo` | 16 |
| `bronze.municipio` | 20 |
| `bronze.regiao` | 5 |
| `bronze.sinistro` | 80 |
| `bronze.telefone` | 20 |

## Por que Delta Lake?

- **ACID transactions** — garante consistência mesmo em falhas
- **Time Travel** — permite consultar versões anteriores dos dados
- **Schema Evolution** — suporte a mudanças de schema
- **Compaction & Optimization** — melhor performance de leitura
