-- criacao e definicao do escopo do banco de dados junto a criacao do usuario
CREATE DATABASE desafio_bi;
CREATE USER daniel WITH ENCRYPTED PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE desafio_bi TO daniel;

-- criacao da tabela de clentes 
CREATE TABLE clientes (
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    region VARCHAR(50),
    signup_date DATE
);
-- criacao da tabela de produtos
CREATE TABLE produtos (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(50),
    price DECIMAL(10,2)
);
-- criacao da tabela de relacionamento de transacoes
CREATE TABLE transacoes (
    transaction_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clientes(client_id),
    product_id INT REFERENCES produtos(product_id),
    amount INT,
    transaction_date DATE,
    total_value DECIMAL(10,2),
    id_menos_um INT,
    price DECIMAL(10,2)
);

