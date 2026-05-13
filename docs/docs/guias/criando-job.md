# 📤 Upload de Arquivos para o Volume

## Passo a passo

Após executar o **Notebook 001** (que cria o Volume), siga estes passos:

### 1. Localizar o Volume no Catalog

1. Acesse **Catalog** no menu lateral
2. Expanda: `workspace → landing → Volumes → dados`
3. Clique no volume `dados`

### 2. Fazer o upload dos CSVs

1. Clique no botão **Upload to this volume** (canto superior direito)
2. Arraste ou selecione **todos os arquivos** da pasta `data/` do repositório:
   - `apolice.csv`
   - `carro.csv`
   - `cliente.csv`
   - `endereco.csv`
   - `estado.csv`
   - `marca.csv`
   - `modelo.csv`
   - `municipio.csv`
   - `regiao.csv`
   - `sinistro.csv`
   - `telefone.csv`
3. Clique em **Upload**

### 3. Confirmar o upload

Execute no Databricks:

```python
display(dbutils.fs.ls('/Volumes/workspace/landing/dados/'))
```

Você deve ver os 11 arquivos listados.

---

# ⚙️ Criando o JOB de Automação

O Job permite executar os 4 notebooks **sequencialmente de forma automática**.

## Passo a passo

### 1. Acessar Workflows

1. No menu lateral, clique em **Workflows**
2. Clique em **Create job**

### 2. Configurar o Job

- **Job name:** `pipeline_lakehouse_medaliao`

### 3. Adicionar as Tasks

**Task 1 — Preparar Ambiente:**
- Task name: `preparando_ambiente`
- Type: **Notebook**
- Source: Selecione o notebook `001_preparando_ambiente`
- Cluster: Selecione seu cluster

**Task 2 — Ingestão Bronze:**
- Task name: `ingestao_bronze`
- Type: **Notebook**
- Source: Selecione o notebook `002_bronze`
- Depends on: `preparando_ambiente`

**Task 3 — Data Quality Silver:**
- Task name: `data_quality_silver`
- Type: **Notebook**
- Source: Selecione o notebook `003_silver`
- Depends on: `ingestao_bronze`

**Task 4 — Modelagem Gold:**
- Task name: `modelagem_gold`
- Type: **Notebook**
- Source: Selecione o notebook `004_gold`
- Depends on: `data_quality_silver`

### 4. Visualizar o grafo do pipeline

Após adicionar as 4 tasks, o Databricks exibe o grafo:

```
preparando_ambiente → ingestao_bronze → data_quality_silver → modelagem_gold
```

### 5. Executar o pipeline

Clique em **Run Now** para executar o pipeline completo.

### 6. Monitorar a execução

- Cada task fica **verde** quando concluída com sucesso
- Clique em qualquer task para ver os logs de execução
- Se uma task falhar, as seguintes **não são executadas** (dependência)

!!! success "Pipeline concluído com sucesso!"
    Ao final, todas as 4 tasks estarão verdes e você terá:
    - 11 tabelas no schema **bronze**
    - 11 tabelas no schema **silver**
    - 5 tabelas no schema **gold** (4 dimensões + 1 fato)
