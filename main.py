import streamlit as st
import pandas as pd

# Função para carregar dados de uma aba específica do Excel
def load_data(sheet_name):
    return pd.read_excel('indicadoresGeoTI_11nov2024.xlsx', sheet_name=sheet_name)

# Títulos das abas que correspondem aos dashboards
sheet_names = [
    'Chamados GeoTI por categoria',
    'Chamados GeoTI por status',
    'Chamados GeoTI por mês (2023)',
    'Chamados GeoTI por mês (2024)'
]

# Título do aplicativo
st.title('Dashboard de Indicadores GeoTI')

# Criação de abas no Streamlit
tab1, tab2, tab3, tab4 = st.tabs(sheet_names)

# Dashboard 1
with tab1:
    st.header(sheet_names[0])
    data1 = load_data(sheet_names[0])
    st.bar_chart(data1.set_index('Categoria'))

# Dashboard 2
with tab2:
    st.header(sheet_names[1])
    data2 = load_data(sheet_names[1])
    st.bar_chart(data2.set_index('Status'))

# Dashboard 3
with tab3:
    st.header(sheet_names[2])
    data3 = load_data(sheet_names[2])
    st.line_chart(data3.set_index('Mês'))

# Dashboard 4
with tab4:
    st.header(sheet_names[3])
    data4 = load_data(sheet_names[3])
    st.line_chart(data4.set_index('Mês'))

# Para executar o aplicativo, use o comando: streamlit run nome_do_arquivo.py
