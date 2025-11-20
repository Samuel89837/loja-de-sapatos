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
        print("\n--- Menu Administrador ---")
        print("1 - Adicionar produto")
        print("2 - Editar produto")
        print("3 - Remover produto")
        print("0 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_produto()
        elif opcao == "2":
            editar_produto()
        elif opcao == "3":
            remover_produto()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")