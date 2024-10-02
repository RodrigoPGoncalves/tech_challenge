import sqlite3
import pandas as pd


# Função para criar a tabela de dados com restrição de unicidade
def create_data_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dataset (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    age REAL,
                    gender TEXT,
                    education INTEGER,
                    introversion_score REAL,
                    sensing_score REAL,
                    thinking_score REAL,
                    judging_score REAL,
                    interest TEXT,
                    personality TEXT,
                    UNIQUE(age, gender, education, introversion_score, 
                           sensing_score, thinking_score, judging_score, 
                           interest, personality))''')
    conn.commit()
    conn.close()

# Função para adicionar dados a partir de um DataFrame
def add_data_from_dataframe(csv_file_path):
    df = pd.read_csv(csv_file_path)
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    for index, row in df.iterrows():
        age = row['Age']
        gender = row['Gender']
        education = row['Education']
        introversion_score = row['Introversion Score']
        sensing_score = row['Sensing Score']
        thinking_score = row['Thinking Score']
        judging_score = row['Judging Score']
        interest = row['Interest']
        personality = row['Personality']

        try:
            # Tenta inserir os dados na tabela
            c.execute('''INSERT INTO dataset (age, gender, education, introversion_score, 
                                                sensing_score, thinking_score, judging_score, 
                                                interest, personality) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (age, gender, education, introversion_score, 
                        sensing_score, thinking_score, judging_score, 
                        interest, personality))
        except sqlite3.IntegrityError:
            # Se a inserção falhar devido à duplicidade, ignora a linha
            #print(f'Dados duplicados encontrados e ignorados:')
            pass

    conn.commit()
    conn.close()

def display_data_info():
    conn = sqlite3.connect('data.db')
    
    # Consultar o número total de registros
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM dataset")
    total_records = c.fetchone()[0]
    
    print(f'Total de registros no banco de dados: {total_records}')
    
    # Carregar os dados em um DataFrame para visualizar as 5 primeiras linhas
    df = pd.read_sql_query("SELECT * FROM dataset", conn)
    
    print("\nAs 5 primeiras linhas da tabela:")
    print(df.head())

    conn.close()
    
def get_data_as_dataframe():
    conn = sqlite3.connect('data.db')
    df = pd.read_sql_query("SELECT * FROM dataset", conn)  # Consulta todos os dados da tabela
    conn.close()
    return df