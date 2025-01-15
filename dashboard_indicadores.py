import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(sheet_name):
    return pd.read_excel('indicadoresGeoTI_20dez2024.xlsx', sheet_name=sheet_name, header=1)

def order_months(df):
    months_order = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    df['Mês'] = pd.Categorical(df['Mês'], categories=months_order, ordered=True)
    return df.sort_values('Mês')

def show_dashboard():
    # Títulos das abas que correspondem aos dashboards
    sheet_names = ['Planilha1', 'Planilha2', 'Planilha3', 'Planilha4']

    # Criação das subabas
    tab1, tab2, tab3, tab4 = st.tabs([
        'Chamados por Categoria',
        'Chamados por Status',
        'Chamados por Mês (2023)',
        'Chamados por Mês (2024)'
    ])

    # Dashboard 1
    with tab1:
        st.header('Chamados GeoTI por Categoria (até 20/12/2024)')
        data1 = load_data(sheet_names[0])
        data1 = data1[data1['Categoria'] != 'Todas as categorias']

        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(data1.set_index('Categoria'))
        with col2:
            fig1 = px.pie(data1, names='Categoria', values='Total', 
                         title='Distribuição por Categoria')
            st.plotly_chart(fig1, use_container_width=True)

    # Dashboard 2
    with tab2:
        st.header('Chamados GeoTI por Status (até 20/12/2024)')
        data2 = load_data(sheet_names[1])
        data2 = data2[~data2['Status'].isin(['Todos os status', 'Total'])]

        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(data2.set_index('Status'))
        with col2:
            fig2 = px.pie(data2, names='Status', values='Total', 
                         title='Distribuição por Status')
            st.plotly_chart(fig2, use_container_width=True)

    # Dashboard 3
    with tab3:
        st.header('Chamados GeoTI por Mês (01/05/2023-31/12/2023)')
        data3 = load_data(sheet_names[2])
        data3 = data3[data3['Mês'] != 'Todos os meses']
        data3 = order_months(data3)
        st.line_chart(data3.set_index('Mês'))

    # Dashboard 4
    with tab4:
        st.header('Chamados GeoTI por Mês (01/01/2024-20/12/2024)')
        data4 = load_data(sheet_names[3])
        data4 = data4[data4['Mês'] != 'Todos os meses']
        data4 = order_months(data4)
        st.line_chart(data4.set_index('Mês'))
