import requests
import pandas as pd
from datetime import datetime

print(">>> O script de extração começou a rodar! <<<")

# --- Configurações ---
# Endpoint para obter o histórico de todos os países (desde o início)
API_URL = "https://disease.sh/v3/covid-19/historical?lastdays=all"
OUTPUT_FILE = "data/covid_bruto.csv"

def extract_data(url: str) -> list:
    """Faz a chamada da API e retorna a lista de dados brutos."""
    print(f"1. Extraindo dados da API: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status() # Lança exceção para status codes 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na extração de dados: {e}")
        return []

def process_and_transform(data: list) -> pd.DataFrame:
    """
    Processa a resposta JSON, calcula variações diárias e padroniza o DataFrame.
    """
    if not data:
        return pd.DataFrame()

    print("2. Processando e transformando dados...")
    
    # Lista para armazenar as linhas do DataFrame final
    records = []
    
    # Itera sobre cada país na lista de dados brutos
    for country_data in data:
        country = country_data.get('country')
        # A API retorna um dicionário para 'timeline' com chaves 'cases', 'deaths', 'recovered'
        timeline = country_data.get('timeline', {})
        
        # Pega as séries temporais (datas e valores acumulados)
        cases = timeline.get('cases', {})
        deaths = timeline.get('deaths', {})
        recovered = timeline.get('recovered', {})

        # Pega todas as datas únicas que aparecem (chaves dos dicionários)
        all_dates = sorted(set(cases.keys()) | set(deaths.keys()) | set(recovered.keys()), 
                           key=lambda x: datetime.strptime(x, '%m/%d/%y'))

        # Inicializa as variáveis para cálculo diário
        prev_cases, prev_deaths, prev_recovered = 0, 0, 0

        for date_str in all_dates:
            # Converte a data para o formato padronizado (AAAA-MM-DD)
            date_obj = datetime.strptime(date_str, '%m/%d/%y')
            standard_date = date_obj.strftime('%Y-%m-%d')
            
            # Pega valores acumulados (ou 0 se não existirem para aquela data)
            total_cases = cases.get(date_str, 0)
            total_deaths = deaths.get(date_str, 0)
            total_recovered = recovered.get(date_str, 0)
            
            # --- Limpeza Preliminar: Cálculo Diário ---
            # Calcula novos casos/mortes/recuperados (variação diária)
            new_cases = total_cases - prev_cases if total_cases >= prev_cases else 0
            new_deaths = total_deaths - prev_deaths if total_deaths >= prev_deaths else 0
            new_recovered = total_recovered - prev_recovered if total_recovered >= prev_recovered else 0

            # Adiciona o registro à lista
            records.append({
                'Pais': country,
                'Data': standard_date,
                'Casos_Total': total_cases,
                'Mortes_Total': total_deaths,
                'Recuperados_Total': total_recovered,
                'Novos_Casos': new_cases,
                'Novas_Mortes': new_deaths,
                'Novos_Recuperados': new_recovered
            })
            
            # Atualiza os valores anteriores para a próxima iteração
            prev_cases = total_cases
            prev_deaths = total_deaths
            prev_recovered = total_recovered

    # Cria e retorna o DataFrame
    df = pd.DataFrame(records)
    print(f"Dados processados. Linhas: {len(df)}")
    return df

def save_deliverable(df: pd.DataFrame, file_path: str):
    """Salva o DataFrame como um arquivo CSV."""
    if df.empty:
        print("Nenhum dado para salvar.")
        return

    print(f"3. Salvando dados em: {file_path}")
    # Salva com o índice falso para evitar coluna extra no CSV
    df.to_csv(file_path, index=False, encoding='utf-8')
    print("Extração concluída com sucesso!")


if __name__ == "__main__":
    # 1. Extrair os dados da API
    raw_data = extract_data(API_URL)
    
    # 2. Processar, transformar e calcular diários
    final_df = process_and_transform(raw_data)
    
    # 3. Salvar o entregável
    save_deliverable(final_df, OUTPUT_FILE)