import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar dados de uma aba específica do Excel
def load_data(sheet_name):
    return pd.read_excel('indicadoresGeoTI_11nov2024.xlsx', sheet_name=sheet_name, header=1)

# Função para ordenar os meses
def order_months(df):
    months_order = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    df['Mês'] = pd.Categorical(df['Mês'], categories=months_order, ordered=True)
    df = df.sort_values('Mês')
    return df

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
    data1 = data1[data1['Categoria'] != 'Todas as categorias']
    st.bar_chart(data1.set_index('Categoria'))

    # Gráfico de Pizza
    fig1, ax1 = plt.subplots()
    ax1.pie(data1['Total'], labels=data1['Categoria'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

# Dashboard 2
with tab2:
    st.header('Chamados GeoTI por Status (11/11/2024)')
    data2 = load_data(sheet_names[1])
    data2 = data2[data2['Status'] != 'Todos os status']
    st.bar_chart(data2.set_index('Status'))

    # Gráfico de Pizza
    fig2, ax2 = plt.subplots()
    ax2.pie(data2['Total'], labels=data2['Status'], autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

# Dashboard 3
with tab3:
    st.header('Chamados GeoTI por Mês (01/05/2023-31/12/2023)')
    data3 = load_data(sheet_names[2])
    data3 = data3[data3['Mês'] != 'Todos os meses']
    data3 = order_months(data3)
    st.line_chart(data3.set_index('Mês'))

# Dashboard 4
with tab4:
    st.header('Chamados GeoTI por Mês (01/01/2024-11/11/2024)')
    data4 = load_data(sheet_names[3])
    data4 = data4[data4['Mês'] != 'Todos os meses']
    data4 = order_months(data4)
    st.line_chart(data4.set_index('Mês'))

# Para executar o aplicativo, use o comando: streamlit run nome_do_arquivo.py
