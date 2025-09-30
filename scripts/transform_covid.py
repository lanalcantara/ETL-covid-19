import pandas as pd

# --- Configurações ---
INPUT_FILE = "data/covid_bruto.csv"
OUTPUT_FILE = "data/covid_transformado.csv"

def load_data(file_path: str) -> pd.DataFrame:
    """Carrega o DataFrame bruto, garantindo a tipagem da coluna 'Data'."""
    print(f"1. Carregando dados brutos de: {file_path}")
    try:
        # Carrega o CSV e garante que a coluna 'Data' é do tipo datetime
        df = pd.read_csv(file_path, parse_dates=['Data'])
        print(f"Dados brutos carregados. Linhas: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"ERRO: Arquivo {file_path} não encontrado. Execute a extração primeiro.")
        return pd.DataFrame()

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica regras de limpeza, padronização e cria colunas de agregação."""
    if df.empty:
        return df

    print("2. Aplicando transformações e limpeza...")
    
    # 2.1 Tratamento de Valores Faltantes (NaN) e Ajuste de Tipos
    
    # Colunas que devem ser inteiras (não podem ter valores flutuantes/decimais)
    integer_cols = [
        'Casos_Total', 'Mortes_Total', 'Recuperados_Total',
        'Novos_Casos', 'Novas_Mortes', 'Novos_Recuperados'
    ]
    
    # Preenche valores NaN nessas colunas com 0 (assumindo que NaN significa 0 casos/mortes)
    df[integer_cols] = df[integer_cols].fillna(0)
    
    # Converte as colunas para o tipo inteiro (int), após o tratamento de NaN
    # Usamos pd.Int64Dtype() para lidar com valores grandes e permitir NaN temporariamente
    for col in integer_cols:
         df[col] = df[col].astype('Int64')

    # 2.2 Filtragem de Dados (Remover Ruídos)
    
    # Remover linhas onde novos casos ou mortes são negativos.
    # Isso geralmente é um artefato da fonte de dados (correção de relatórios passados).
    initial_rows = len(df)
    df = df[
        (df['Novos_Casos'] >= 0) & 
        (df['Novas_Mortes'] >= 0) &
        (df['Novos_Recuperados'] >= 0)
    ]
    removed_rows = initial_rows - len(df)
    if removed_rows > 0:
        print(f"   -> {removed_rows} linhas removidas devido a valores diários negativos.")

    # 2.3 Criação de Colunas de Agregação e Análise
    
    # Casos Ativos (Total - Mortes - Recuperados)
    # É importante usar .clip(lower=0) pois o cálculo pode resultar em negativos em dados brutos.
    df['Casos_Ativos'] = (df['Casos_Total'] - df['Mortes_Total'] - df['Recuperados_Total']).clip(lower=0)
    
    # Taxa de Mortalidade (Mortes Totais / Casos Totais) - Expressa em %
    # Usamos .replace(0, pd.NA) para evitar divisão por zero em Casos_Total = 0
    df['Taxa_Mortalidade (%)'] = (
        (df['Mortes_Total'] / df['Casos_Total'].replace(0, pd.NA)) * 100
    )
    
    print(f"Transformação concluída. Linhas finais: {len(df)}")
    return df

def save_deliverable(df: pd.DataFrame, file_path: str):
    """Salva o DataFrame transformado."""
    if df.empty:
        print("Nenhum dado para salvar.")
        return

    print(f"3. Salvando dados limpos em: {file_path}")
    df.to_csv(file_path, index=False, encoding='utf-8')
    print("Transformação concluída com sucesso!")


if __name__ == "__main__":
    # 1. Carregar
    df_bruto = load_data(INPUT_FILE)
    
    # 2. Transformar
    df_transformado = transform_data(df_bruto)
    
    # 3. Salvar
    save_deliverable(df_transformado, OUTPUT_FILE)