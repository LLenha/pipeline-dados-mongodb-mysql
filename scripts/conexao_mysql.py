import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DATA = os.path.join(PASTA_PROJETO, "data")

load_dotenv(os.path.join(PASTA_PROJETO, ".env"))

COLUNAS_TABELA = """
    id VARCHAR(100),
    Produto VARCHAR(100),
    Categoria_Produto VARCHAR(100),
    Preco FLOAT(10,2),
    Frete FLOAT(10,2),
    Data_Compra DATE,
    Vendedor VARCHAR(100),
    Local_Compra VARCHAR(100),
    Avaliacao_Compra INT,
    Tipo_Pagamento VARCHAR(100),
    Qntd_Parcelas INT,
    Latitude FLOAT(10,2),
    Longitude FLOAT(10,2),

    PRIMARY KEY (id)
"""


def connect_mysql():
    cnx = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    )
    print("Conectado ao MySQL")
    return cnx


def create_cursor(cnx):
    return cnx.cursor(buffered=True)


def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    print(f"Banco de dados '{db_name}' pronto")


def show_databases(cursor):
    cursor.execute("SHOW DATABASES;")
    for db in cursor:
        print(db)


def create_product_table(cursor, db_name, tb_name):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {db_name}.{tb_name}({COLUNAS_TABELA});")
    print(f"Tabela '{tb_name}' pronta")


def show_tables(cursor, db_name):
    cursor.execute(f"USE {db_name};")
    cursor.execute("SHOW TABLES;")
    for tb in cursor:
        print(tb)


def read_csv(path):
    return pd.read_csv(path)


def add_product_data(cnx, cursor, df, db_name, tb_name):
    # Só insere se a tabela estiver vazia, para não dar erro de chave duplicada
    cursor.execute(f"SELECT COUNT(*) FROM {db_name}.{tb_name};")
    total = cursor.fetchone()[0]
    if total > 0:
        print(f"A tabela '{tb_name}' já tem {total} linhas. Nada foi inserido.")
        return

    lista_dados = [tuple(row) for _, row in df.iterrows()]
    sql = f"INSERT INTO {db_name}.{tb_name} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.executemany(sql, lista_dados)
    cnx.commit()
    print(f"{cursor.rowcount} dados foram inseridos na tabela '{tb_name}'.")


if __name__ == "__main__":
    cnx = connect_mysql()
    cursor = create_cursor(cnx)

    create_database(cursor, "dbprodutos")
    show_databases(cursor)

    # Livros
    df_livros = read_csv(os.path.join(PASTA_DATA, "tabela_livros.csv"))
    create_product_table(cursor, "dbprodutos", "tb_livros")
    add_product_data(cnx, cursor, df_livros, "dbprodutos", "tb_livros")

    # Produtos de 2021 em diante
    df_produtos = read_csv(os.path.join(PASTA_DATA, "tb_2021_em_diante.csv"))
    create_product_table(cursor, "dbprodutos", "tb_produtos_2021_em_diante")
    add_product_data(cnx, cursor, df_produtos, "dbprodutos", "tb_produtos_2021_em_diante")

    show_tables(cursor, "dbprodutos")

    cursor.close()
    cnx.close()
