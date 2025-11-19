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


CREATE TRIGGER trg_produtos_update
ON produtos
AFTER UPDATE
AS
BEGIN
    UPDATE produtos 
    SET atualizado_em = GETDATE()
    WHERE id IN (SELECT id FROM inserted);
END;


CREATE TABLE imagens_produtos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    produto_id INT NOT NULL,
    url VARCHAR(500) NOT NULL,
    alt VARCHAR(500),
    principal BIT NOT NULL DEFAULT 0,
    criado_em DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);


CREATE TABLE categorias (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao VARCHAR(500),
    criado_em DATETIME NOT NULL DEFAULT GETDATE()
);


CREATE TABLE itens_carrinho (
    id INT IDENTITY(1,1) PRIMARY KEY,
    utilizador_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    adicionado_em DATETIME NOT NULL DEFAULT GETDATE(),
    UNIQUE (utilizador_id, produto_id),
    FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);