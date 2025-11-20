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


CREATE TABLE encomendas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    utilizador_id INT NULL,
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('pendente', 'pago', 'enviado')),
    total_cents INT NOT NULL,
    moeda VARCHAR(10) NOT NULL DEFAULT 'EUR',
    nome_envio VARCHAR(255),
    morada_envio VARCHAR(255),
    telefone_contacto VARCHAR(50),
    criado_em DATETIME NOT NULL DEFAULT GETDATE(),
    atualizado_em DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id)
);


CREATE TRIGGER trg_encomendas_update
ON encomendas
AFTER UPDATE
AS
BEGIN
    UPDATE encomendas 
    SET atualizado_em = GETDATE()
    WHERE id IN (SELECT id FROM inserted);
END;



CREATE TABLE itens_encomenda (
    id INT IDENTITY(1,1) PRIMARY KEY,
    encomenda_id INT NOT NULL,
    produto_id INT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unit_cents INT NOT NULL,
    FOREIGN KEY (encomenda_id) REFERENCES encomendas(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE SET NULL
);



CREATE TABLE notificacoes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    utilizador_id INT,
    tipo VARCHAR(100) NOT NULL,
    conteudo VARCHAR(2000),
    lida BIT NOT NULL DEFAULT 0,
    criado_em DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id) ON DELETE CASCADE
);



CREATE TABLE historico_produtos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    produto_id INT NULL,
    acao VARCHAR(100) NOT NULL,
    alterado_por INT NULL,
    valores_antigos VARCHAR(2000),
    valores_novos VARCHAR(2000),
    criado_em DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE SET NULL,
    FOREIGN KEY (alterado_por) REFERENCES utilizadores(id) ON DELETE SET NULL
);


CREATE TABLE configuracoes (
    chave VARCHAR(255) PRIMARY KEY,
    valor VARCHAR(2000)
);


INSERT INTO utilizadores (nome, email, password) 
VALUES 
('Daniel Gatinhos', 'danielmiau@gmail.com', 'miau1234'),
('Maria Alberta', 'maria@gmail.com', 'maria123');


INSERT INTO categorias (nome, descricao) 
VALUES
('Sapatos Homem', 'Calçado masculino'),
('Sapatos Mulher', 'Calçado feminino');


NSERT INTO produtos (titulo, descricao, preco_cents, categoria_id, stock) 
VALUES
('Sapatilha Nike Air', 'Modelo desportivo confortável', 4999, 1, 10),
('Sandália Elegante', 'Sandália feminina para verão', 2999, 2, 15);


INSERT INTO imagens_produtos (produto_id, url, alt, principal)
VALUES
(1, 'https://www.nike.com/pt/t/sapatilhas-air-force-1-07-E5NnNyBr/CW2288-111', 'Nike Air Vista Lateral', 1),
(2, 'https://www.jdsports.pt/product/castanho-birkenstock-sandlias-arizona-eva-mulher/771573_jdsportspt/', 'Sandália elegante dourada', 1);



INSERT INTO itens_carrinho (utilizador_id, produto_id, quantidade)
VALUES
(1, 1, 1),
(1, 2, 2);



INSERT INTO encomendas (utilizador_id, estado, total_cents, nome_envio, morada_envio, telefone_contacto)
VALUES
(1, 'pendente', 7998, 'Daniel Gatinhos', 'Rua das Flores 12', '912345678'),
(1, 'pago', 2999, 'Daniel Gatinhos', 'Rua das Flores 12', '912345678');


INSERT INTO itens_encomenda (encomenda_id, produto_id, quantidade, preco_unit_cents)
VALUES
(1, 1, 1, 4999),
(1, 2, 1, 2999);


INSERT INTO notificacoes (utilizador_id, tipo, conteudo)
VALUES
(1, 'Encomenda', 'A sua encomenda #1 foi recebida.'),
(1, 'Promoção', 'Novo desconto disponível em sapatos! 20% OFF.');


INSERT INTO historico_produtos (produto_id, acao, alterado_por, valores_antigos, valores_novos)
VALUES
(1, 'Atualização de preço', 2, 'preco = 3999', 'preco = 4999'),
(2, 'Alteração de stock', 2, 'stock = 10', 'stock = 15');


INSERT INTO configuracoes (chave, valor)
VALUES
('site_manutencao', 'false'),
('itens_por_pagina', '12');