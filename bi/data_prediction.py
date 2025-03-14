import pandas as pd
import psycopg2
from prophet import Prophet
import matplotlib.pyplot as plt

# Conectar ao PostgreSQL
conn = psycopg2.connect(
    dbname="desafio_bi",
    user="daniel",
    password="12345",
    host="localhost",
    port="5432"
)

# Carregar os dados de transações
query = """
    SELECT transaction_date, SUM(total_value) as revenue
    FROM desafio.transacoes
    GROUP BY transaction_date
    ORDER BY transaction_date;
"""

sales_data = pd.read_sql(query, conn)
conn.close()

# Renomear colunas para Prophet
sales_data.columns = ["ds", "y"]

# Criar e treinar o modelo Prophet
model = Prophet()
model.fit(sales_data)

# Criar previsões para os próximos 30 dias
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Plotar previsão
fig = model.plot(forecast)
plt.title("Previsão de Receita para os Próximos 30 Dias")
plt.show()
