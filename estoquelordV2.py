import cv2
from pyzbar import pyzbar

codigo_barras_produtos = {
    "arroz": "7891234567890",
    "feijão": "7890987654321",
    "macarrão": "1234567890123",
    "leite": "0987654321098",
    "café": "1357986420477"
}

estoque = {}

def adicionar_produto(produto, quantidade):
    if produto in estoque:
        estoque[produto] += quantidade
    else:
        estoque[produto] = quantidade
    print(f"{quantidade} unidades de {produto} adicionadas ao estoque")

def remover_produto(produto, quantidade):
    if produto not in estoque:
        print("Produto não encontrado no estoque")
    elif estoque[produto] < quantidade:
        print("Quantidade removida maior do que o estoque disponível")
    else:
        estoque[produto] -= quantidade
        print(f"{quantidade} unidades de {produto} removidas do estoque")

def fazer_pedido(produto, quantidade):
    if produto not in estoque:
        print("Produto não encontrado no estoque")
    elif estoque[produto] < quantidade:
        print("Estoque insuficiente para atender ao pedido")
    else:
        estoque[produto] -= quantidade
        print(f"{quantidade} unidades de {produto} enviadas")

def mostrar_estoque():
    print("\n----- Estoque atual -----")
    for produto, quantidade in estoque.items():
        print(f"{produto}: {quantidade}")

def digitalizar_produto():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar imagem da câmera")
            break
        decoded_objects = pyzbar.decode(frame)
        if decoded_objects:
            for obj in decoded_objects:
                barcode = obj.data.decode("utf-8")
                produto = None
                for p, cb in codigo_barras_produtos.items():
                    if cb == barcode:
                        produto = p
                        break
                if produto is None:
                    print("Produto não encontrado")
                else:
                    print(f"{produto}: {estoque.get(produto, 0)} unidades em estoque")
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

while True:
    print("\n----- Sistema de controle de estoque -----")
    print("1 - Adicionar produto")
    print("2 - Remover produto")
    print("3 - Fazer pedido")
    print("4 - Digitalizar produto")
    print("5 - Mostrar estoque")
    print("6 - Sair")
    opcao = int(input("Digite a opção desejada: "))
    if opcao == 1:
        produto = input("Digite o nome do produto: ")
        quantidade = int(input("Digite a quantidade a ser adicionada: "))
        adicionar_produto(produto, quantidade)
    elif opcao == 2:
        produto = input("Digite o nome do produto: ")
        quantidade = int(input("Digite a quantidade a ser removida: "))
        remover_produto(produto, quantidade)
    elif opcao == 3:
        produto = input("Digite o nome do produto: ")
        quantidade = int(input("Digite a quantidade a ser enviada: "))
        fazer_pedido(produto, quantidade)
    elif opcao == 4:
        digitalizar_produto()
    elif opcao == 5:
        mostrar_estoque()
    elif opcao == 6:
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida, tente novamente")
