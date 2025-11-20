from db import conectar

# =====================================================
# MENU CLIENTE
# =====================================================
def menu_cliente():
    while True:
        print("\n===== MENU CLIENTE =====")
        print("1 - Ver catálogo")
        print("2 - Procurar produto")
        print("3 - Ver detalhes de um produto")
        print("4 - Filtrar produtos por preço")
        print("5 - Ver produtos por categoria")
        print("6 - Ver produtos relacionados")
        print("7 - Ver carrinho")
        print("8 - Adicionar produto ao carrinho")
        print("9 - Remover produto do carrinho")
        print("10 - Alterar quantidade no carrinho")
        print("11 - Ver total da compra")
        print("12 - Finalizar compra")
        print("0 - Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            ver_catalogo()

        elif opcao == "2":
            procurar_produto()

        elif opcao == "3":
            ver_detalhes_produto()

        elif opcao == "4":
            filtrar_produtos()

        elif opcao == "5":
            ver_por_categoria()

        elif opcao == "6":
            produtos_relacionados()

        elif opcao == "7":
            ver_carrinho()

        elif opcao == "8":
            adicionar_ao_carrinho()

        elif opcao == "9":
            remover_do_carrinho()

        elif opcao == "10":
            alterar_quantidade_carrinho()

        elif opcao == "11":
            total_carrinho()

        elif opcao == "12":
            finalizar_compra()

        elif opcao == "0":
            break

        else:
            print("Opção inválida, tente novamente!")


# =====================================================
# FUNÇÕES DO CLIENTE
# =====================================================

def ver_catalogo():
    """
    Mostra a lista completa de produtos disponíveis e respetivos preços.

    Args:
        None

    Returns:
        None
    """
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, titulo, preco_cents, stock FROM produtos")
    produtos = cur.fetchall()

    print("\n===== CATÁLOGO =====")
    for p in produtos:
        status = "ESGOTADO" if p[3] == 0 else f"Stock: {p[3]}"
        print(f"ID: {p[0]} | {p[1]} | {p[2]/100:.2f}€ | {status}")

    con.close()



def procurar_produto():
    """
    Pesquisa produtos pelo nome introduzido pelo utilizador.

    Args:
        None

    Returns:
        None
    """
    termo = input("Nome do produto: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, titulo, preco_cents FROM produtos WHERE titulo LIKE ?", 
                ('%' + termo + '%',))
    produtos = cur.fetchall()

    print("\n===== RESULTADOS =====")
    for p in produtos:
        print(f"ID: {p[0]} | {p[1]} | {p[2]/100:.2f}€")

    con.close()


def ver_detalhes_produto():
    """
    Mostra informações completas de um produto escolhido pelo utilizador.

    Args:
        None

    Returns:
        None

    Raises:
        ValueError: Se o ID não existir.
    """

    pid = input("ID do produto: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM produtos WHERE id = ?", (pid,))
    p = cur.fetchone()

    if p:
        print("\n===== DETALHES =====")
        print(f"ID: {p[0]}")
        print(f"Título: {p[1]}")
        print(f"Descrição: {p[2]}")
        print(f"Preço: {p[3]/100:.2f}€")
        print(f"Stock: {p[6]}")
    else:
        print("Produto não encontrado.")

    con.close()


def filtrar_produtos():
    """
    Filtra e apresenta produtos dentro de um intervalo de preços.

    Args:
        None

    Returns:
        None
    """

    minimo = int(input("Preço mínimo (centimos): "))
    maximo = int(input("Preço máximo (centimos): "))

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT id, titulo, preco_cents 
        FROM produtos 
        WHERE preco_cents BETWEEN ? AND ?
    """, (minimo, maximo))

    produtos = cur.fetchall()

    print("\n===== FILTRADOS =====")
    for p in produtos:
        print(f"{p[0]} - {p[1]} - {p[2]/100:.2f}€")

    con.close()


def ver_por_categoria():
    """
    Mostra produtos que pertencem a uma categoria escolhida pelo utilizador.

    Args:
        None

    Returns:
        None
    """

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, nome FROM categorias")
    categorias = cur.fetchall()

    print("\nCategorias disponíveis:")
    for c in categorias:
        print(f"{c[0]} - {c[1]}")

    cid = input("Escolha uma categoria: ")

    cur.execute("""
        SELECT id, titulo, preco_cents 
        FROM produtos 
        WHERE categoria_id = ?
    """, (cid,))

    produtos = cur.fetchall()

    print("\nProdutos:")
    for p in produtos:
        print(f"{p[0]} - {p[1]} - {p[2]/100:.2f}€")

    con.close()


def produtos_relacionados():
    """
    Mostra produtos da mesma categoria do produto escolhido, exceto ele próprio.

    Args:
        None

    Returns:
        None
    """ 
    
    pid = input("ID do produto: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT categoria_id FROM produtos WHERE id = ?", (pid,))
    row = cur.fetchone()

    if not row:
        print("Produto não encontrado.")
        return

    categoria = row[0]

    cur.execute("""
        SELECT id, titulo 
        FROM produtos 
        WHERE categoria_id = ? AND id != ?
    """, (categoria, pid))

    relacionados = cur.fetchall()

    print("\nProdutos relacionados:")
    for r in relacionados:
        print(f"{r[0]} - {r[1]}")

    con.close()


def ver_carrinho():
    """
    Mostra todos os produtos atualmente presentes no carrinho do utilizador.

    Args:
        None

    Returns:
        None
    """
    
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT p.titulo, i.quantidade, p.preco_cents 
        FROM itens_carrinho i
        JOIN produtos p ON p.id = i.produto_id
        WHERE i.utilizador_id = 1
    """)

    itens = cur.fetchall()

    print("\n===== CARRINHO =====")
    if not itens:
        print("Carrinho vazio.")
    else:
        for item in itens:
            print(f"{item[0]} - {item[1]} unidades - {item[2]/100:.2f}€")

    con.close()



def adicionar_ao_carrinho():
    """
    Adiciona um produto ao carrinho, valida o stock e
    atualiza a quantidade caso já existam no carrinho.

    Args:
        None

    Returns:
        None

    Raises:
        ValueError: Caso a quantidade pedida ultrapasse o stock disponível.
    """

    pid = input("ID do produto: ")
    qtd = int(input("Quantidade: "))

    con = conectar()
    cur = con.cursor()

    # Verificar stock atual
    cur.execute("SELECT stock, titulo FROM produtos WHERE id = ?", (pid,))
    produto = cur.fetchone()

    if not produto:
        print("Produto não encontrado!")
        con.close()
        return

    stock_atual, nome = produto

    if stock_atual <= 0:
        print(f"O produto '{nome}' está ESGOTADO.")
        con.close()
        return

    # verificar se já existe no carrinho
    cur.execute("""
        SELECT quantidade FROM itens_carrinho
        WHERE utilizador_id = 1 AND produto_id = ?
    """, (pid,))
    
    existente = cur.fetchone()

    # SE JÁ EXISTE → somar quantidade
    if existente:
        nova_qtd = existente[0] + qtd

        if nova_qtd > stock_atual:
            print(f"Stock insuficiente! Disponível: {stock_atual} unidades.")
            con.close()
            return

        cur.execute("""
            UPDATE itens_carrinho
            SET quantidade = ?
            WHERE utilizador_id = 1 AND produto_id = ?
        """, (nova_qtd, pid))

        con.commit()
        print(f"✔ Quantidade atualizada no carrinho! Agora tens {nova_qtd}x '{nome}'.")
        con.close()
        return
    
    # SE NÃO EXISTE → inserir normalmente
    if qtd > stock_atual:
        print(f"Stock insuficiente! Disponível: {stock_atual} unidades.")
        con.close()
        return

    cur.execute("""
        INSERT INTO itens_carrinho (utilizador_id, produto_id, quantidade)
        VALUES (1, ?, ?)
    """, (pid, qtd))

    con.commit()
    print(f"✔ '{nome}' adicionado ao carrinho! ({qtd} unidades)")
    con.close()




def remover_do_carrinho():
    """
    Remove totalmente um produto do carrinho do utilizador.

    Args:
        None

    Returns:
        None
    """

    pid = input("ID do produto para remover: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        DELETE FROM itens_carrinho 
        WHERE utilizador_id = 1 AND produto_id = ?
    """, (pid,))  # <-- reparei o erro aqui

    con.commit()
    print("Removido!")
    con.close()



def alterar_quantidade_carrinho():
    """
    Altera a quantidade de um item já existente no carrinho,
    verificando se existe stock suficiente.

    Args:
        None

    Returns:
        None

    Raises:
        ValueError: Se o produto não existir ou não houver stock suficiente.
    """

    pid = input("Produto: ")
    qtd = int(input("Nova quantidade: "))

    con = conectar()
    cur = con.cursor()

    # verificar stock do produto
    cur.execute("SELECT stock, titulo FROM produtos WHERE id = ?", (pid,))
    produto = cur.fetchone()

    if not produto:
        print("Produto não encontrado!")
        con.close()
        return

    stock_atual, nome = produto

    if qtd > stock_atual:
        print(f"Stock insuficiente! Disponível: {stock_atual} unidades.")
        con.close()
        return

    # atualizar carrinho
    cur.execute("""
        UPDATE itens_carrinho 
        SET quantidade = ?
        WHERE utilizador_id = 1 AND produto_id = ?
    """, (qtd, pid))

    con.commit()
    print(f"Quantidade atualizada para '{nome}' → {qtd} unidades")
    con.close()




def total_carrinho():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT SUM(quantidade * preco_cents)
        FROM itens_carrinho i
        JOIN produtos p ON p.id = i.produto_id
        WHERE i.utilizador_id = 1
    """)

    total = cur.fetchone()[0]

    print("\n===== TOTAL =====")
    print(f"Total: {(total or 0) / 100:.2f}€")

    con.close()


def finalizar_compra():
    con = conectar()
    cur = con.cursor()

    # total
    cur.execute("""
        SELECT SUM(quantidade * preco_cents)
        FROM itens_carrinho i
        JOIN produtos p ON p.id = i.produto_id
        WHERE i.utilizador_id = 1
    """)
    total = cur.fetchone()[0]

    if not total:
        print("Carrinho vazio!")
        return

    # criar encomenda
    cur.execute("""
        INSERT INTO encomendas (utilizador_id, estado, total_cents)
        VALUES (1, 'pendente', ?)
    """, (total,))
    encomenda_id = cur.lastrowid

    # gerar itens_encomenda
    cur.execute("""
        INSERT INTO itens_encomenda (encomenda_id, produto_id, quantidade, preco_unit_cents)
        SELECT ?, produto_id, quantidade, preco_cents
        FROM itens_carrinho
        JOIN produtos ON produtos.id = itens_carrinho.produto_id
        WHERE utilizador_id = 1
    """, (encomenda_id,))

    #DESCONTAR STOCK (a parte que faltava)
    cur.execute("""
        UPDATE produtos
        SET stock = stock - (
            SELECT quantidade 
            FROM itens_carrinho 
            WHERE produto_id = produtos.id AND utilizador_id = 1
        )
        WHERE id IN (
            SELECT produto_id FROM itens_carrinho WHERE utilizador_id = 1
        )
    """)

    # limpar carrinho
    cur.execute("DELETE FROM itens_carrinho WHERE utilizador_id = 1")
    con.commit()

    print(f"Compra finalizada! Encomenda #{encomenda_id}")
    con.close()
