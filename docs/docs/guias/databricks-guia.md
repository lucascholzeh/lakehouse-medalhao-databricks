# 📘 Como usar o Databricks Community Edition

## 1. Criar sua conta (gratuita)

1. Acesse [community.cloud.databricks.com](https://community.cloud.databricks.com)
2. Clique em **Sign Up** → **Get started with Community Edition**
3. Preencha e-mail, senha e informações básicas
4. Confirme o e-mail e faça login

!!! warning "Importante"
    O Databricks Community Edition tem um cluster que é **encerrado automaticamente após 2 horas de inatividade**. Sempre inicie o cluster antes de executar os notebooks.

---

## 2. Criar o Cluster

1. No menu lateral, clique em **Compute**
2. Clique em **Create compute**
3. Preencha:
   - **Cluster name:** `lakehouse-cluster`
   - **Databricks Runtime:** `13.3 LTS` ou superior
   - Deixe o resto no padrão
4. Clique em **Create compute**
5. Aguarde o status ficar **Running** (verde)

---

## 3. Importar os Notebooks

### Opção A — Via arquivo .py (upload direto)

1. No menu lateral, clique em **Workspace**
2. Navegue até sua pasta pessoal (ícone da casinha)
3. Clique no botão **⋮** → **Import**
4. Selecione **File** e faça upload do arquivo `.py`
5. Repita para cada notebook

### Opção B — Via Git Repos (recomendado)

1. No menu lateral, clique em **Repos**
2. Clique em **Add repo**
3. Cole a URL do seu repositório GitHub
4. Clique em **Create Repo**
5. Os notebooks aparecem automaticamente na estrutura de pastas

---

## 4. Vincular o Notebook ao Cluster

1. Abra qualquer notebook
2. No topo, clique no dropdown de cluster (mostra "Detached")
3. Selecione seu cluster `lakehouse-cluster`
4. Aguarde conectar (o ícone fica verde)

---

## 5. Executar células

| Ação | Atalho |
|------|--------|
| Executar célula atual | `Shift + Enter` |
| Executar célula e criar nova abaixo | `Ctrl + Enter` |
| Executar todas as células | Clique em **Run All** no topo |
| Parar execução | Clique em **Interrupt** |

---

## 6. Ver as tabelas no Catalog

1. No menu lateral, clique em **Catalog**
2. Expanda: `workspace → bronze → Tables`
3. Clique em uma tabela para ver o schema, amostras de dados e detalhes Delta

!!! tip "Visualização rápida"
    Para ver os dados de uma tabela sem abrir notebook, clique na tabela no Catalog e vá na aba **Sample Data**.

---

## 7. Solução de erros comuns

### ❌ `SCHEMA_NOT_FOUND: workspace.workspace`
**Causa:** O catálogo padrão está incorreto.  
**Solução:** Adicione `USE CATALOG workspace;` no início do notebook, ou substitua `workspace.landing` pelo nome correto do seu catálogo.

### ❌ `Path does not exist: /Volumes/workspace/landing/dados/`
**Causa:** Os CSVs ainda não foram enviados para o Volume.  
**Solução:** Siga o [Guia de Upload de Arquivos](upload-arquivos.md).

### ❌ `Cluster terminated`
**Causa:** O cluster ficou inativo e foi desligado automaticamente.  
**Solução:** Vá em **Compute**, clique no cluster e em **Start**.
