def menu_cliente():
    while True:
        print("\n--- Menu Cliente ---")
        print("1 - Ver catálogo")
        print("2 - Adicionar produto ao carrinho")
        print("3 - Ver carrinho")
        print("4 - Remover do carrinho")
        print("5 - Filtrar produtos por preço")
        print("6 - Finalizar compra")
        print("0 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            ver_catalogo()

        elif opcao == "2":
            adicionar_ao_carrinho()

        elif opcao == "3":
            ver_carrinho()

        elif opcao == "4":
            remover_do_carrinho()

        elif opcao == "5":
            filtrar_produtos()

        elif opcao == "6":
            finalizar_compra()

        elif opcao == "0":
            break

        else:
            print("Opção inválida! Tente novamente.")




    def ver_catalogo():
        print(" Exibindo catálogo de produtos...")


    def adicionar_ao_carrinho():
        print(" Produto adicionado ao carrinho!")


    def ver_carrinho():
        print(" Exibindo itens do carrinho...")

    
    def remover_do_carrinho():
        print(" Produto removido do carrinho!")