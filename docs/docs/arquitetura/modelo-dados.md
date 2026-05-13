# 🗃️ Modelo de Dados

## Modelo Relacional (origem — Landing/Bronze/Silver)

O domínio de negócio é um sistema de **Seguro de Veículos** com as seguintes entidades:

```
regiao (5)
  └── estado (15)
        └── municipio (20)
              └── endereco (20)
                    └── cliente (20) ←── apolice (40) ←── sinistro (80)
                                              │
                      modelo (16) ──< carro (40) ───────┘
                      marca (8) ─┘

cliente (20) ──< telefone (20)
```

## Dicionário de Dados

### `regiao`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `cd_regiao` | INT (PK) | Código da região |
| `nm_regiao` | VARCHAR | Nome da região geográfica |

### `estado`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `cd_estado` | INT (PK) | Código do estado |
| `nm_estado` | VARCHAR | Nome do estado |
| `uf` | CHAR(2) | Sigla do estado |
| `cd_regiao` | INT (FK) | Referência à região |

### `municipio`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `cd_municipio` | INT (PK) | Código do município |
| `nm_municipio` | VARCHAR | Nome do município |
| `cd_estado` | INT (FK) | Referência ao estado |

### `cliente`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `cd_cliente` | INT (PK) | Código do cliente |
| `nm_cliente` | VARCHAR | Nome completo |
| `cpf` | VARCHAR(11) | CPF (somente dígitos) |
| `sexo` | CHAR(1) | M / F |
| `dt_nascimento` | DATE | Data de nascimento |

### `carro`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `placa` | VARCHAR(7) (PK) | Placa do veículo |
| `cd_modelo` | INT (FK) | Referência ao modelo |
| `cor` | VARCHAR | Cor do veículo |
| `ano` | INT | Ano de fabricação |
| `chassi` | VARCHAR | Número do chassi |

### `apolice`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `cd_apolice` | INT (PK) | Código da apólice |
| `cd_cliente` | INT (FK) | Cliente segurado |
| `placa` | VARCHAR (FK) | Veículo segurado |
| `dt_inicio` | DATE | Início da vigência |
| `dt_fim` | DATE | Fim da vigência |
| `vl_premio` | DECIMAL | Valor do prêmio anual |

### `sinistro`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `cd_sinistro` | INT (PK) | Código do sinistro |
| `placa` | VARCHAR (FK) | Veículo envolvido |
| `dt_sinistro` | DATE | Data do evento |
| `cd_local_sinistro` | INT (FK) | Município onde ocorreu |
| `vl_prejuizo` | DECIMAL | Valor do prejuízo |
| `ds_tipo` | VARCHAR | Tipo: COLISAO, ROUBO, etc. |

---

## Star Schema — Gold (Ralph Kimball)

### `gold.dim_carro`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `SK_CARRO` | BIGINT (IDENTITY) | Surrogate Key |
| `PLACA` | VARCHAR | Natural Key |
| `MARCA` | VARCHAR | Nome da marca |
| `MODELO` | VARCHAR | Nome do modelo |
| `COR` | VARCHAR | Cor do veículo |
| `ANO` | INT | Ano de fabricação |
| `CHASSI` | VARCHAR | Número do chassi |

### `gold.dim_tempo`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `DATA` | DATE (NK) | Data completa |
| `ANO` | INT | Ano |
| `MES` | INT | Número do mês |
| `NOME_MES` | VARCHAR | Nome do mês em PT |
| `DIA` | INT | Dia do mês |
| `NOME_DIA_SEMANA` | VARCHAR | Nome do dia |
| `NUMERO_DIA_SEMANA` | INT | 1=Dom … 7=Sáb |
| `TRIMESTRE` | INT | Trimestre (1–4) |

### `gold.dim_cliente`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `SK_CLIENTE` | BIGINT (IDENTITY) | Surrogate Key |
| `CODIGO_CLIENTE` | INT | Natural Key |
| `NOME` | VARCHAR | Nome do cliente |
| `CPF` | VARCHAR | CPF do cliente |
| `SEXO` | CHAR(1) | M / F |
| `DATA_NASCIMENTO` | DATE | Data de nascimento |

### `gold.dim_localidade`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `SK_LOCALIDADE` | BIGINT (IDENTITY) | Surrogate Key |
| `CODIGO_MUNICIPIO` | INT | Natural Key |
| `NOME_MUNICIPIO` | VARCHAR | Nome do município |
| `SIGLA_ESTADO` | VARCHAR(2) | UF |
| `NOME_ESTADO` | VARCHAR | Nome do estado |
| `NOME_REGIAO` | VARCHAR | Nome da região |

### `gold.fato_sinistro`
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `FK_TEMPO` | DATE | → `dim_tempo.DATA` |
| `FK_LOCALIDADE` | BIGINT | → `dim_localidade.SK_LOCALIDADE` |
| `FK_CARRO` | BIGINT | → `dim_carro.SK_CARRO` |
| `FK_CLIENTE` | BIGINT | → `dim_cliente.SK_CLIENTE` |
| `QTDE_SINISTRO` | INT | **Métrica:** quantidade |
| `VALOR_PREJUIZO` | DECIMAL(15,2) | **Métrica:** valor total |
