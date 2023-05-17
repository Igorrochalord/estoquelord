import cv2
from pyzbar import pyzbar
from time import sleep

estoque = {}
contatos = [
    {"nome": "Pedro Augusto", "empresa": "Brasilia Distribuidora de alimentos", "telefone": "61-991209984"},
    {"nome": "Marques Diniz", "empresa": "Marques Distribuidora de bebidas", "telefone": "61-998541200"},
    {"nome": "Sergio Amorin", "empresa": "Rac Distribuidora de alimentos", "telefone": "61-3475-7972"},
    {"nome": "Lucas Andrade", "empresa": "DF Distribuidora", "telefone": "61-3037-73332"},
    {"nome": "Marcos Silva", "empresa": "Distribuidora de bebidas fale baixo ", "telefone": "61-30458920"},
    {"nome": "Swift", "empresa": "Swift", "telefone": "08004002892"},
    {"nome": "Israel Gonçalves  ", "empresa": "Meats distribuidora ", "telefone": "61-3042-0340"},
    {"nome": "AMBEV", "empresa": "AMBEV", "telefone": "(61)999351306"}
    ]

def adicionar_produto():
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")
    preco = float(input("Digite o preço do produto: "))
    quantidade = int(input("Digite a quantidade do produto: "))
    produto = {"nome": nome, "descricao": descricao, "preco": preco, "quantidade": quantidade}
    estoque[nome] = produto
    print("Produto adicionado ao estoque com sucesso!")
    if quantidade <= 6:
        print("Alerta de estoque! Recomendamos entrar em contato com um distribuidor")


def remover_produto():
    nome = input("Digite o nome do produto: ")
    if nome in estoque:
        del estoque[nome]
        print("Produto removido do estoque com sucesso!")
    else:
        print("Produto não encontrado no estoque")


def fazer_pedido():
    nome = input("Digite o nome do produto: ")
    if nome in estoque:
        quantidade = int(input("Digite a quantidade do produto: "))
        if estoque[nome]["quantidade"] >= quantidade:
            estoque[nome]["quantidade"] -= quantidade
            print(f"Pedido de {quantidade} {nome}(s) realizado com sucesso!")
            if estoque[nome]["quantidade"] <= 6:
                opcao = input("Alerta de estoque! Deseja exibir a lista de contatos para contato? (s/n) ")
                if opcao.lower() == "s":
                    for contato in contatos:
                        sleep(0.5)
                        print(f"{contato['nome']} da empresa {contato['empresa']}. Telefone: {contato['telefone']}")
        else:
            print("Não há produtos suficientes em estoque")
    else:
        print("Produto não encontrado no estoque")


def digitalizar_produto():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            print("Código de barras detectado")
            print("Tipo de código: ", obj.type)
            print("Código: ", obj.data)
            nome = obj.data.decode('utf-8')
            if nome in estoque:
                print(f"O produto {nome} está em estoque com quantidade de {estoque[nome]['quantidade']}")
            else:
                print("Produto não encontrado no estoque")
                adicionar = input("Deseja adicionar este produto ao estoque? (s/n) ")
                if adicionar.lower() == "s":
                    descricao = input("Digite a descrição do produto: ")
                    preco = float(input("Digite o preço do produto: "))
                    quantidade = int(input("Digite a quantidade do produto: "))
                    produto = {"nome": nome, "descricao": descricao, "preco": preco, "quantidade": quantidade}
                    estoque[nome] = produto
                    print("Produto adicionado ao estoque com sucesso!")
                    if quantidade <= 6:
                        opcao = input("Alerta de estoque! Deseja exibir a lista de contatos para contato? (s/n) ")
                        if opcao.lower() == "s":
                            for contato in contatos:
                                print(f"{contato['nome']} da empresa {contato['empresa']}. Telefone: {contato['telefone']}")
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def exibir_estoque():
    for nome, produto in estoque.items():
        print(f"Nome: {nome}, Descrição: {produto['descricao']}, Preço: {produto['preco']}, Quantidade: {produto['quantidade']}")


def exibir_menu():
    print("Bem-vindo ao sistema de gerenciamento de estoque")
    print("Selecione uma opção:")
    print("1 - Adicionar produto")
    print("2 - Remover produto")
    print("3 - Fazer pedido")
    print("4 - Digitalizar produto")
    print("5 - Exibir estoque")
    print("6 - Sair")
    opcao = int(input("Opção: "))
    return opcao


def main():
    while True:
        opcao = exibir_menu()
        if opcao == 1:
            adicionar_produto()
        elif opcao == 2:
            remover_produto()
        elif opcao == 3:
            fazer_pedido()
        elif opcao == 4:
            digitalizar_produto()
        elif opcao == 5:
            exibir_estoque()
        elif opcao == 6:
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()

