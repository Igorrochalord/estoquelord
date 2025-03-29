import cv2
from pyzbar import pyzbar
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["estoque"]
collection = db["produtos"]

# Função para adicionar produto ao MongoDB
def adicionar_produto():
    nome = simpledialog.askstring("Adicionar Produto", "Digite o nome do produto:")
    descricao = simpledialog.askstring("Adicionar Produto", "Digite a descrição do produto:")
    preco = simpledialog.askfloat("Adicionar Produto", "Digite o preço do produto:")
    quantidade = simpledialog.askinteger("Adicionar Produto", "Digite a quantidade do produto:")
    
    if nome and descricao and preco and quantidade:
        produto = {"nome": nome, "descricao": descricao, "preco": preco, "quantidade": quantidade}
        collection.insert_one(produto)
        messagebox.showinfo("Sucesso", "Produto adicionado ao estoque com sucesso!")
        if quantidade <= 6:
            messagebox.showwarning("Alerta de Estoque", "Estoque baixo! Recomendamos entrar em contato com um distribuidor.")
    else:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")

# Função para remover produto do MongoDB
def remover_produto():
    nome = simpledialog.askstring("Remover Produto", "Digite o nome do produto:")
    produto = collection.find_one({"nome": nome})
    if produto:
        collection.delete_one({"nome": nome})
        messagebox.showinfo("Sucesso", "Produto removido do estoque com sucesso!")
    else:
        messagebox.showerror("Erro", "Produto não encontrado no estoque")

# Função para modificar produto no MongoDB
def modificar_produto():
    nome = simpledialog.askstring("Modificar Produto", "Digite o nome do produto:")
    produto = collection.find_one({"nome": nome})
    if produto:
        descricao = simpledialog.askstring("Modificar Produto", f"Digite a nova descrição do produto ({produto['descricao']}):", initialvalue=produto['descricao'])
        preco = simpledialog.askfloat("Modificar Produto", f"Digite o novo preço do produto ({produto['preco']}):", initialvalue=produto['preco'])
        quantidade = simpledialog.askinteger("Modificar Produto", f"Digite a nova quantidade do produto ({produto['quantidade']}):", initialvalue=produto['quantidade'])
        
        if descricao and preco and quantidade:
            collection.update_one({"nome": nome}, {"$set": {"descricao": descricao, "preco": preco, "quantidade": quantidade}})
            messagebox.showinfo("Sucesso", "Produto modificado com sucesso!")
            if quantidade <= 6:
                messagebox.showwarning("Alerta de Estoque", "Estoque baixo! Recomendamos entrar em contato com um distribuidor.")
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
    else:
        messagebox.showerror("Erro", "Produto não encontrado no estoque")

# Função para fazer pedido e atualizar o MongoDB
def fazer_pedido(nome=None):
    if not nome:
        nome = simpledialog.askstring("Fazer Pedido", "Digite o nome do produto:")
    produto = collection.find_one({"nome": nome})
    if produto:
        quantidade = simpledialog.askinteger("Fazer Pedido", "Digite a quantidade do produto:")
        if produto["quantidade"] >= quantidade:
            nova_quantidade = produto["quantidade"] - quantidade
            collection.update_one({"nome": nome}, {"$set": {"quantidade": nova_quantidade}})
            messagebox.showinfo("Sucesso", f"Pedido de {quantidade} {nome}(s) realizado com sucesso!")
            if nova_quantidade <= 6:
                messagebox.showwarning("Alerta de Estoque", "Estoque baixo! Recomendamos entrar em contato com um distribuidor.")
        else:
            messagebox.showerror("Erro", "Não há produtos suficientes em estoque")
    else:
        messagebox.showerror("Erro", "Produto não encontrado no estoque")

# Função para digitalizar código de barras e adicionar/consultar produto
def digitalizar_produto():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            nome = obj.data.decode('utf-8')
            produto = collection.find_one({"nome": nome})
            if produto:
                messagebox.showinfo("Produto Encontrado", f"O produto {nome} está em estoque com quantidade de {produto['quantidade']}")
            else:
                resposta = messagebox.askyesno("Produto Não Encontrado", "Produto não encontrado no estoque. Deseja adicionar este produto?")
                if resposta:
                    descricao = simpledialog.askstring("Adicionar Produto", "Digite a descrição do produto:")
                    preco = simpledialog.askfloat("Adicionar Produto", "Digite o preço do produto:")
                    quantidade = simpledialog.askinteger("Adicionar Produto", "Digite a quantidade do produto:")
                    produto = {"nome": nome, "descricao": descricao, "preco": preco, "quantidade": quantidade}
                    collection.insert_one(produto)
                    messagebox.showinfo("Sucesso", "Produto adicionado ao estoque com sucesso!")
            # Fechar a janela de digitalização após processar o código de barras
            cap.release()
            cv2.destroyAllWindows()
            return  # Sair da função após processar o código de barras
        cv2.imshow("Digitalizar Produto", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Função para mostrar o estoque em uma nova janela
def mostrar_estoque():
    estoque_window = tk.Toplevel()
    estoque_window.title("Estoque")
    
    # Tabela para exibir o estoque
    tree = ttk.Treeview(estoque_window, columns=("Nome", "Descrição", "Preço", "Quantidade"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Preço", text="Preço")
    tree.heading("Quantidade", text="Quantidade")
    tree.pack(fill=tk.BOTH, expand=True)

    # Botão para fazer pedido
    btn_fazer_pedido = tk.Button(estoque_window, text="Fazer Pedido", command=lambda: fazer_pedido(tree.item(tree.selection())['values'][0]), bg="lightgreen", fg="black")
    btn_fazer_pedido.pack(fill=tk.X, padx=20, pady=5)

    # Preencher a tabela com os produtos
    produtos = collection.find()
    for produto in produtos:
        tree.insert("", tk.END, values=(produto["nome"], produto["descricao"], produto["preco"], produto["quantidade"]))

    if collection.count_documents({}) == 0:
        messagebox.showinfo("Estoque", "O estoque está vazio.")

# Função principal para criar a interface gráfica
def criar_interface():
    root = tk.Tk()
    root.title("Sistema de Controle de Estoque")

    # Botões
    btn_adicionar = tk.Button(root, text="Adicionar Produto", command=adicionar_produto, bg="lightblue", fg="black")
    btn_adicionar.pack(fill=tk.X, padx=20, pady=5)

    btn_remover = tk.Button(root, text="Remover Produto", command=remover_produto, bg="lightcoral", fg="black")
    btn_remover.pack(fill=tk.X, padx=20, pady=5)

    btn_modificar = tk.Button(root, text="Modificar Produto", command=modificar_produto, bg="lightyellow", fg="black")
    btn_modificar.pack(fill=tk.X, padx=20, pady=5)

    btn_digitalizar = tk.Button(root, text="Digitalizar Produto", command=digitalizar_produto, bg="lightpink", fg="black")
    btn_digitalizar.pack(fill=tk.X, padx=20, pady=5)

    btn_mostrar_estoque = tk.Button(root, text="Mostrar Estoque", command=mostrar_estoque, bg="lightgreen", fg="black")
    btn_mostrar_estoque.pack(fill=tk.X, padx=20, pady=5)

    btn_sair = tk.Button(root, text="Sair", command=root.quit, bg="gray", fg="white")
    btn_sair.pack(fill=tk.X, padx=20, pady=5)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()