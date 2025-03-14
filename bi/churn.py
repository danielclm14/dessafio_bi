import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

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

# Definir churn (1 se não compra há mais de 180 dias, 0 caso contrário)
clients_data["churn"] = (clients_data["recency"] > 450).astype(int) 


# Selecionar variáveis para o modelo
X = clients_data[["frequency", "total_spent", "avg_ticket", "recency"]]
y = clients_data["churn"]

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo Random Forest para prever churn
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)

# Exibir métricas do modelo
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred))

# Exibir matriz de confusão
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print("Matriz de Confusão:")
print(f"Verdadeiros Negativos: {tn}")
print(f"Falsos Positivos: {fp}")
print(f"Falsos Negativos: {fn}")
print(f"Verdadeiros Positivos: {tp}")

# Plotar a matriz de confusão
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues", xticklabels=["Não Churn", "Churn"], yticklabels=["Não Churn", "Churn"])
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.title("Matriz de Confusão - Previsão de Churn")
plt.show()
