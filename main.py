import streamlit as st
import pandas as pd

# Função para carregar dados de uma aba específica do Excel
def load_data(sheet_name):
    # Substitua pelo caminho correto se necessário
    file_path = 'indicadoresGeoTI_11nov2024.xlsx'
    return pd.read_excel(file_path, sheet_name=sheet_name)

# Títulos das abas que correspondem aos dashboards
sheet_names = ['Dashboard1', 'Dashboard2', 'Dashboard3', 'Dashboard4']

# Título do aplicativo
st.title('Dashboard de Indicadores GeoTI')

# Criação de abas no Streamlit
tab1, tab2, tab3, tab4 = st.tabs(sheet_names)

# Dashboard 1
with tab1:
    st.header(sheet_names[0])
    data1 = load_data(sheet_names[0])
    st.write(data1)
    # Adicione visualizações específicas para o Dashboard 1 aqui

# Dashboard 2
with tab2:
    st.header(sheet_names[1])
    data2 = load_data(sheet_names[1])
    st.write(data2)
    # Adicione visualizações específicas para o Dashboard 2 aqui

# Dashboard 3
with tab3:
    st.header(sheet_names[2])
    data3 = load_data(sheet_names[2])
    st.write(data3)
    # Adicione visualizações específicas para o Dashboard 3 aqui

# Dashboard 4
with tab4:
    st.header(sheet_names[3])
    data4 = load_data(sheet_names[3])
    st.write(data4)
    # Adicione visualizações específicas para o Dashboard 4 aqui

# Para executar o aplicativo, use o comando: streamlit run nome_do_arquivo.py
