import cv2
from pyzbar import pyzbar

estoque = {}

def adicionar_produto():
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")
    preco = float(input("Digite o preço do produto: "))
    quantidade = int(input("Digite a quantidade do produto: "))
    produto = {"nome": nome, "descricao": descricao, "preco": preco, "quantidade": quantidade}
    estoque[nome] = produto
    print("Produto adicionado ao estoque com sucesso!")

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
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def mostrar_estoque():
    for nome, produto in estoque.items():
        print(f"Produto: {produto['nome']}, Descrição: {produto['descricao']}, Preço: R${produto['preco']}, Quantidade: {produto['quantidade']}")

while True:
    print("== Sistema de Controle de Estoque ==")
    print("1 - Adicionar produto")
    print("2 - Remover produto")
    print("3 - Fazer pedido")
    print("4 - Digitalizar produto")
    print("5 - Mostrar estoque")
    print("6 - Sair do sistema")
    opcao = int(input("Digite a opção desejada: "))

    if opcao == 1:
        adicionar_produto()

    elif opcao == 2:
        remover_produto()

    elif opcao == 3:
        fazer_pedido()

    elif opcao == 4:
        digitalizar_produto()

    elif opcao == 5:
        mostrar_estoque()

    elif opcao == 6:
        print("Obrigado por utilizar o sistema de controle de estoque!")
        break

    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
