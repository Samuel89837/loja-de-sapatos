CREATE TABLE utilizadores (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);


CREATE TABLE produtos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao VARCHAR(500),
    preco_cents INT NOT NULL CHECK (preco_cents >= 0),
    moeda VARCHAR(10) NOT NULL DEFAULT 'EUR',
    ativo BIT NOT NULL DEFAULT 1,
    stock INT NOT NULL DEFAULT 0,
    categoria_id INT NULL,
    criado_em DATETIME NOT NULL DEFAULT GETDATE(),
    atualizado_em DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);