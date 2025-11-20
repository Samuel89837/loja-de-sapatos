from db import conectar

# =====================================================
# MENU CLIENTE
# =====================================================
def menu_cliente(uid):
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
            ver_carrinho(uid)

        elif opcao == "8":
            adicionar_ao_carrinho(uid)

        elif opcao == "9":
            remover_do_carrinho(uid)

        elif opcao == "10":
            alterar_quantidade_carrinho(uid)

        elif opcao == "11":
            total_carrinho(uid)

        elif opcao == "12":
            finalizar_compra(uid)

        elif opcao == "0":
            break

        else:
            print("Opção inválida, tente novamente!")


# =====================================================
# FUNÇÕES DO CLIENTE
# =====================================================

def ver_catalogo():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, titulo, preco_cents, stock FROM produtos WHERE ativo = 1")
    produtos = cur.fetchall()

    print("\n===== CATÁLOGO =====")
    for p in produtos:
        print(f"ID: {p[0]} | {p[1]} | {p[2]/100:.2f}€ | Stock: {p[3]}")

    con.close()


def procurar_produto():
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


def ver_carrinho(uid):
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT p.titulo, i.quantidade, p.preco_cents 
        FROM itens_carrinho i
        JOIN produtos p ON p.id = i.produto_id
        WHERE i.utilizador_id = ?
    """, (uid,))

    itens = cur.fetchall()

    print("\n===== CARRINHO =====")
    if not itens:
        print("Carrinho vazio.")
    else:
        for item in itens:
            print(f"{item[0]} - {item[1]} unidades - {item[2]/100:.2f}€")

    con.close()


def adicionar_ao_carrinho(uid):
    pid = input("ID do produto: ")
    qtd = int(input("Quantidade: "))

    con = conectar()
    cur = con.cursor()

    try:
        cur.execute("""
            INSERT INTO itens_carrinho (utilizador_id, produto_id, quantidade)
            VALUES (?, ?, ?)
        """, (uid, pid, qtd))

        con.commit()
        print("Produto adicionado!")
    except:
        print("Erro ao adicionar. Talvez já esteja no carrinho.")

    con.close()


def remover_do_carrinho(uid):
    pid = input("ID do produto para remover: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        DELETE FROM itens_carrinho 
        WHERE utilizador_id = ? AND produto_id = ?
    """, (uid, pid))

    con.commit()
    print("Removido!")
    con.close()


def alterar_quantidade_carrinho(uid):
    pid = input("Produto: ")
    qtd = int(input("Nova quantidade: "))

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        UPDATE itens_carrinho 
        SET quantidade = ?
        WHERE utilizador_id = ? AND produto_id = ?
    """, (qtd, uid, pid))

    con.commit()
    print("Quantidade atualizada!")
    con.close()


def total_carrinho(uid):
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT SUM(quantidade * preco_cents)
        FROM itens_carrinho i
        JOIN produtos p ON p.id = i.produto_id
        WHERE i.utilizador_id = ?
    """, (uid,))

    total = cur.fetchone()[0]

    print("\n===== TOTAL =====")
    print(f"Total: {(total or 0) / 100:.2f}€")

    con.close()


def finalizar_compra(uid):
    con = conectar()
    cur = con.cursor()

    # total
    cur.execute("""
        SELECT SUM(quantidade * preco_cents)
        FROM itens_carrinho i
        JOIN produtos p ON p.id = i.produto_id
        WHERE i.utilizador_id = ?
    """, (uid,))

    total = cur.fetchone()[0]

    if not total:
        print("Carrinho vazio!")
        return

    # criar encomenda
    cur.execute("""
        INSERT INTO encomendas (utilizador_id, estado, total_cents)
        VALUES (?, 'pendente', ?)
    """, (uid, total))

    encomenda_id = cur.lastrowid

    # gerar itens_encomenda
    cur.execute("""
        INSERT INTO itens_encomenda (encomenda_id, produto_id, quantidade, preco_unit_cents)
        SELECT ?, produto_id, quantidade, preco_cents
        FROM itens_carrinho
        JOIN produtos ON produtos.id = itens_carrinho.produto_id
        WHERE utilizador_id = ?
    """, (encomenda_id, uid))

    # limpar carrinho
    cur.execute("DELETE FROM itens_carrinho WHERE utilizador_id = ?", (uid,))
    con.commit()

    print(f"Compra finalizada! Encomenda #{encomenda_id}")
    con.close()
