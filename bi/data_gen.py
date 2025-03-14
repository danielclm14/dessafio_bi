import pandas as pd
import numpy as np

# Definir quantidades de registros
num_clients = 500
num_products = 50
num_transactions = 5000

# Gerar dados de clientes
clients = pd.DataFrame({
    "client_id": range(1, num_clients + 1),
    "name": [f"Cliente {i}" for i in range(1, num_clients + 1)],
    "region": np.random.choice(["Norte", "Sul", "Leste", "Oeste"], num_clients),
    "signup_date": pd.to_datetime(np.random.choice(pd.date_range("2020-01-01", "2023-12-31"), num_clients)),
})

# Gerar dados de produtos
products = pd.DataFrame({
    "product_id": range(1, num_products + 1),
    "product_name": [f"Produto {i}" for i in range(1, num_products + 1)],
    "category": np.random.choice(["Investimento", "Crédito", "Seguros", "Conta Corrente"], num_products),
    "price": np.random.uniform(50, 5000, num_products).round(2),
})

# Gerar dados de transações
transactions = pd.DataFrame({
    "transaction_id": range(1, num_transactions + 1),
    "client_id": np.random.choice(clients["client_id"], num_transactions),
    "product_id": np.random.choice(products["product_id"], num_transactions),
    "amount": np.random.randint(1, 10, num_transactions),
    "transaction_date": pd.to_datetime(np.random.choice(pd.date_range("2022-01-01", "2024-02-01"), num_transactions)),
})

# Adicionar valor total da transação
transactions = transactions.merge(products[["product_id", "price"]], on="product_id", how="left")
transactions["total_value"] = (transactions["amount"] * transactions["price"]).round(2)

# Exibir os dados
import ace_tools as tools
tools.display_dataframe_to_user(name="Dados de Clientes", dataframe=clients)
tools.display_dataframe_to_user(name="Dados de Produtos", dataframe=products)
tools.display_dataframe_to_user(name="Dados de Transações", dataframe=transactions)
