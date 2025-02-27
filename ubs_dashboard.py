import streamlit as st
import pandas as pd
import plotly.express as px

# =============================
# 1) LEITURA E PREPARAÇÃO DOS DADOS
# =============================
df = pd.read_csv("ubs_atualizado.csv", sep=";")

# Limpa espaços extras na coluna Nome_UF
df['Nome_UF'] = df['Nome_UF'].astype(str).str.strip()

# Substitui vírgulas por ponto nas colunas de coordenadas (caso existam)
df['LATITUDE'] = df['LATITUDE'].astype(str).str.replace(',', '.')
df['LONGITUDE'] = df['LONGITUDE'].astype(str).str.replace(',', '.')

# Converte as colunas para numérico (valores inválidos viram NaN)
df['LATITUDE'] = pd.to_numeric(df['LATITUDE'], errors='coerce')
df['LONGITUDE'] = pd.to_numeric(df['LONGITUDE'], errors='coerce')

# =============================
# 2) CRIAÇÃO DOS GRÁFICOS INICIAIS
# =============================
st.title("Dashboard de Unidades Básicas de Saúde (UBS)")

# -- Freq. de UBS por Estado
df_freq = df['Nome_UF'].value_counts().reset_index()
df_freq.columns = ['Estado', 'Frequência']

grafico = px.bar(
    df_freq, 
    x='Estado', 
    y='Frequência', 
    title='Frequência de UBS por Estado', 
    labels={'Estado': 'Estado', 'Frequência': 'Número de UBS'},
    text_auto=True
)
st.plotly_chart(grafico)

# -- Filtro para exibir tabela das UBS por estado
estados = st.multiselect("Selecione os estados", df_freq['Estado'].unique())
if estados:
    df_filtrado_tabela = df[df['Nome_UF'].isin(estados)]
    st.write(df_filtrado_tabela)

# -- Gráfico de pizza
fig_pie = px.pie(
    df_freq, 
    values='Frequência', 
    names='Estado', 
    title="Distribuição de UBS por Estado"
)
st.plotly_chart(fig_pie)

# -- Contagem de UBS por município
df_municipios = df['Nome_Município'].value_counts().reset_index()
df_municipios.columns = ['Município', 'Frequência']

min_ubs = st.slider("Número mínimo de UBS por município", 0, int(df_municipios['Frequência'].max()), 300)
df_municipios_filtrado = df_municipios[df_municipios['Frequência'] >= min_ubs]

fig_hist = px.histogram(
    df_municipios_filtrado, 
    x='Município', 
    y='Frequência', 
    title=f'Municípios com pelo menos {min_ubs} UBS',
    labels={'Município': 'Município', 'Frequência': 'Número de UBS'},
    text_auto=True
)
st.plotly_chart(fig_hist)

# =============================
# 3) MAPA INTERATIVO COM FILTRO LATERAL
# =============================

# Filtro na barra lateral para selecionar o estado
estado_selecionado = st.sidebar.selectbox(
    'Selecione o Estado para o mapa:',
    df['Nome_UF'].unique()
)

# Filtra os dados para o estado selecionado
df_mapa = df[df['Nome_UF'] == estado_selecionado]

# Remove linhas onde LATITUDE ou LONGITUDE são nulas
df_mapa = df_mapa.dropna(subset=['LATITUDE', 'LONGITUDE'])

st.write(f"Exibindo UBS para o estado: {estado_selecionado}")
st.write("Número de UBS encontradas:", df_mapa.shape[0])

# Exibe algumas linhas para verificar as coordenadas
st.write("Prévia dos dados filtrados:", df_mapa[['Nome_UF','LATITUDE','LONGITUDE']].head(10))

# Exibe o mapa interativo
st.map(df_mapa[['LATITUDE', 'LONGITUDE']])
