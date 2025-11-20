from db import conectar
from datetime import datetime


ADMIN_CREDENCIAIS = {
    "utilizador": "admin",
    "password": "1234"
}

def autenticar_admin():

    """
    Realiza a autenticação do administrador através de input.

    Args:
        None

    Returns:
        bool: True se as credenciais forem válidas, False caso contrário.
    """

    print("\n=== Login do Administrador ===")
    user = input("Utilizador: ")
    password = input("Palavra-passe: ")

    if user == ADMIN_CREDENCIAIS["utilizador"] and password == ADMIN_CREDENCIAIS["password"]:
        print("\nLogin bem-sucedido!")
        return True
    else:
        print("\nCredenciais incorretas. Acesso negado.")
        return False



def menu_admin():
    """
    Apresenta o menu do administrador e encaminha a escolha
    para as funções respetivas.

    Args:
        None

    Returns:
        None
    """
    
    if not autenticar_admin():
        return

    while True:
        print("\n--- MENU ADMINISTRADOR ---")
        print("1 - Adicionar produto")
        print("2 - Editar produto")
        print("3 - Remover produto")
        print("4 - Listar produtos")
        print("5 - Ver notificações de pedidos")
        print("6 - Ativar/Desativar produtos")
        print("7 - Adicionar categoria")
        print("8 - Total de produtos em stock")
        print("9 - Total de vendas diárias")
        print("10 - Histórico de alterações")
        print("11 - Gerir utilizadores")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_produto()
        elif opcao == "2":
            editar_produto()
        elif opcao == "3":
            remover_produto()
        elif opcao == "4":
            listar_produtos()
        elif opcao == "5":
            ver_notificacoes()
        elif opcao == "6":
            ativar_desativar_produto()
        elif opcao == "7":
            adicionar_categoria()
        elif opcao == "8":
            total_stock()
        elif opcao == "9":
            vendas_diarias()
        elif opcao == "10":
            historico_alteracoes()
        elif opcao == "11":
            gerir_utilizadores()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


    
    
# ==========================================
#   ADICIONAR PRODUTO
# ==========================================
def adicionar_produto():
    print("\n=== Adicionar Produto ===")
    titulo = input("Nome: ")
    descricao = input("Descrição: ")
    preco = float(input("Preço (€): "))
    stock = int(input("Stock inicial: "))
    categoria = input("ID da categoria: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO produtos (titulo, descricao, preco_cents, stock, categoria_id, ativo)
        VALUES (?, ?, ?, ?, ?, 1)
    """, (titulo, descricao, int(preco * 100), stock, categoria))

    con.commit()
    print("Produto adicionado com sucesso!")
    con.close()


# ==========================================
#   EDITAR PRODUTO
# ==========================================
def editar_produto():
    pid = input("\nID do produto a editar: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, titulo, descricao, preco_cents, stock FROM produtos WHERE id = ?", (pid,))
    produto = cur.fetchone()

    if not produto:
        print("Produto não encontrado!")
        return

    print(f"\nProduto atual:")
    print(f"Nome: {produto[1]}")
    print(f"Descrição: {produto[2]}")
    print(f"Preço: {produto[3] / 100:.2f}€")
    print(f"Stock: {produto[4]}")

    novo_nome = input("Novo nome (ENTER p/ manter): ") or produto[1]
    nova_desc = input("Nova descrição (ENTER p/ manter): ") or produto[2]
    novo_preco = input("Novo preço (ENTER p/ manter): ")
    novo_preco = int(float(novo_preco) * 100) if novo_preco else produto[3]
    novo_stock = input("Novo stock (ENTER p/ manter): ")
    novo_stock = int(novo_stock) if novo_stock else produto[4]

    cur.execute("""
        UPDATE produtos 
        SET titulo = ?, descricao = ?, preco_cents = ?, stock = ?, atualizado_em = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (novo_nome, nova_desc, novo_preco, novo_stock, pid))

    con.commit()
    print("Produto editado com sucesso!")
    con.close()



# ==========================================
#   REMOVER PRODUTO
# ==========================================
def remover_produto():
    pid = input("\nID do produto a remover: ")

    con = conectar()
    cur = con.cursor()

    # Verificar se o ID existe
    cur.execute("SELECT titulo FROM produtos WHERE id = ?", (pid,))
    produto = cur.fetchone()

    if not produto:
        print(f" O produto com ID {pid} não existe ou já foi removido!")
        con.close()
        return

    nome = produto[0]

    # Remover o produto
    cur.execute("DELETE FROM produtos WHERE id = ?", (pid,))
    con.commit()

    print(f" Produto '{nome}' removido com sucesso!")
    con.close() 




# ==========================================
#   LISTAR PRODUTOS
# ==========================================
def listar_produtos():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, titulo, preco_cents, stock, ativo FROM produtos")
    produtos = cur.fetchall()

    print("\n=== LISTA DE PRODUTOS ===")
    for p in produtos:
        estado = "Ativo" if p[4] else "Inativo"
        print(f"{p[0]} | {p[1]} | {p[2]/100:.2f}€ | Stock: {p[3]} | {estado}")

    con.close() 



# ==========================================
#   VER NOTIFICAÇÕES (ENCOMENDAS PENDENTES)
# ==========================================
def ver_notificacoes():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT id, utilizador_id, total_cents, estado 
        FROM encomendas
        WHERE estado = 'pendente'
    """)

    pedidos = cur.fetchall()

    print("\n=== NOTIFICAÇÕES DE NOVOS PEDIDOS ===")
    if not pedidos:
        print("Nenhum pedido pendente.")
    else:
        for p in pedidos:
            print(f"Encomenda #{p[0]} | Cliente: {p[1]} | Total: {p[2] / 100:.2f}€ | Estado: {p[3]}")

    con.close()


#==========================================
# ATIVAR / DESATIVAR PRODUTO
#==========================================
def ativar_desativar_produto():
    pid = input("ID do produto: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT titulo, ativo FROM produtos WHERE id = ?", (pid,))
    produto = cur.fetchone()

    if not produto:
        print("Produto não encontrado!")
        return

    nome, ativo = produto
    print(f"\nEstado atual: {'Ativo' if ativo else 'Inativo'}")

    # Alterna o estado
    novo_estado = 0 if ativo == 1 else 1

    cur.execute("""
        UPDATE produtos 
        SET ativo = ? 
        WHERE id = ?
    """, (novo_estado, pid))

    con.commit()

    print(f"Produto '{nome}' agora está: {'Ativo' if novo_estado else 'Inativo'}")
    con.close()


#==========================================
#ADICIONAR CATEGORIA
#==========================================
def adicionar_categoria():
    nome = input("\nNome da categoria: ")
    desc = input("Descrição: ")

    con = conectar()
    cur = con.cursor()

    cur.execute("INSERT INTO categorias (nome, descricao) VALUES (?, ?)", (nome, desc))
    con.commit()

    print("Categoria adicionada!")
    con.close()




#==========================================
#TOTAL DO STOCK
#==========================================
def total_stock():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT SUM(stock) FROM produtos")
    total = cur.fetchone()[0]

    print(f"\nTotal de produtos em stock: {total}")
    con.close()




#==========================================
#VENDAS DIÁRIAS
#==========================================
def vendas_diarias():
    hoje = datetime.now().strftime("%Y-%m-%d")

    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT SUM(total_cents) 
        FROM encomendas
        WHERE DATE(criado_em) = ?
    """, (hoje,))

    total = cur.fetchone()[0]

    print(f"\nVendas de hoje ({hoje}): {(total or 0)/100:.2f}€")
    con.close()




#==========================================
#HISTÓRICO DE ALTERAÇÕES
#==========================================
def historico_alteracoes():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT produto_id, acao, criado_em
        FROM historico_produtos
        ORDER BY criado_em DESC
    """)

    hist = cur.fetchall()

    print("\n=== HISTÓRICO DE ALTERAÇÕES ===")
    for h in hist:
        print(f"Produto {h[0]} | {h[1]} | {h[2]}")

    con.close()





#==========================================
#GERIR UTILIZADORES
#==========================================
def gerir_utilizadores():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, nome, email FROM utilizadores")
    utilizadores = cur.fetchall()

    print("\n=== UTILIZADORES ===")
    for u in utilizadores:
        print(f"{u[0]} | {u[1]} | {u[2]}")

    con.close()



