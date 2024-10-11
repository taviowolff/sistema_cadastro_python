import tkinter as tk
from tkinter import ttk, messagebox
from database import adicionar_item, remover_todos_itens, remover_item_por_id, conectar_db

def adicionar_item_interface():
    nome = entry_nome.get()
    categoria = entry_categoria.get()
    quantidade = int(entry_quantidade.get())
    localizacao = entry_localizacao.get()
    descricao = entry_descricao.get()

    adicionar_item(nome, categoria, quantidade, localizacao, descricao)
    messagebox.showinfo("Sucesso", "Item adicionado com sucesso")
    limpar_campos()
    atualizar_lista()  # Atualiza a lista após adicionar

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_localizacao.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)

def atualizar_lista():
    # Remove todos os itens atuais da Treeview
    for row in tree.get_children():
        tree.delete(row)
    
    # Conectar ao banco de dados e buscar todos os itens
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM itens')
    rows = cursor.fetchall()
    conn.close()

    # Inserir cada item na Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

def remover_todos():
    confirmar = messagebox.askyesno("Confirmação", "Você realmente deseja remover todos os itens?")
    if confirmar:
        remover_todos_itens()
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Todos os itens foram removidos!")

def remover_selecionado():
    try:
        item_selecionado = tree.selection()[0]
        item_id = tree.item(item_selecionado, 'values')[0]
        remover_item_por_id(item_id)
        tree.delete(item_selecionado)  # Remove da Treeview
        messagebox.showinfo("Sucesso", "Item removido com sucesso!")
    except IndexError:
        messagebox.showwarning("Erro", "Nenhum item selecionado")

def criar_interface():
    global entry_nome, entry_categoria, entry_quantidade, entry_localizacao, entry_descricao, tree

    janela = tk.Tk()
    janela.title('Inventário Doméstico')

    # Definir o tamanho da janela
    janela.geometry('620x550')

    # Tema escuro
    janela.configure(bg='#2E2E2E')  # Cor de fundo escura da janela

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#333333",  # Cor de fundo da Treeview
                    foreground="white",  # Cor de texto
                    fieldbackground="#333333",  # Cor de fundo para campos de entrada
                    bordercolor="#4D4D4D",  # Cor da borda
                    rowheight=25)

    # Widgets de entrada
    tk.Label(janela, text='Nome do Item').grid(row=0, column=0, sticky='w', padx=10, pady=5)
    entry_nome = tk.Entry(janela)
    entry_nome.grid(row=0, column=0, padx=10, pady=5)

    tk.Label(janela, text='Categoria').grid(row=1, column=0, sticky='w', padx=10, pady=5)
    entry_categoria = tk.Entry(janela)
    entry_categoria.grid(row=1, column=0, padx=10, pady=5)

    tk.Label(janela, text='Quantidade').grid(row=2, column=0, sticky='w', padx=10, pady=5)
    entry_quantidade = tk.Entry(janela)
    entry_quantidade.grid(row=2, column=0, padx=10, pady=5)

    tk.Label(janela, text='Localização').grid(row=3, column=0, sticky='w', padx=10, pady=5)
    entry_localizacao = tk.Entry(janela)
    entry_localizacao.grid(row=3, column=0, padx=10, pady=5)

    tk.Label(janela, text='Descrição').grid(row=4, column=0, sticky='w', padx=10, pady=5)
    entry_descricao = tk.Entry(janela)
    entry_descricao.grid(row=4, column=0, padx=10, pady=5)

    # Botão para adicionar item
    btn_adicionar = tk.Button(janela, text='Adicionar Item', command=adicionar_item_interface)
    btn_adicionar.grid(row=2, column=1, sticky='w', padx=10, pady=5)

    # Botões para remover itens
    btn_remover_selecionado = tk.Button(janela, text='Remover Selec', command=remover_selecionado)
    btn_remover_selecionado.grid(row=3, column=1, sticky='w', padx=10, pady=5)

    btn_remover_todos = tk.Button(janela, text='Remover Todos', command=remover_todos)
    btn_remover_todos.grid(row=4, column=1, sticky='w', padx=10, pady=5)

    # Treeview para exibir os itens
    columns = ('ID', 'Nome', 'Categoria', 'Quantidade', 'Localização', 'Descrição')
    tree = ttk.Treeview(janela, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)  # Definir a largura de cada coluna

    tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    # Atualizar a lista de itens ao iniciar a interface
    atualizar_lista()

    janela.mainloop()
