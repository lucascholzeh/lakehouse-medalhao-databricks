# 📓 Notebook 003 — Camada Silver (Data Quality)

**Arquivo:** `notebooks/003_silver.py`

## Objetivo

Aplicar regras de **Data Quality** nos dados Bronze e persistir na camada Silver com nomenclatura padronizada.

## Regras aplicadas

| # | Regra | Implementação |
|---|-------|--------------|
| 1 | Remover duplicatas | `df.dropDuplicates()` |
| 2 | Filtrar PKs nulas | `df.filter(col(pk).isNotNull())` |
| 3 | Padronizar nomes de colunas | Expansão de prefixos abreviados |
| 4 | Maiúsculo em todos os nomes | `colname.upper()` |
| 5 | Remover colunas Bronze | Drop de `data_hora_bronze`, `nome_arquivo` |
| 6 | Adicionar metadados Silver | `NOME_TABELA_BRONZE`, `DATA_HORA_SILVER` |

## Exemplo de transformação de colunas

| Antes (Bronze) | Depois (Silver) |
|---------------|----------------|
| `cd_cliente` | `CODIGO_CLIENTE` |
| `nm_cliente` | `NOME_CLIENTE` |
| `dt_nascimento` | `DATA_NASCIMENTO` |
| `vl_premio` | `VALOR_PREMIO` |
| `uf` | `SIGLA_ESTADO` |
