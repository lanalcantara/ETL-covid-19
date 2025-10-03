import pandas as pd
import numpy as np
from pathlib import Path

# --- Configurações ---
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INDIC_FILE = RAW_DIR / "indicadores_completo.csv"
COVID_FILE = PROCESSED_DIR / "covid_completo.csv"
OUTPUT_FILE = PROCESSED_DIR / "analise_final.csv"

# --- Países que serão usados ---
COUNTRIES = [
    "Brazil","United States","India","China",
    "United Kingdom","Germany","France",
    "South Africa","Mexico"
]

# --- Parâmetros de geração sintética ---
BASE_NEW_CASES = {
    "United States": 60000, "Brazil": 45000, "India": 40000,
    "China": 2000, "United Kingdom": 15000, "Germany": 12000,
    "France": 11000, "South Africa": 7000, "Mexico": 8000
}

CFR = {  # case fatality rate estimado
    "United States": 0.015, "Brazil": 0.02, "India": 0.01,
    "China": 0.005, "United Kingdom": 0.017, "Germany": 0.014,
    "France": 0.016, "South Africa": 0.018, "Mexico": 0.02
}

def generate_covid_data():
    dates = pd.date_range(start="2020-01-01", end="2021-12-31", freq="D")
    rows = []
    np.random.seed(42)

    for country in COUNTRIES:
        base = BASE_NEW_CASES.get(country, 1000)
        t = np.arange(len(dates))
        # duas ondas (2020 e 2021)
        center1 = (pd.to_datetime("2020-08-01") - dates[0]).days
        center2 = (pd.to_datetime("2021-06-15") - dates[0]).days
        sigma1, sigma2 = 60, 70

        wave1 = np.exp(-0.5 * ((t - center1) / sigma1)**2)
        wave2 = np.exp(-0.5 * ((t - center2) / sigma2)**2)
        seasonal = 1 + 0.1 * np.sin(2 * np.pi * t / 180)
        noise = np.random.normal(0, 0.2, size=len(dates))

        new_cases = base * (0.1 + 2.5*wave1 + 3.0*wave2) * seasonal * (1 + noise)
        new_cases = np.clip(new_cases, 0, None).round().astype(int)

        new_deaths = (new_cases * CFR.get(country, 0.01)).round().astype(int)
        cum_cases = np.cumsum(new_cases)
        cum_deaths = np.cumsum(new_deaths)

        for date, c_cases, c_deaths, n_cases in zip(dates, cum_cases, cum_deaths, new_cases):
            rows.append({
                "country": country,
                "date": date,
                "cases": int(c_cases),
                "deaths": int(c_deaths),
                "new_cases": int(n_cases)
            })

    return pd.DataFrame(rows)

def transform_and_merge(df_covid, df_ind):
    df_covid = df_covid.sort_values(["country","date"]).reset_index(drop=True)

    # crescimento diário (%)
    df_covid["cases_prev"] = df_covid.groupby("country")["cases"].shift(1)
    df_covid["growth_rate_pct"] = ((df_covid["cases"] - df_covid["cases_prev"]) /
                                   df_covid["cases_prev"]).replace([np.inf,-np.inf], np.nan) * 100
    df_covid["growth_rate_pct"] = df_covid["growth_rate_pct"].fillna(0)

    # média móvel 7 dias
    df_covid["ma7_new_cases"] = df_covid.groupby("country")["new_cases"] \
        .rolling(window=7, min_periods=1).mean().reset_index(level=0, drop=True)

    # merge com indicadores
    df_covid["year"] = df_covid["date"].dt.year
    df_ind["year"] = pd.to_datetime(df_ind["date"]).dt.year
    df_final = pd.merge(df_covid, df_ind.drop(columns=["date"]), on=["country","year"], how="left")

    # organizar colunas
    cols = ["country","date","year","cases","deaths","new_cases",
            "growth_rate_pct","ma7_new_cases",
            "gdp","unemployment_rate","poverty_rate",
            "health_spending_gdp","life_expectancy","education_index"]
    for c in cols:
        if c not in df_final.columns:
            df_final[c] = None

    return df_final[cols]

if __name__ == "__main__":
    print("📥 Gerando dados COVID sintéticos...")
    df_covid = generate_covid_data()
    df_covid.to_csv(COVID_FILE, index=False)
    print(f"✅ covid_completo salvo em {COVID_FILE}")

    print("📥 Lendo indicadores...")
    df_ind = pd.read_csv(INDIC_FILE)

    print("🔄 Transformando e unindo dados...")
    df_final = transform_and_merge(df_covid, df_ind)

    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ analise_final salvo em {OUTPUT_FILE} ({len(df_final)} linhas)")
