import wbgapi as wb
import pandas as pd
from datetime import datetime

# --- Configurações ---
OUTPUT_FILE = "data/worldbank_bruto.csv"

# Indicadores do Banco Mundial a serem extraídos
INDICATORS = {
    'SP.POP.TOTL': 'Populacao_Total',
    'NY.GDP.PCAP.CD': 'PIB_Per_Capita',
    'SP.DYN.LE00.IN': 'Expectativa_Vida',
}

# Período de extração (Focando nos anos mais recentes disponíveis)
YEARS = 2021 

def extract_worldbank_data() -> pd.DataFrame:
    """
    Extrai dados de múltiplos indicadores do Banco Mundial,
    garante que os países são padronizados e salva o resultado.
    """
    print(f"1. Extraindo dados do Banco Mundial para o ano de {YEARS}...")
    
    # Lista para armazenar os DataFrames de cada indicador
    dfs = []
    
    # Itera sobre cada indicador
    for code, name in INDICATORS.items():
        print(f"   -> Buscando indicador: {name} ({code})")
        
        # Faz a requisição e retorna um DataFrame
        df_indicador = wb.data.DataFrame(
            code, 
            time=YEARS, 
            labels=True, 
            index='economy' # Define o código do país como índice
        ).reset_index()

        # ----------------------------------------------------
        # CORREÇÃO DO KEYERROR: Lógica robusta de renomeação de colunas
        # ----------------------------------------------------
        
        # 1. Mapeamento base das colunas
        rename_map = {
            'economy': 'Pais_ID', 
            code: name           
        }
        
        # 2. Renomeia a coluna de tempo (se ela existir)
        # O nome é geralmente 'Time' quando labels=True.
        if 'Time' in df_indicador.columns:
            rename_map['Time'] = 'Ano_Referencia'
        
        # Renomeia as colunas
        df_indicador = df_indicador.rename(columns=rename_map)
        
        # 3. Garante que 'Ano_Referencia' existe (cria se a API não retornou a coluna de tempo)
        if 'Ano_Referencia' not in df_indicador.columns:
             df_indicador['Ano_Referencia'] = str(YEARS) 
             
        # 4. Define a lista de colunas para seleção final
        cols_to_select = ['Pais_ID', 'Country', 'Ano_Referencia', name]
        
        # 5. Seleciona e limpa
        df_indicador = df_indicador[cols_to_select].copy()
        df_indicador = df_indicador.dropna(subset=[name])
        
        dfs.append(df_indicador)

    # 2. Mesclar e Padronizar os Dados
    print("2. Mesclando dados dos indicadores...")
    
    # Faz um merge de todos os DataFrames (mescla por país e ano)
    df_final = dfs[0].copy()
    for df in dfs[1:]:
        df_final = pd.merge(df_final, df, on=['Pais_ID', 'Country', 'Ano_Referencia'], how='outer')

    # Renomeia o país para consistência
    df_final = df_final.rename(columns={'Country': 'Pais'})
    
    # Seleciona as colunas finais
    df_final = df_final[['Pais', 'Pais_ID', 'Ano_Referencia'] + list(INDICATORS.values())]
    
    print(f"Dados do Banco Mundial processados. Linhas: {len(df_final)}")
    return df_final

def save_deliverable(df: pd.DataFrame, file_path: str):
    """Salva o DataFrame como um arquivo CSV."""
    if df.empty:
        print("Nenhum dado do Banco Mundial para salvar.")
        return

    print(f"3. Salvando dados em: {file_path}")
    df.to_csv(file_path, index=False, encoding='utf-8')
    print("Extração do Banco Mundial concluída com sucesso!")


if __name__ == "__main__":
    df_worldbank = extract_worldbank_data()
    save_deliverable(df_worldbank, OUTPUT_FILE)