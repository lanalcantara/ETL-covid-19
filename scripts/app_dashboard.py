import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Dashboard COVID")

<<<<<<< HEAD
st.title("📊 Análise Integrada: COVID-19 e Indicadores Globais")

# 1. Carregar dados
# **IMPORTANTE:** Assumindo que o nome da coluna de tempo é 'Periodo' (com P maiúsculo)
df = pd.read_csv("data/base_final_analise.csv")

# CORREÇÃO DO KEYERROR: Alterando 'periodo' para 'Periodo' ou outro nome correto
# Se 'Periodo' não for o nome correto, substitua por aquele que você encontrou no CSV!
df["Periodo"] = pd.to_datetime(df["Periodo"]) 

# Limpeza e preparo para análise de correlação
df.columns = df.columns.str.lower() # Padroniza todas as colunas para minúsculo
=======
st.title("📊 Dashboard COVID-19")

# 1. Carregar dados
df = pd.read_csv("data/base_final_analise.csv")
df["periodo"] = pd.to_datetime(df["periodo"])
>>>>>>> a019aa29b526f81ccda577d52c06fe132923200c

# 2. Filtros na barra lateral
paises = sorted(df["pais"].unique())
pais = st.sidebar.selectbox("Selecione o país", options=paises)

# Filtrar dataset
df_sel = df[df["pais"] == pais]

<<<<<<< HEAD
st.header(f"País Selecionado: {pais}")
st.markdown("---")


# === SEÇÃO 1: TENDÊNCIAS TEMPORAIS (COVID) ===

col1, col2 = st.columns(2)

# 3. Gráfico de casos confirmados ao longo do tempo
with col1:
    st.subheader("Casos Confirmados (Tendência)")
    # Note: Estou usando o nome 'periodo' aqui porque padronizei na linha 15 (df.columns.str.lower())
    chart_casos = alt.Chart(df_sel).mark_line(color="blue").encode(
        x=alt.X("periodo:T", title="Data"),
        y=alt.Y("casos_confirmados:Q", title="Casos Confirmados")
    ).interactive()
    st.altair_chart(chart_casos, use_container_width=True)

# 4. Gráfico de óbitos ao longo do tempo
with col2:
    st.subheader("Óbitos (Tendência)")
    chart_obitos = alt.Chart(df_sel).mark_line(color="red").encode(
        x=alt.X("periodo:T", title="Data"),
        y=alt.Y("obitos:Q", title="Óbitos")
    ).interactive()
    st.altair_chart(chart_obitos, use_container_width=True)


# === SEÇÃO 2: ANÁLISE SOCIOECONÔMICA (KPI CRÍTICO) ===
st.markdown("---")
st.header("Análise de Impacto Socioeconômico Global")

# Encontrar o PIB per capita e a taxa de mortalidade final
# **ATENÇÃO: Você deve substituir 'pib_per_capita' e 'taxa_mortalidade' pelos nomes reais das colunas no seu CSV!**
df_agregado = df.groupby('pais').agg({
    'pib_per_capita': 'mean',
    'taxa_mortalidade': 'max' # Usamos o máximo para pegar o indicador final
}).reset_index().dropna()

st.subheader("PIB Per Capita vs. Taxa de Mortalidade")

# Gráfico de Dispersão (Scatter Plot)
scatter_chart = alt.Chart(df_agregado).mark_circle(size=60).encode(
    x=alt.X('pib_per_capita', scale=alt.Scale(type="log"), title='PIB Per Capita Médio'),
    y=alt.Y('taxa_mortalidade', title='Taxa Máxima de Mortalidade COVID (%)'),
    tooltip=['pais', 'pib_per_capita', 'taxa_mortalidade'],
    color='pais'
).properties(
    title="Relação entre Riqueza e Impacto da Pandemia"
).interactive()

st.altair_chart(scatter_chart, use_container_width=True)


# 5. Tabela resumo
st.markdown("---")
st.subheader("Tabela de Dados Brutos (Amostra)")
st.dataframe(df_sel)
=======
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

>>>>>>> a019aa29b526f81ccda577d52c06fe132923200c
