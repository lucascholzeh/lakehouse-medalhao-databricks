# 📓 Notebook 004 — Camada Gold (Modelagem Dimensional)

**Arquivo:** `notebooks/004_gold.py`

## Objetivo

Criar o **Star Schema** seguindo a metodologia **Ralph Kimball**, populando dimensões e tabela fato a partir dos dados Silver.

## Tabelas criadas

| Tabela | Tipo | Linhas Esperadas |
|--------|------|-----------------|
| `gold.dim_carro` | Dimensão | 40 |
| `gold.dim_tempo` | Dimensão | ~1.461 (2023–2026) |
| `gold.dim_cliente` | Dimensão | 20 |
| `gold.dim_localidade` | Dimensão | 20 |
| `gold.fato_sinistro` | Fato | ~80 (agrupado) |

## Estratégia MERGE (SCD Type 1)

Todas as dimensões são carregadas com `MERGE INTO`:

```sql
MERGE INTO gold.dim_cliente AS d
USING cliente_relacional    AS r
ON r.CODIGO_CLIENTE = d.CODIGO_CLIENTE

WHEN MATCHED AND (r.nome <> d.nome OR ...) THEN
  UPDATE SET ...

WHEN NOT MATCHED THEN
  INSERT (CODIGO_CLIENTE, NOME, ...)
  VALUES (r.CODIGO_CLIENTE, r.NOME, ...)
```

## Queries analíticas incluídas

- Top 10 localidades com mais sinistros
- Sinistros por ano e mês
