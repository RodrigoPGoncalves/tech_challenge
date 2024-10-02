import streamlit as st
import sqlite3
import hashlib
import db.db_users as dbUser
import db.db_data as dbData
from datetime import datetime, timedelta
from streamlitPages.page1 import app as page1_app
from streamlitPages.page2 import app as page2_app
from streamlitPages.page3 import app as page3_app

# Criar a tabela de usuários e data no SQLite
dbUser.create_user_table()
dbData.create_data_table()

# Função para autenticar o usuário
def authenticate_user(username, password):
    return dbUser.login_user(username, password)

# Função para definir um hash de senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = None

def main():
    st.title("Analise de Personalidade")
    if not st.session_state.logged_in:
        # Menu de navegação
        menu = ["Login", "Cadastro"]
        choice = st.sidebar.selectbox("Escolha", menu)
        
        if choice == "Login":
            st.subheader("Login")
            
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")

            if st.button("Login"):
                user = authenticate_user(username, password)
                if user:
                    st.success(f"Bem-vindo, {username}!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.last_activity = datetime.now()  # Armazena a hora do login
                    st.rerun()
                    
                else:
                    st.error("Nome de usuário ou senha incorretos")

        elif choice == "Cadastro":
            st.subheader("Cadastro")

            new_username = st.text_input("Novo Usuário")
            new_password = st.text_input("Nova Senha", type="password")

            if st.button("Cadastrar"):
                if dbUser.add_user(new_username, new_password):
                    st.success("Usuário cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário já existe. Escolha outro nome de usuário.")
    else:
        current_time = datetime.now()
        last_activity = st.session_state.last_activity

        # Checa se o tempo de sessão excedeu 30 minutos
        if (current_time - last_activity) > timedelta(minutes=30):
            st.warning("Sessão expirada. Por favor, faça login novamente.")
            st.session_state.logged_in = False
        else:
            st.session_state.last_activity = current_time  # Atualiza a última atividade
            #st.success("Sessão ativa!")

            # Navegação para páginas após o login
            st.sidebar.header(f"Bem-vindo, {st.session_state.username}!")
            selection = st.sidebar.selectbox("Escolha uma página", ["Testando o Modelo", "Analisando os Dados", "Modelagem"])

            # Carregar a página selecionada
            if selection == "Testando o Modelo":
                page1_app()
            elif selection == "Analisando os Dados":
                page2_app()
            elif selection == "Modelagem":
                page3_app()

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.success("Você foi desconectado.")
            st.rerun()

if __name__ == '__main__':
    main()
