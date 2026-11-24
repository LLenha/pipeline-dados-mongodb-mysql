# Pipeline de dados com Python, MongoDB e MySQL

Pipeline ETL que extrai dados de vendas de uma API, armazena os dados brutos no **MongoDB Atlas**, faz a limpeza e a transformação com **pandas** e carrega o resultado em tabelas do **MySQL**.

```
API (labdados.com/produtos)
        │  extrair_e_salvar.py
        ▼
MongoDB Atlas (db_produtos.produtos) ── dados brutos, 9.435 registros
        │  transform_data.py
        ▼
CSVs tratados em data/
        │  conexao_mysql.py
        ▼
MySQL (dbprodutos) ── tb_livros, tb_produtos_2021_em_diante
```

## Etapas

### 1. Extração: `scripts/extrair_e_salvar.py`
- Consome a API `https://labdados.com/produtos` com `requests`.
- Insere os 9.435 registros na coleção `produtos` do MongoDB Atlas.
- Só insere se a coleção estiver vazia, então rodar de novo não duplica os dados.

### 2. Transformação: `scripts/transform_data.py`
- Renomeia os campos `lat`/`lon` para `latitude`/`longitude` no MongoDB.
- Seleciona dois recortes:
  - **Livros:** produtos da categoria `livros` (742 registros).
  - **2021 em diante:** vendas a partir de 2021, filtradas com regex na data (6.574 registros).
- Converte as datas de `dd/mm/aaaa` para `aaaa-mm-dd`, o formato aceito pelo tipo `DATE` do MySQL.
- Salva os recortes em `data/tabela_livros.csv` e `data/tb_2021_em_diante.csv`.

### 3. Carga: `scripts/conexao_mysql.py`
- Cria o banco `dbprodutos` e as tabelas com tipos definidos (`DATE`, `FLOAT`, `INT`) e chave primária.
- Insere os CSVs tratados com `executemany`.
- Só insere se a tabela estiver vazia, o que evita erro de chave duplicada.

## Tecnologias
- Python 3.12
- MongoDB Atlas (`pymongo`)
- MySQL 8.4 (`mysql-connector-python`)
- pandas
- requests
- python-dotenv, para guardar as credenciais fora do código

## Estrutura

```
.
├── data/
│   ├── tabela_livros.csv
│   └── tb_2021_em_diante.csv
├── scripts/
│   ├── extrair_e_salvar.py
│   ├── transform_data.py
│   └── conexao_mysql.py
├── .env.example
├── requirements.txt
└── README.md
```

## Como executar

1. Clone o repositório e crie o ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Linux/macOS
   pip install -r requirements.txt
   ```
2. Copie o `.env.example` para `.env` e preencha com as credenciais do MongoDB Atlas e do MySQL.
3. Rode as etapas em ordem:
   ```bash
   python scripts/extrair_e_salvar.py
   python scripts/transform_data.py
   python scripts/conexao_mysql.py
   ```

Pré-requisitos: um cluster no MongoDB Atlas (o plano gratuito serve) e um servidor MySQL rodando localmente.
