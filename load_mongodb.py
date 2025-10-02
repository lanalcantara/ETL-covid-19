import pandas as pd
from pymongo import MongoClient
import json
import numpy as np

# --- Configurações de Conexão e Arquivos ---
MONGO_URI = "mongodb+srv://lana_covid19_user:centralizados@cluster0.ssgnfdi.mongodb.net/"
DB_NAME = "covid_etl_db"
COLLECTION_NAME = "dados_analise_final"
INPUT_FILE = "data/base_final_analise.csv"

def load_to_mongodb(file_path: str, uri: str, db_name: str, collection_name: str):
    """
    Lê o CSV final, converte para formato JSON e carrega no MongoDB.
    """
    print(f"1. Lendo base de análise final de: {file_path}")
    try:
        # Carrega o DataFrame
        df = pd.read_csv(file_path, parse_dates=['Data'])
        print(f"Dados lidos. Linhas: {len(df)}")
    except FileNotFoundError:
        print(f"ERRO: Arquivo {file_path} não encontrado.")
        return

    print(f"2. Conectando ao MongoDB e carregando para a coleção '{collection_name}'...")
    
    # Converte tipos não nativos do JSON (como NaNs) para None
    df = df.replace({np.nan: None})
    
    # Converte o DataFrame para uma lista de dicionários (formato de documentos MongoDB)
    data_json = df.to_dict('records')
    
    try:
        # 3. Conexão e Carregamento
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        
        # Limpa a coleção antiga antes de carregar (opcional, mas bom para ETL)
        collection.drop()
        
        # Insere todos os documentos
        collection.insert_many(data_json)
        
        print(f"Carregamento concluído com sucesso!")
        print(f"Total de documentos carregados: {collection.count_documents({})}")
        
        client.close()
        
    except Exception as e:
        print(f"ERRO durante o carregamento para o MongoDB. Verifique a URI e a conexão (VPN/Firewall): {e}")

if __name__ == "__main__":
    # Importante: Substitua a URI pela sua conexão real antes de rodar!
    load_to_mongodb(INPUT_FILE, MONGO_URI, DB_NAME, COLLECTION_NAME)