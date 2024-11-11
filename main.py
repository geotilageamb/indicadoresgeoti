import streamlit as st
import pandas as pd

# Função para carregar dados de uma aba específica do Excel
def load_data(sheet_name):
    return pd.read_excel('indicadoresGeoTI_11nov2024.xlsx', sheet_name=sheet_name)

# Títulos das abas que correspondem aos dashboards
sheet_names = ['Planilha1', 'Planilha2', 'Planilha3', 'Planilha4']

# Título do aplicativo
st.title('Dashboard de Indicadores GeoTI')

# Criação de abas no Streamlit
tab1, tab2, tab3, tab4 = st.tabs([
    'Chamados por Categoria',
    'Chamados por Status',
    'Chamados por Mês (2023)',
    'Chamados por Mês (2024)'
])

# Dashboard 1
with tab1:
    st.header('Chamados GeoTI por Categoria (11/11/2024)')
    data1 = load_data(sheet_names[0])
    if 'Categoria' in data1.columns:
        st.bar_chart(data1.set_index('Categoria'))
    else:
        st.write("Coluna 'Categoria' não encontrada.")

# Dashboard 2
with tab2:
    st.header('Chamados GeoTI por Status (11/11/2024)')
    data2 = load_data(sheet_names[1])
    if 'Status' in data2.columns:
        st.bar_chart(data2.set_index('Status'))
    else:
        st.write("Coluna 'Status' não encontrada.")

# Dashboard 3
with tab3:
    st.header('Chamados GeoTI por Mês (01/05/2023-31/12/2023)')
    data3 = load_data(sheet_names[2])
    if 'Mês' in data3.columns:
        st.line_chart(data3.set_index('Mês'))
    else:
        st.write("Coluna 'Mês' não encontrada.")

# Dashboard 4
with tab4:
    st.header('Chamados GeoTI por Mês (01/01/2024-11/11/2024)')
    data4 = load_data(sheet_names[3])
    if 'Mês' in data4.columns:
        st.line_chart(data4.set_index('Mês'))
    else:
        st.write("Coluna 'Mês' não encontrada.")

# Para executar o aplicativo, use o comando: streamlit run nome_do_arquivo.py
