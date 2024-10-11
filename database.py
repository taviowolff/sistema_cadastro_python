import sqlite3

def conectar_db():
    return sqlite3.connect('inventario.db')

def criar_tabela():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            localizacao TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_item(nome, categoria, quantidade, localizacao, descricao):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO itens (nome, categoria, quantidade, localizacao, descricao)
        VALUES (?, ?, ?, ?, ?)''',
        (nome, categoria, quantidade, localizacao, descricao)
    )
    conn.commit()
    conn.close()

def remover_todos_itens():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM itens')
    conn.commit()
    conn.close()

def remover_item_por_id(item_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM itens WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
