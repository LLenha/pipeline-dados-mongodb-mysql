import os

import requests
from dotenv import load_dotenv
from pymongo import MongoClient

PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PASTA_PROJETO, ".env"))

# Conectando ao MongoDB

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("Connected successfully")
except Exception as e:
    raise Exception("The following error occurred: ", e)

db = client["db_produtos"]
collection = db["produtos"]


# Extraindo dados de uma API

response = requests.get("https://labdados.com/produtos")
produtos = response.json()
print(f"Produtos recebidos da API: {len(produtos)}")


# Salvando no MongoDB (só insere se a coleção estiver vazia, para não duplicar)

if collection.count_documents({}) == 0:
    docs = collection.insert_many(produtos)
    print(f"Produtos inseridos: {len(docs.inserted_ids)}")
else:
    print(f"A coleção já tem {collection.count_documents({})} documentos. Nada foi inserido.")

client.close()
