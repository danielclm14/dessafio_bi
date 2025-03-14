# Importar bibliotecas
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Conectar ao PostgreSQL e carregar os dados dos clientes e transações
conn = psycopg2.connect(
    dbname="desafio_bi",
    user="daniel",
    password="12345",
    host="localhost",
    port="5432"
)

query = """
    SELECT c.client_id, 
           COUNT(t.transaction_id) AS frequency,
           SUM(t.total_value) AS total_spent,
           SUM(t.total_value) / COUNT(t.transaction_id) AS avg_ticket,
           (CURRENT_DATE - MAX(t.transaction_date)) AS recency
    FROM desafio.clientes c
    JOIN desafio.transacoes t ON c.client_id = t.client_id
    GROUP BY c.client_id;
"""

import sqlalchemy

engine = sqlalchemy.create_engine("postgresql://daniel:12345@localhost:5432/desafio_bi")
clients_data = pd.read_sql(query, engine)
conn.close()

# Definir churn (1 se não compra há mais de 420 dias, 0 caso contrário)
clients_data["churn"] = (clients_data["recency"] > 420).astype(int)

# Selecionar variáveis para o modelo
X = clients_data[["frequency", "total_spent", "avg_ticket", "recency"]]
y = clients_data["churn"]

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo Random Forest para prever churn
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Obter a importância das variáveis no modelo
feature_importances = model.feature_importances_
feature_names = X.columns

# Criar um DataFrame para visualização
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Plotar a importância das variáveis
plt.figure(figsize=(8, 5))
sns.barplot(x=importance_df['Importance'], y=importance_df['Feature'], palette='viridis')
plt.title('Importância das Variáveis na Previsão de Churn')
plt.xlabel('Importância')
plt.ylabel('Variável')
plt.show()
