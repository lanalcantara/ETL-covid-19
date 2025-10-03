import pandas as pd

# 1. Carregar dados brutos
df = pd.read_csv("data/covid_bruto.csv")

print("Formato inicial:", df.shape)
print("Colunas:", df.columns.tolist())

# 2. Padronizar nomes das colunas
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# 3. Tratar valores nulos (exemplo: preencher com 0 onde for numérico)
for col in df.select_dtypes(include="number").columns:
    df[col] = df[col].fillna(0)

# 4. Converter datas (se houver colunas de data)
if "data" in df.columns:
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

# 5. Salvar CSV limpo
df.to_csv("data/covid_transformado.csv", index=False)

print("Transformação concluída! Arquivo salvo em data/covid_transformado.csv")
