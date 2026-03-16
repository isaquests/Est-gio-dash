import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Dashboard Cooppras", layout="wide")

logo_direita = "https://cooppras.com.br/wp-content/uploads/2024/03/LOGO_OFICIAL_CDR.png"
logo_esquerda = "https://cooppras.com.br/wp-content/uploads/2024/03/LOGO_OFICIAL_CDR.png"

col1, col2, col3 = st.columns([1,4,1])

with col1:
    st.image("https://cooppras.com.br/wp-content/uploads/2024/03/LOGO_OFICIAL_CDR.png", width=120)

with col2:
    st.markdown("<h1 style='text-align:center;'>DASHBOARD DOS PRODUTORES DE OVINOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Análise econômica e produtiva da COOPIPRAS</p>", unsafe_allow_html=True)

with col3:
    st.image("https://cooppras.com.br/wp-content/uploads/2024/03/LOGO_OFICIAL_CDR.png", width=120)



# Upload do CSV
arquivo = "https://docs.google.com/spreadsheets/d/1BU8vr3jZVpIhhRwJmN6SMQh7NCQZcSy5/export?format=csv&gid=622776986"

if arquivo is None:
    st.stop()

df = pd.read_csv(arquivo)

# Limpar nomes das colunas
df.columns = df.columns.str.strip()

# -----------------------------
# Limpeza dos dados numéricos
# -----------------------------

colunas_numericas = [
    "idade",
    "tempo_atuacao_anos",
    "total_animais",
    "partos_ano",
    "receita_venda",
    "custo_total_mes",
    "custo_animal",
    "custo_alimentacao",
    "custo_sanidade",
    "custo_energia",
    "custo_agua",
    "custo_transporte"
]

for col in colunas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Indicadores principais da produção
# -----------------------------

# st.subheader("📌 Indicadores da Produção")

with st.container(border=True):

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Idade média",
        round(df["idade"].mean())
    )
    
    col2.metric(
        "Tempo médio de atuação (anos)",
        round(df["tempo_atuacao_anos"].mean())
    )
    
    col3.metric(
        "Partos por ano",
        round(df["partos_ano"].mean(), 1)
    )
    
    col4.metric(
        "Custo médio por animal (R$)",
        round(df["custo_animal"].mean(), 2)
    )

# col5 = st.columns(1)[0]
    col5.metric(
        "Média de animais por produtor",
        round(df["total_animais"].mean())
    )

# -----------------------------
# Seção de gráficos analíticos
# -----------------------------

# função que traça uma linha para dividir as coisas ==> st.divider()

# st.subheader("📊 Análises")
with st.container(border=True):
    col1, col2 = st.columns(2)

# Gráfico de escolaridade dos produtores
    with col1:
    
        if "escolaridade" in df.columns:
    
            dados = df["escolaridade"].value_counts().reset_index()
            dados.columns = ["escolaridade", "quantidade"]
    
            fig1 = px.bar(
                dados,
                x="escolaridade",
                y="quantidade",
                title="Escolaridade dos Produtores",
                text="quantidade"
            )
    
            st.plotly_chart(fig1, use_container_width=True)

# Distribuição de lucratividade
with st.container(border=True):
    with col2:
    
        if "lucratividade?" in df.columns:
    
            dados = df["lucratividade?"].value_counts().reset_index()
            dados.columns = ["lucratividade", "quantidade"]
    
            fig2 = px.pie(
                dados,
                names="lucratividade",
                values="quantidade",
                title="Distribuição de Lucratividade"
            )
    
            st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)

# -----------------------------
# Tipo de comercialização da produção
# -----------------------------

# st.subheader("📊 Tipo de Comercialização da Produção")
with st.container(border=True):
    comercializacao = df["destino"].value_counts().reset_index()
    comercializacao.columns = ["Tipo", "Quantidade"]
    
    fig = px.bar(
        comercializacao,
        x="Tipo",
        y="Quantidade",
        text="Quantidade",
        color="Tipo"
    )
    
    fig.update_layout(
        xaxis_title="Tipo de Comercialização",
        yaxis_title="Quantidade de Produtores",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Comparação de custos médios da produção
with st.container(border=True):
    with col3:
    
        gastos_cols = [
            "custo_agua",
            "custo_energia",
            "custo_alimentacao",
            "custo_sanidade",
            "custo_transporte"
        ]
    
        gastos_existentes = [g for g in gastos_cols if g in df.columns]
    
        if gastos_existentes:
    
            gastos_medios = df[gastos_existentes].mean().reset_index()
            gastos_medios.columns = ["categoria", "valor"]
    
            gastos_medios["categoria"] = gastos_medios["categoria"].str.replace("custo_", "")
            gastos_medios["categoria"] = gastos_medios["categoria"].str.capitalize()
    
            fig3 = px.bar(
                gastos_medios,
                x="valor",
                y="categoria",
                orientation="h",
                title="Custos Médios",
                text="valor"
            )
    
            st.plotly_chart(fig3, use_container_width=True)

# Comparação entre receita média e custo médio
with st.container(border=True):
    with col4:
    
        if "receita_venda" in df.columns and "custo_total_mes" in df.columns:
    
            dados = pd.DataFrame({
                "tipo": ["Receita média", "Custo médio"],
                "valor": [
                    df["receita_venda"].mean(),
                    df["custo_total_mes"].mean()
                ]
            })
    
            fig = px.bar(
                dados,
                x="tipo",
                y="valor",
                title="Receita média x Custo médio",
                text="valor"
            )
    
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Ranking das principais dificuldades
# -----------------------------

# st.subheader("🏆 Ranking das Principais Dificuldades dos Produtores")
with st.container(border=True):
    ranking_dificuldades = (
        df["dificuldades_enfrentadas"]
        .value_counts()
        .head(5)
        .reset_index()
    )
    
    ranking_dificuldades.columns = ["Dificuldade", "Quantidade"]
    
    fig = px.bar(
        ranking_dificuldades,
        x="Quantidade",
        y="Dificuldade",
        orientation="h",
        text="Quantidade",
        color="Quantidade"
    )
    
    fig.update_layout(
        xaxis_title="Número de Produtores",
        yaxis_title="Dificuldade",
        yaxis=dict(autorange="reversed")
    )
    
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Tabela completa do dataset
# -----------------------------

# st.divider()
st.subheader("📋 Dados completos")

st.dataframe(df)
