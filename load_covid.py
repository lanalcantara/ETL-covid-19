import pandas as pd
from sqlalchemy import create_engine

# --- Configurações ---
INPUT_FILE = "data/covid_transformado.csv"
# Definindo o banco de dados SQLite (será criado na pasta 'data/')
DATABASE_PATH = "data/covid.db"
TABLE_NAME = "covid_data"

def load_data(file_path: str, db_path: str, table_name: str):
    """
    Carrega o DataFrame limpo em um banco de dados SQLite.
    """
    print(f"1. Lendo dados transformados de: {file_path}")
    try:
        # Carrega o DataFrame
        df = pd.read_csv(file_path, parse_dates=['Data'])
        print(f"Dados lidos. Linhas: {len(df)}")
    except FileNotFoundError:
        print(f"ERRO: Arquivo {file_path} não encontrado. Execute a transformação primeiro.")
        return

    print(f"2. Conectando ao banco de dados SQLite e carregando...")
    
    # Cria uma conexão com o banco de dados SQLite
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Carrega o DataFrame em uma tabela SQL
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Carregamento concluído com sucesso!")
        print(f"Dados salvos na tabela '{table_name}' no arquivo '{db_path}'.")
    except Exception as e:
        print(f"ERRO durante o carregamento para o DB: {e}")

if __name__ == "__main__":
    load_data(INPUT_FILE, DATABASE_PATH, TABLE_NAME)