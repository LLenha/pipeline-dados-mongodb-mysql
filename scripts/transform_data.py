import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DATA = os.path.join(PASTA_PROJETO, "data")

load_dotenv(os.path.join(PASTA_PROJETO, ".env"))
URI = os.getenv("MONGODB_URI")


def connect_mongo(uri):
    client = MongoClient(uri)
    try:
        client.admin.command("ping")
        print("Connected successfully")
    except Exception as e:
        raise Exception("The following error occurred: ", e)
    return client


def create_connect_db(client, db_name):
    return client[db_name]


def create_connect_collection(db, col_name):
    return db[col_name]


def rename_column(col, col_name, new_name):
    # Se o campo já foi renomeado, o $rename não faz nada
    col.update_many({}, {"$rename": {col_name: new_name}})


def select_category(col, category):
    query = {"Categoria do Produto": category}
    return list(col.find(query))


def make_regex(col, regex):
    query = {"Data da Compra": {"$regex": regex}}
    return list(col.find(query))


def create_dataframe(lista):
    return pd.DataFrame(lista)


def format_date(df):
    # "01/01/2020" -> "2020-01-01"
    df["Data da Compra"] = pd.to_datetime(df["Data da Compra"], format="%d/%m/%Y")
    df["Data da Compra"] = df["Data da Compra"].dt.strftime("%Y-%m-%d")


def save_csv(df, path):
    df.to_csv(path, index=False)
    print(f"Arquivo salvo: {path} ({len(df)} linhas)")


if __name__ == "__main__":
    client = connect_mongo(URI)
    db = create_connect_db(client, "db_produtos")
    col = create_connect_collection(db, "produtos")

    rename_column(col, "lat", "latitude")
    rename_column(col, "lon", "longitude")

    os.makedirs(PASTA_DATA, exist_ok=True)

    # Tabela só com os livros
    df_livros = create_dataframe(select_category(col, "livros"))
    format_date(df_livros)
    save_csv(df_livros, os.path.join(PASTA_DATA, "tabela_livros.csv"))

    # Tabela com as compras de 2021 em diante
    df_2021 = create_dataframe(make_regex(col, "/202[1-9]"))
    format_date(df_2021)
    save_csv(df_2021, os.path.join(PASTA_DATA, "tb_2021_em_diante.csv"))

    client.close()
