import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Configuração da página — apenas uma vez
st.set_page_config(page_title="Dashboard Cooppras", layout="wide")

logo_url = "https://cooppras.com.br/wp-content/uploads/2024/03/LOGO_OFICIAL_CDR.png"
st.markdown(
    
    logo_url = "https://cooppras.com.br/wp-content/uploads/2024/03/LOGO_OFICIAL_CDR.png"

col_logo, col_title = st.columns([3, 1])

with col_title:
    st.image(logo_url, width=150)

with col_logo:
    st.markdown(
        "<h3 style='text-align: center; color:#2B6CB0;'>Dashboard dos Produtores de Ovinos</h3>",
        unsafe_allow_html=True
    )


# 1. Carregar dados

st.subheader("Carregando Dados📥")

url = "https://drive.google.com/uc?id=1amRbo-F46eHp28K9SEGfS5vA3RlU70c3"

df = pd.read_csv(url, sep=";")

st.write("Amostra dos dados:")
st.dataframe(df.head())

# 2. Indicadores gerais
st.subheader("Indicadores Gerais📌")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Produtores", df.shape[0])
col2.metric("Idade Média", round(df["idade"].mean(), 1))
col3.metric("Lucro Bruto Médio (R$)", round(df["lucro_bruto"].mean(), 2))
col4.metric("Número Médio de Animais", round(df["quantidade_animais"].mean(), 1))


# 3. Distribuição de Sexo
st.subheader("Distribuição por Sexo📊")
fig = px.pie(df, names="sexo", title="Distribuição de Sexo")
st.plotly_chart(fig, use_container_width=True)

# 4. Nível Tecnológico
st.subheader("Nível Tecnológico dos Produtores⚙️")
fig2 = px.histogram(
    df,
    x="nivel_tecnologico",
    color="nivel_tecnologico",
    title="Distribuição do Nível Tecnológico",
)
st.plotly_chart(fig2, use_container_width=True)

# 5. Lucro Bruto por Sistema de Criação
st.subheader("Lucro Bruto por Sistema de Criação💰")

fig3 = px.box(
    df,
    x="sistema_criacao",
    y="lucro_bruto",
    color="sistema_criacao",
    title="Comparação de Lucro por Sistema de Criação",
)
st.plotly_chart(fig3, use_container_width=True)

# 6. Correlação: Número de Animais x Lucro Bruto
st.subheader("Dispersão: quantidade de animais vs lucro bruto📈")

fig4 = px.scatter(
    df,
    x="quantidade_animais",
    y="lucro_bruto",
    trendline="ols",
    title="Relação entre Número de Animais e Lucro",
)
st.plotly_chart(fig4, use_container_width=True)

# 7. Gastos médios por categoria
st.subheader("Composição dos Gastos Médios💸")

gastos_cols = ["alimentacao", "remedio_vacina", "mao_de_obra", "energia", "agua", "transporte", "outros_gastos"]

gastos_medios = df[gastos_cols].mean().reset_index()
gastos_medios.columns = ["categoria", "valor"]

fig5 = px.bar(
    gastos_medios,
    x="categoria",
    y="valor",
    title="Gastos Médios por Categoria (R$)",
)
st.plotly_chart(fig5, use_container_width=True)

# 8. Tabela filtrável

st.subheader("Filtro dos Cooperados🔎")

filtro_sistema = st.selectbox("Selecione o sistema de criação:", df["sistema_criacao"].unique())

df_filtrado = df[df["sistema_criacao"] == filtro_sistema]

st.write(f"Produtores que usam o sistema: **{filtro_sistema}**")
st.dataframe(df_filtrado)
