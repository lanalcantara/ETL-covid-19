import streamlit as st
import pandas as pd
import altair as alt

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard COVID")

# Título
st.title("📊 Análise Integrada: COVID-19 e Indicadores Globais")

# 1. Carregar dados
df = pd.read_csv("data/base_final_analise.csv")

# Padroniza nomes de colunas e datas
df.columns = df.columns.str.lower()  # todas minúsculas
if "periodo" in df.columns:
    df["periodo"] = pd.to_datetime(df["periodo"])
elif "data" in df.columns:
    df["periodo"] = pd.to_datetime(df["data"])
else:
    st.error("Coluna de data não encontrada no CSV.")

# 2. Filtros na barra lateral
paises = sorted(df["pais"].unique())
pais = st.sidebar.selectbox("Selecione o país", options=paises)

# Filtrar dataset pelo país selecionado
df_sel = df[df["pais"] == pais]

st.header(f"País Selecionado: {pais}")
st.markdown("---")

# === SEÇÃO 1: TENDÊNCIAS TEMPORAIS (COVID) ===
col1, col2 = st.columns(2)

# Gráfico de casos confirmados
with col1:
    st.subheader("Casos Confirmados (Tendência)")
    if "casos_confirmados" in df_sel.columns:
        chart_casos = alt.Chart(df_sel).mark_line(color="blue").encode(
            x="periodo:T",
            y="casos_confirmados:Q"
        ).interactive()
        st.altair_chart(chart_casos, use_container_width=True)
    else:
        st.warning("Coluna 'casos_confirmados' não encontrada.")

# Gráfico de óbitos
with col2:
    st.subheader("Óbitos (Tendência)")
    if "obitos" in df_sel.columns:
        chart_obitos = alt.Chart(df_sel).mark_line(color="red").encode(
            x="periodo:T",
            y="obitos:Q"
        ).interactive()
        st.altair_chart(chart_obitos, use_container_width=True)
    else:
        st.warning("Coluna 'obitos' não encontrada.")

# === SEÇÃO 2: TABELA DE DADOS ===
st.markdown("---")
st.subheader("Tabela de Dados Brutos (Amostra)")
st.dataframe(df_sel)

# === SEÇÃO 3: ANÁLISE SOCIOECONÔMICA GLOBAL ===
if "pib_per_capita" in df.columns and "taxa_mortalidade" in df.columns:
    st.markdown("---")
    st.header("Análise de Impacto Socioeconômico Global")

    df_agregado = df.groupby("pais").agg({
        "pib_per_capita": "mean",
        "taxa_mortalidade": "max"
    }).reset_index().dropna()

    st.subheader("PIB Per Capita vs. Taxa de Mortalidade")
    scatter_chart = alt.Chart(df_agregado).mark_circle(size=60).encode(
        x=alt.X("pib_per_capita", scale=alt.Scale(type="log"), title="PIB Per Capita Médio"),
        y=alt.Y("taxa_mortalidade", title="Taxa Máxima de Mortalidade COVID (%)"),
        tooltip=["pais", "pib_per_capita", "taxa_mortalidade"],
        color="pais"
    ).properties(
        title="Relação entre Riqueza e Impacto da Pandemia"
    ).interactive()
    st.altair_chart(scatter_chart, use_container_width=True)
