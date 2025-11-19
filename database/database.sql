CREATE TABLE utilizadores (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);