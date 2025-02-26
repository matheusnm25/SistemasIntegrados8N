import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar o arquivo atualizado
df = pd.read_csv("ubs_atualizado.csv", sep=";")

# Contar a frequência de UBS por estado
df_freq = df['Nome_UF'].value_counts().reset_index()
df_freq.columns = ['Estado', 'Frequência']

# Criar o dashboard
st.title("Dashboard de Unidades Básicas de Saúde (UBS)")

# Gráfico de barras
grafico = px.bar(df_freq, x='Estado', y='Frequência', 
                 title='Frequência de UBS por Estado', 
                 labels={'Estado': 'Estado', 'Frequência': 'Número de UBS'},
                 text_auto=True)

st.plotly_chart(grafico)

# Filtro para estados específicos
estados = st.multiselect("Selecione os estados", df_freq['Estado'].unique())
if estados:
    df_filtrado = df[df['Nome_UF'].isin(estados)]
    st.write(df_filtrado)

# Gráfico de pizza
fig = px.pie(df_freq, values='Frequência', names='Estado', title="Distribuição de UBS por Estado")
st.plotly_chart(fig)

# Contagem de UBS por município
df_municipios = df['Nome_Município'].value_counts().reset_index()
df_municipios.columns = ['Município', 'Frequência']

# Slider para filtro de municípios
municipios = st.slider("Número mínimo de UBS por município", 0, df_municipios['Frequência'].max(), 300)

# Aplicando o filtro
df_municipios_filtrado = df_municipios[df_municipios['Frequência'] >= municipios]

# Criando o histograma filtrado
fig2 = px.histogram(df_municipios_filtrado, x='Município', y='Frequência', 
                    title=f'Municípios com pelo menos {municipios} UBS',
                    labels={'Município': 'Município', 'Frequência': 'Número de UBS'},
                    text_auto=True)

st.plotly_chart(fig2)
