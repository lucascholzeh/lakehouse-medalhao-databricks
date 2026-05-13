# 📓 Notebook 001 — Preparando o Ambiente

**Arquivo:** `notebooks/001_preparando_ambiente.py`

## Objetivo

Criar toda a estrutura de schemas e volumes necessária no Unity Catalog antes de iniciar o pipeline.

## O que este notebook faz?

1. Exibe o catálogo e database ativos
2. Cria o schema `landing` com o Volume `dados` para upload de CSVs
3. Cria os schemas `bronze`, `silver` e `gold`
4. Verifica os schemas e o volume criados
5. Lista os arquivos presentes no volume

## Código principal

```sql
-- Criação dos schemas
CREATE SCHEMA IF NOT EXISTS workspace.landing
  COMMENT 'Schema para a zona de pouso — arquivos CSV brutos da origem';

CREATE VOLUME IF NOT EXISTS workspace.landing.dados
  COMMENT 'Volume para upload dos arquivos CSV do sistema de seguro de veículos';

CREATE SCHEMA IF NOT EXISTS workspace.bronze
  COMMENT 'Camada Bronze — dados brutos ingeridos em Delta Lake';

CREATE SCHEMA IF NOT EXISTS workspace.silver
  COMMENT 'Camada Silver — dados tratados com regras de qualidade';

CREATE SCHEMA IF NOT EXISTS workspace.gold
  COMMENT 'Camada Gold — modelo dimensional para análise e BI';
```

## Resultado esperado

| Schema | Tipo | Status |
|--------|------|--------|
| `workspace.landing` | Schema | ✅ Criado |
| `workspace.landing.dados` | Volume | ✅ Criado |
| `workspace.bronze` | Schema | ✅ Criado |
| `workspace.silver` | Schema | ✅ Criado |
| `workspace.gold` | Schema | ✅ Criado |

!!! warning "Atenção"
    Se aparecer o erro `SCHEMA_NOT_FOUND: workspace.workspace`, seu catálogo padrão está incorreto. Execute `SELECT current_catalog()` para ver qual catálogo está ativo e ajuste os nomes no notebook.
