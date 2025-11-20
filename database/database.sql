PRAGMA foreign_keys = ON;

CREATE TABLE utilizadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    password TEXT
);

CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    preco_cents INTEGER NOT NULL CHECK (preco_cents >= 0),
    moeda TEXT NOT NULL DEFAULT 'EUR',
    ativo INTEGER NOT NULL DEFAULT 1,
    stock INTEGER NOT NULL DEFAULT 0,
    categoria_id INTEGER,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TRIGGER trg_produtos_update
AFTER UPDATE ON produtos
BEGIN
    UPDATE produtos
    SET atualizado_em = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TABLE imagens_produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    alt TEXT,
    principal INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

CREATE TABLE itens_carrinho (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilizador_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    adicionado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (utilizador_id, produto_id),
    FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
);

CREATE TABLE encomendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilizador_id INTEGER,
    estado TEXT NOT NULL CHECK (estado IN ('pendente', 'pago', 'enviado')),
    total_cents INTEGER NOT NULL,
    moeda TEXT NOT NULL DEFAULT 'EUR',
    nome_envio TEXT,
    morada_envio TEXT,
    telefone_contacto TEXT,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id)
);

CREATE TRIGGER trg_encomendas_update
AFTER UPDATE ON encomendas
BEGIN
    UPDATE encomendas
    SET atualizado_em = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TABLE itens_encomenda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encomenda_id INTEGER NOT NULL,
    produto_id INTEGER,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unit_cents INTEGER NOT NULL,
    FOREIGN KEY (encomenda_id) REFERENCES encomendas(id) ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE SET NULL
);

CREATE TABLE notificacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilizador_id INTEGER,
    tipo TEXT NOT NULL,
    conteudo TEXT,
    lida INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilizador_id) REFERENCES utilizadores(id) ON DELETE CASCADE
);

CREATE TABLE historico_produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    acao TEXT NOT NULL,
    alterado_por INTEGER,
    valores_antigos TEXT,
    valores_novos TEXT,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE SET NULL,
    FOREIGN KEY (alterado_por) REFERENCES utilizadores(id) ON DELETE SET NULL
);

CREATE TABLE configuracoes (
    chave TEXT PRIMARY KEY,
    valor TEXT
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