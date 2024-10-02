import sqlite3
import hashlib

# Função para criar a tabela de usuários
def create_user_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Função para cadastrar um novo usuário
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    password_hashed = hashlib.sha256(password.encode()).hexdigest()  # Hash da senha
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hashed))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Retorna False se o usuário já existir
    conn.close()
    return True

# Função para verificar login
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    password_hashed = hashlib.sha256(password.encode()).hexdigest()  # Hash da senha
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hashed))
    result = c.fetchone()
    conn.close()
    return result  
