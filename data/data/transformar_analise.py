import pandas as pd

# 1. Carregar base transformada
df = pd.read_csv("data/covid_transformado.csv")

# 2. Garantir formato de data
if "data" in df.columns:
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

# 3. Criar coluna de período (mês/ano)
df["periodo"] = df["data"].dt.to_period("M").dt.to_timestamp()

# 4. Agregar por período e país (ou região/bairro, se houver coluna correspondente)
agg = df.groupby(["periodo", "pais"]).agg({
    "casos_confirmados": "sum",
    "obitos": "sum"
}).reset_index()

# 5. Salvar tabela final
agg.to_csv("data/base_final_analise.csv", index=False)

print("✅ Agregação concluída! Arquivo salvo em data/base_final_analise.csv")
