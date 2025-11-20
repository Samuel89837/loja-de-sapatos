from db import conectar
from datetime import datetime


ADMIN_CREDENCIAIS = {
    "utilizador": "admin",
    "password": "1234"
}

def autenticar_admin():
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