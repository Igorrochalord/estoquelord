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

while True:
    print("\n----- Sistema de controle de estoque -----")
    print("1 - Adicionar produto")
    print("2 - Remover produto")
    print("3 - Fazer pedido")
    print("4 - Sair")
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
        quantidade = int(input("Digite a quantidade desejada: "))
        fazer_pedido(produto, quantidade)
    elif opcao == 4:
        break
    else:
        print("Opção inválida")