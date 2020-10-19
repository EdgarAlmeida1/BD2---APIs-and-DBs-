
class View():
    def inicio(self):
        return self.menu()

    def menu(self):
        print("**************** MENU ****************")
        print("1 - Dar carga no banco de dados relacional")
        print("2 - Dump dos dados em JSON para o banco orientado a documentos")
        print("0 - Sair")
        opt = int(input("Digite a opcao: "))
        return opt