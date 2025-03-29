import cv2
from pyzbar import pyzbar
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys

class SistemaEstoque:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.conectar_mongodb()
        
    def conectar_mongodb(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Testa a conexão
            self.db = self.client["estoque"]
            self.collection = self.db["produtos"]
            messagebox.showinfo("Sucesso", "Conectado ao MongoDB com sucesso!")
        except ConnectionFailure as e:
            messagebox.showerror("Erro de Conexão", 
                               f"Não foi possível conectar ao MongoDB:\n{str(e)}\n"
                               "Verifique se o MongoDB está rodando.")
            sys.exit(1)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            sys.exit(1)

    def validar_float(self, title, prompt):
        while True:
            valor = simpledialog.askstring(title, prompt)
            if valor is None:
                return None
            try:
                return float(valor)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, digite um valor numérico válido.")

    def validar_int(self, title, prompt):
        while True:
            valor = simpledialog.askstring(title, prompt)
            if valor is None:
                return None
            try:
                return int(valor)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, digite um número inteiro válido.")

    def adicionar_produto(self, nome=None):
        nome = nome or simpledialog.askstring("Adicionar Produto", "Digite o nome do produto:")
        if not nome:
            return
        
        descricao = simpledialog.askstring("Adicionar Produto", "Digite a descrição do produto:")
        preco = self.validar_float("Adicionar Produto", "Digite o preço do produto:")
        quantidade = self.validar_int("Adicionar Produto", "Digite a quantidade do produto:")
    
        if None in [descricao, preco, quantidade]:
            return
        
        produto = {
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "quantidade": quantidade
        }
        self.collection.insert_one(produto)
        messagebox.showinfo("Sucesso", "Produto adicionado ao estoque com sucesso!")
    
        if quantidade <= 6:
            messagebox.showwarning("Alerta", "Estoque baixo! Nível crítico.")

    def remover_produto(self):
        nome = simpledialog.askstring("Remover Produto", "Digite o nome do produto:")
        if not nome:
            return
            
        produto = self.collection.find_one({"nome": nome})
        if produto:
            self.collection.delete_one({"nome": nome})
            messagebox.showinfo("Sucesso", "Produto removido do estoque com sucesso!")
        else:
            messagebox.showerror("Erro", "Produto não encontrado no estoque")

    def modificar_produto(self, nome=None):
        nome = nome or simpledialog.askstring("Modificar Produto", "Digite o nome do produto:")
        if not nome:
            return
            
        produto = self.collection.find_one({"nome": nome})
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado no estoque")
            return

        nova_descricao = simpledialog.askstring(
            "Modificar Produto",
            f"Digite a nova descrição ({produto['descricao']}):",
            initialvalue=produto['descricao']
        )
        
        novo_preco = self.validar_float(
            "Modificar Produto",
            f"Digite o novo preço ({produto['preco']}):",
        )
        
        nova_quantidade = self.validar_int(
            "Modificar Produto",
            f"Digite a nova quantidade ({produto['quantidade']}):",
        )
        
        if None in [nova_descricao, novo_preco, nova_quantidade]:
            return
            
        self.collection.update_one(
            {"nome": nome},
            {"$set": {
                "descricao": nova_descricao,
                "preco": novo_preco,
                "quantidade": nova_quantidade
            }}
        )
        messagebox.showinfo("Sucesso", "Produto modificado com sucesso!")
        
        if nova_quantidade <= 6:
            messagebox.showwarning("Alerta", "Estoque baixo! Nível crítico.")

    def fazer_pedido(self, nome=None):
        if not nome:
            nome = simpledialog.askstring("Fazer Pedido", "Digite o nome do produto:")
            if not nome:
                return
                
        produto = self.collection.find_one({"nome": nome})
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado no estoque")
            return

        quantidade = self.validar_int("Fazer Pedido", "Digite a quantidade do produto:")
        if quantidade is None:
            return
            
        if produto["quantidade"] < quantidade:
            messagebox.showerror("Erro", "Não há produtos suficientes em estoque")
            return
            
        nova_quantidade = produto["quantidade"] - quantidade
        self.collection.update_one(
            {"nome": nome},
            {"$set": {"quantidade": nova_quantidade}}
        )
        messagebox.showinfo("Sucesso", f"Pedido de {quantidade} {nome}(s) realizado com sucesso!")
        
        if nova_quantidade <= 6:
            messagebox.showwarning("Alerta", "Estoque baixo! Nível crítico.")

    def digitalizar_produto(self):
        try:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                messagebox.showerror("Erro", "Não foi possível acessar a câmera")
                return
                
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                frame = cv2.resize(frame, (640, 480))
                
                try:
                    codes = pyzbar.decode(frame)
                    if codes:
                        code = codes[0].data.decode('utf-8')
                        cap.release()
                        cv2.destroyAllWindows()
                        self.processar_codigo(code)
                        return
                except Exception as e:
                    print(f"Erro ao decodificar: {str(e)}")
                
                cv2.imshow('Scanner de Código de Barras (Pressione Q para sair)', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def processar_codigo(self, codigo):
        produto = self.collection.find_one({"nome": codigo})
        if produto:
            resposta = messagebox.askyesno(
                "Produto Encontrado", 
                f"{produto['nome']}\n"
                f"Descrição: {produto['descricao']}\n"
                f"Preço: R${produto['preco']:.2f}\n"
                f"Estoque: {produto['quantidade']}\n\n"
                "Deseja modificar este produto?"
            )
            if resposta:
                self.modificar_produto(produto['nome'])
        else:
            if messagebox.askyesno("Novo Produto", "Produto não cadastrado. Deseja adicionar?"):
                self.adicionar_produto(codigo)

    def mostrar_estoque(self):
        estoque_window = tk.Toplevel()
        estoque_window.title("Estoque Atual")
        estoque_window.geometry("800x600")
        
        main_frame = ttk.Frame(estoque_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("Nome", "Descrição", "Preço", "Quantidade"),
            show="headings",
            selectmode="browse"
        )
        
        tree.heading("Nome", text="Nome")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Preço", text="Preço (R$)")
        tree.heading("Quantidade", text="Quantidade")
        
        tree.column("Nome", width=150)
        tree.column("Descrição", width=250)
        tree.column("Preço", width=100, anchor='e')
        tree.column("Quantidade", width=100, anchor='e')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        produtos = list(self.collection.find().sort("nome", 1))
        for produto in produtos:
            tree.insert(
                "",
                tk.END,
                values=(
                    produto["nome"],
                    produto["descricao"],
                    f"{produto['preco']:.2f}",
                    produto["quantidade"]
                )
            )
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="Fazer Pedido",
            command=lambda: self.fazer_pedido(tree.item(tree.selection())['values'][0] if tree.selection() else None
        ).pack(side=tk.LEFT, padx=5))
        
        ttk.Button(
            button_frame,
            text="Fechar",
            command=estoque_window.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def criar_interface(self):
        root = tk.Tk()
        root.title("Sistema de Controle de Estoque")
        root.geometry("400x500")
        
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10)
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        botoes = [
            ("➕ Adicionar Produto", lambda: self.adicionar_produto()),
            ("✖️ Remover Produto", self.remover_produto),
            ("✏️ Modificar Produto", self.modificar_produto),
            ("📷 Digitalizar Código", self.digitalizar_produto),
            ("📦 Consultar Estoque", self.mostrar_estoque),
            ("🚪 Sair", root.quit)
        ]
        
        for texto, comando in botoes:
            btn = ttk.Button(
                main_frame,
                text=texto,
                command=comando,
                style='TButton'
            )
            btn.pack(fill=tk.X, pady=5)
        
        root.mainloop()

if __name__ == "__main__":
    app = SistemaEstoque()
    app.criar_interface()