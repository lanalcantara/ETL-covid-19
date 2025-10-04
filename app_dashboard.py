import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Dashboard COVID")

st.title("📊 Dashboard COVID-19")

# 1. Carregar dados
df = pd.read_csv("data/base_final_analise.csv")
df["periodo"] = pd.to_datetime(df["periodo"])

# 2. Filtros na barra lateral
paises = sorted(df["pais"].unique())
pais = st.sidebar.selectbox("Selecione o país", options=paises)

# Filtrar dataset
df_sel = df[df["pais"] == pais]

# 3. Gráfico de casos confirmados ao longo do tempo
st.subheader(f"Casos Confirmados – {pais}")
chart_casos = alt.Chart(df_sel).mark_line(color="blue").encode(
    x="periodo:T",
    y="casos_confirmados:Q"
)
st.altair_chart(chart_casos, use_container_width=True)

# 4. Gráfico de óbitos ao longo do tempo
st.subheader(f"Óbitos – {pais}")
chart_obitos = alt.Chart(df_sel).mark_line(color="red").encode(
    x="periodo:T",
    y="obitos:Q"
)
st.altair_chart(chart_obitos, use_container_width=True)

# 5. Tabela resumo
st.subheader("Resumo por período")
st.dataframe(df_sel)
