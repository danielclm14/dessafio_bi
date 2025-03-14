import psycopg2
import pandas as pd

# Conexão com o banco de dados
conn = psycopg2.connect(
    dbname="desafio_bi",
    user="daniel",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Função para inserir dados
from psycopg2.extras import execute_values

def insert_data(query, data):
    execute_values(cursor, query, data)
    conn.commit()


# Carregar os DataFrames do Pandas (simulando a leitura dos dados gerados)
clients = pd.read_csv("clientes.csv")
products = pd.read_csv("produtos.csv")
transactions = pd.read_csv("transacoes.csv")

# Inserir clientes
insert_clients = """
    INSERT INTO desafio.clientes (name, region, signup_date)
    VALUES %s
"""

insert_data(insert_clients, [tuple(row[1:]) for row in clients.values])


# Inserir produtos
insert_products = """
    INSERT INTO desafio.produtos (product_id, product_name, category, price)
    VALUES %s
"""
insert_data(insert_products, [tuple(row) for row in products.values])

# Inserir transações
insert_transactions = """
    INSERT INTO desafio.transacoes (id_menos_um,client_id, product_id, amount, transaction_date, price, total_value)
    VALUES %s
"""
insert_data(insert_transactions, [tuple(row[1:]) for row in transactions.values])

# Fechar conexão
cursor.close()
conn.close()

print("Dados inseridos com sucesso!")
