import sqlalchemy
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Conectar ao PostgreSQL e carregar os dados dos clientes e transações
conn = psycopg2.connect(
    dbname="desafio_bi",
    user="daniel",
    password="12345",
    host="localhost",
    port="5432"
)

query = """
    SELECT c.client_id, c.region, 
           COUNT(t.transaction_id) AS frequency,
           SUM(t.total_value) AS total_spent,
           SUM(t.total_value) / COUNT(t.transaction_id) AS avg_ticket,
           (CURRENT_DATE - MAX(t.transaction_date)) AS recency
    FROM desafio.clientes c
    JOIN desafio.transacoes t ON c.client_id = t.client_id
    GROUP BY c.client_id, c.region;
"""

clients_data = pd.read_sql(query, conn)
conn.close()

# Normalizar os dados para o K-Means (removendo a coluna de região temporariamente)
features = clients_data.drop(columns=["client_id", "region"])
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Aplicar o K-Means com 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clients_data["cluster"] = kmeans.fit_predict(scaled_features)

# Criar um scatter plot para visualizar os clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=clients_data["frequency"],
    y=clients_data["total_spent"],
    hue=clients_data["cluster"],
    palette="viridis",
    alpha=0.7
)
plt.title("Segmentação de Clientes - Clusters")
plt.xlabel("Frequência de Compras")
plt.ylabel("Total Gasto")
plt.legend(title="Cluster")
plt.show()
