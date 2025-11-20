from db import conectar

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

        cur.execute("SELECT id, titulo, preco_cents FROM produtos WHERE titulo LIKE ?", ('%' + termo + '%',))
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

        cur.execute("SELECT id, titulo, preco_cents FROM produtos WHERE preco_cents BETWEEN ? AND ?", (minimo, maximo))
        produtos = cur.fetchall()

        print("\n===== FILTRADOS =====")
        for p in produtos:
            print(f"{p[0]} - {p[1]} - {p[2]/100:.2f}€")

        con.close()

    def adicionar_ao_carrinho():
        print(" Produto adicionado ao carrinho!")


    def ver_carrinho():
        print(" Exibindo itens do carrinho...")

    
    def remover_do_carrinho():
        print(" Produto removido do carrinho!")


    def filtrar_produtos():
        print(" Filtrando produtos por preço...")

    
    def finalizar_compra():
        print(" Compra finalizada com sucesso!")


