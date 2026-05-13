# 🏆 Lakehouse com Databricks — Arquitetura Medalhão

Bem-vindo à documentação do projeto de **Engenharia de Dados** desenvolvido como atividade prática do curso de Engenharia de Software.

---

## O que é este projeto?

Este projeto implementa um **Lakehouse** completo utilizando a plataforma **Databricks Community Edition** com **Delta Lake**, seguindo a **Arquitetura Medalhão** — um padrão moderno de engenharia de dados que organiza os dados em camadas progressivas de qualidade e transformação.

O domínio de negócio escolhido é um sistema de **Seguro de Veículos**, com dados de apólices, sinistros, clientes, veículos e localidades.

---

## Fluxo do Pipeline

```mermaid
flowchart LR
    A[("📁 CSVs\nOrigem")] -->|Upload| B
    
    subgraph B["🟫 LANDING"]
        direction TB
        B1["Volume\nDados Brutos"]
    end
    
    B -->|Notebook 002| C
    
    subgraph C["🥉 BRONZE"]
        direction TB
        C1["Delta Lake\nDados Raw\n+ Metadados"]
    end
    
    C -->|Notebook 003| D
    
    subgraph D["🥈 SILVER"]
        direction TB
        D1["Delta Lake\nData Quality\nPadronizado"]
    end
    
    D -->|Notebook 004| E
    
    subgraph E["🥇 GOLD"]
        direction TB
        E1["Star Schema\nKimball\nBI Ready"]
    end
    
    style B fill:#8B4513,color:#fff
    style C fill:#cd7f32,color:#fff
    style D fill:#C0C0C0,color:#000
    style E fill:#FFD700,color:#000
```

---

## Tecnologias

| Tecnologia | Papel no Projeto |
|-----------|-----------------|
| **Databricks Community** | Plataforma de execução e orquestração |
| **Apache Spark / PySpark** | Engine de processamento distribuído |
| **Delta Lake** | Formato de armazenamento ACID |
| **Unity Catalog** | Governança e catálogo de dados |
| **SQL** | Transformações e modelagem |

---

## Navegação

Use o menu superior para acessar:

- **🏗️ Arquitetura** — Entenda o modelo de dados e as camadas
- **📓 Notebooks** — Código e explicação de cada etapa
- **📋 Guias** — Como configurar e usar o Databricks

---

!!! tip "Primeira vez aqui?"
    Comece pelo guia [Como usar o Databricks](guias/databricks-guia.md) e depois siga a ordem dos notebooks.
