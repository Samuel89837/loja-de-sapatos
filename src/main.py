from cliente import menu_cliente
from admin import menu_admin

def main():
    while True:
        print("\n===== LOJA ONLINE =====")
        print("1 - Entrar como Cliente")
        print("2 - Entrar como Administrador")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            menu_cliente()
        elif opcao == "2":
            menu_admin()
        elif opcao == "0":
            print("A sair... Até logo!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()