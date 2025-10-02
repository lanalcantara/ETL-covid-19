import pandas as pd
import numpy as np

# --- Configurações de Arquivo ---
COVID_FILE = "data/covid_transformado.csv"
WB_FILE = "data/worldbank_bruto.csv"
FINAL_FILE = "data/base_final_analise.csv"

# Mapeamento para corrigir incompatibilidades de nomes de países
# Ex: O Banco Mundial pode chamar um país diferente da API COVID-19.
# Adicione mais correções conforme necessário se a mesclagem não funcionar perfeitamente.
COUNTRY_NAME_MAPPING = {
    "Congo (Brazzaville)": "Congo, Rep.",
    "Congo (Kinshasa)": "Congo, Dem. Rep.",
    "Egypt": "Egypt, Arab Rep.",
    "Iran": "Iran, Islamic Rep.",
    "Slovak Republic": "Slovakia",
    "Korea, South": "Korea, Rep.",
    "Russian Federation": "Russia",
    "United Kingdom": "United Kingdom", # Adicionado para garantir que UK esteja na lista
    "United States": "United States",    # Adicionado para garantir que US esteja na lista
    # Adicione aqui mais correções se o join resultar em muitos 'NaN'
}


def load_data(covid_file: str, wb_file: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega os dois dataframes."""
    print("1. Carregando datasets...")
    try:
        df_covid = pd.read_csv(covid_file, parse_dates=['Data'])
        print(f"   -> COVID-19: {len(df_covid)} linhas carregadas.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo {covid_file} não encontrado.")
        df_covid = pd.DataFrame()

    try:
        df_wb = pd.read_csv(wb_file)
        print(f"   -> Banco Mundial: {len(df_wb)} linhas carregadas.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo {wb_file} não encontrado.")
        df_wb = pd.DataFrame()
        
    return df_covid, df_wb


def merge_and_finalize(df_covid: pd.DataFrame, df_wb: pd.DataFrame) -> pd.DataFrame:
    """Aplica a padronização e realiza a mesclagem."""
    if df_covid.empty or df_wb.empty:
        return pd.DataFrame()

    print("2. Aplicando Padronização e Mesclagem...")

    # --- 2.1 Padronização de Chaves (País) ---
    
    # Padroniza os nomes de países no dataset COVID-19 usando o mapeamento
    # O .map() tenta usar o valor do dicionário; se não encontrar a chave, mantém o nome original
    df_covid['Pais_Padrao'] = df_covid['Pais'].map(COUNTRY_NAME_MAPPING).fillna(df_covid['Pais'])
    
    # Padroniza os nomes de países no dataset do Banco Mundial (usando o 'Pais' original do WB)
    # Aqui vamos criar uma coluna para o 'Pais' do WB que corresponda ao do COVID-19.
    # Como o nosso mapeamento está focado em como a API COVID-19 chama o país,
    # vamos usar a coluna 'Pais' do WB (que já é mais padronizada) como chave principal.
    df_wb['Pais_Padrao'] = df_wb['Pais'] 
    
    # Renomeia as colunas de indicadores do WB para facilitar o join
    wb_cols = [col for col in df_wb.columns if col in ['Populacao_Total', 'PIB_Per_Capita', 'Expectativa_Vida']]
    
    # Seleciona apenas as colunas WB de que precisamos (País, ID, Ano e Indicadores)
    df_wb_final = df_wb[['Pais_Padrao', 'Pais_ID'] + wb_cols].drop_duplicates(subset=['Pais_Padrao'])

    # --- 2.2 Mesclagem (JOIN) ---
    
    # Mescla (JOIN) os dados. Usamos 'left' para manter todas as linhas da COVID-19
    # e adicionar os indicadores econômicos quando houver correspondência.
    df_final = pd.merge(
        df_covid, 
        df_wb_final, 
        on='Pais_Padrao', 
        how='left'
    )
    
    # Limpeza final: remove a coluna de padronização temporária
    df_final = df_final.drop(columns=['Pais_Padrao'])
    
    # Verificação de sucesso do JOIN
    total_linhas = len(df_final)
    total_com_indicadores = df_final['Populacao_Total'].count()
    
    print(f"   -> Mesclagem concluída. Total de linhas: {total_linhas}")
    print(f"   -> Linhas com indicadores do Banco Mundial: {total_com_indicadores} ({(total_com_indicadores/total_linhas*100):.2f}%)")
    
    return df_final


def save_deliverable(df: pd.DataFrame, file_path: str):
    """Salva o DataFrame final."""
    if df.empty:
        print("Nenhum dado para salvar.")
        return

    print(f"3. Salvando base de análise final em: {file_path}")
    df.to_csv(file_path, index=False, encoding='utf-8')
    print("Junção de datasets concluída com sucesso!")


if __name__ == "__main__":
    df_covid, df_wb = load_data(COVID_FILE, WB_FILE)
    df_final = merge_and_finalize(df_covid, df_wb)
    save_deliverable(df_final, FINAL_FILE)