import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da página
st.set_page_config(layout="wide", page_title="Dashboard de Indicadores GeoTI")

# Funções de carregamento de dados
def load_data(filename, sheet_name):
    return pd.read_excel(filename, sheet_name=sheet_name, header=1)

def load_sla_data():
    return pd.read_excel('geoti_sla.xlsx')

def order_months(df):
    months_order = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    df['Mês'] = pd.Categorical(df['Mês'], categories=months_order, ordered=True)
    return df.sort_values('Mês')

# Configurações e variáveis globais
sheet_names = ['Planilha1', 'Planilha2', 'Planilha3', 'Planilha4', 'Chamados']
MAIN_FILE = 'indicadoresGeoTI_20dez2024.xlsx'

# Título do aplicativo
st.title('Dashboard de Indicadores GeoTI')

# Criação das abas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    'Chamados por Categoria',
    'Chamados por Status',
    'Chamados por Mês (2023)',
    'Chamados por Mês (2024)',
    'Detalhamento dos Chamados',
    'SLA dos Chamados'
])

# Dashboard 1 - Chamados por Categoria
with tab1:
    st.header('Chamados GeoTI por Categoria (até 20/12/2024)')
    data1 = load_data(MAIN_FILE, sheet_names[0])
    data1 = data1[data1['Categoria'] != 'Todas as categorias']

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(data1.set_index('Categoria'))
    with col2:
        fig1 = px.pie(data1, names='Categoria', values='Total', 
                     title='Distribuição por Categoria')
        st.plotly_chart(fig1, use_container_width=True)

# Dashboard 2 - Chamados por Status
with tab2:
    st.header('Chamados GeoTI por Status (até 20/12/2024)')
    data2 = load_data(MAIN_FILE, sheet_names[1])
    data2 = data2[~data2['Status'].isin(['Todos os status', 'Total'])]

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(data2.set_index('Status'))
    with col2:
        fig2 = px.pie(data2, names='Status', values='Total', 
                     title='Distribuição por Status')
        st.plotly_chart(fig2, use_container_width=True)

# Dashboard 3 - Chamados 2023
with tab3:
    st.header('Chamados GeoTI por Mês (01/05/2023-31/12/2023)')
    data3 = load_data(MAIN_FILE, sheet_names[2])
    data3 = data3[data3['Mês'] != 'Todos os meses']
    data3 = order_months(data3)
    st.line_chart(data3.set_index('Mês'))

# Dashboard 4 - Chamados 2024
with tab4:
    st.header('Chamados GeoTI por Mês (01/01/2024-20/12/2024)')
    data4 = load_data(MAIN_FILE, sheet_names[3])
    data4 = data4[data4['Mês'] != 'Todos os meses']
    data4 = order_months(data4)
    st.line_chart(data4.set_index('Mês'))

# Dashboard 5 - Detalhamento dos Chamados
with tab5:
    st.header('Detalhamento dos Chamados GeoTI')
    data5 = load_data(MAIN_FILE, 'Chamados')

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        categoria_filter = st.multiselect(
            'Filtrar por Categoria:', 
            options=sorted(data5['Categoria'].unique())
        )
    with col2:
        status_filter = st.multiselect(
            'Filtrar por Status:', 
            options=sorted(data5['Status'].unique())
        )
    with col3:
        prioridade_filter = st.multiselect(
            'Filtrar por Prioridade:',
            options=sorted(data5['Prioridade'].unique())
        )

    # Aplicação dos filtros
    df_filtered = data5
    if categoria_filter:
        df_filtered = df_filtered[df_filtered['Categoria'].isin(categoria_filter)]
    if status_filter:
        df_filtered = df_filtered[df_filtered['Status'].isin(status_filter)]
    if prioridade_filter:
        df_filtered = df_filtered[df_filtered['Prioridade'].isin(prioridade_filter)]

    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Chamados", len(df_filtered))
    with col2:
        st.metric("Tempo Médio (horas)", 
                 round(df_filtered['HORAS EM NÚMEROS'].mean(), 2))
    with col3:
        st.metric("Chamados em Aberto", 
                 len(df_filtered[df_filtered['Status'] == 'Novo']))
    with col4:
        st.metric("Chamados Concluídos",
                 len(df_filtered[df_filtered['Status'] == 'Concluído (solucionado)']))

    # Gráficos
    col1, col2 = st.columns(2)
    with col1:
        fig_cat = px.bar(
            df_filtered['Categoria'].value_counts().reset_index(),
            x='index', y='Categoria',
            title='Distribuição de Chamados por Categoria'
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        fig_status = px.pie(
            df_filtered, 
            names='Status',
            title='Distribuição por Status'
        )
        st.plotly_chart(fig_status, use_container_width=True)

    # Tabela detalhada
    st.subheader('Tabela de Chamados')
    colunas_exibir = [
        'ID', 'Solicitante', 'Solicitado em', 'Categoria', 
        'Descrição da solicitação', 'Prioridade', 'Status', 
        'Atribuído a', 'Solução empregada', 'HORAS EM NÚMEROS'
    ]

    st.dataframe(
        df_filtered[colunas_exibir].sort_values('Solicitado em', ascending=False),
        hide_index=True,
        column_config={
            'ID': st.column_config.NumberColumn('ID', format='%d'),
            'Solicitado em': st.column_config.DatetimeColumn('Solicitado em'),
            'HORAS EM NÚMEROS': st.column_config.NumberColumn('Horas', format='%.2f'),
            'Descrição da solicitação': st.column_config.TextColumn('Descrição', width='large'),
            'Solução empregada': st.column_config.TextColumn('Solução', width='large')
        }
    )

# Dashboard 6 - SLA dos Chamados
with tab6:
    st.header('Análise de SLA dos Chamados')
    sla_data = load_sla_data()

    # Métricas SLA
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Chamados", len(sla_data))
    with col2:
        tempo_medio = sla_data['HORAS EM NÚMEROS'].mean()
        st.metric("Tempo Médio de Resposta", f"{tempo_medio:.2f} horas")
    with col3:
        dentro_sla = len(sla_data[sla_data['HORAS EM NÚMEROS'] <= 24]) / len(sla_data) * 100
        st.metric("Dentro do SLA (24h)", f"{dentro_sla:.1f}%")

    # Gráficos SLA
    col1, col2 = st.columns(2)
    with col1:
        tempo_categoria = sla_data.groupby('Categoria')['HORAS EM NÚMEROS'].mean().reset_index()
        fig_tempo = px.bar(
            tempo_categoria,
            x='Categoria',
            y='HORAS EM NÚMEROS',
            title='Tempo Médio de Resposta por Categoria'
        )
        st.plotly_chart(fig_tempo, use_container_width=True)

    with col2:
        fig_prioridade = px.pie(
            sla_data,
            names='Prioridade',
            title='Distribuição por Prioridade'
        )
        st.plotly_chart(fig_prioridade, use_container_width=True)

    # Filtros SLA
    col1, col2 = st.columns(2)
    with col1:
        sla_prioridade_filter = st.multiselect(
            'Filtrar por Prioridade (SLA):',
            options=sorted(sla_data['Prioridade'].unique())
        )
    with col2:
        sla_categoria_filter = st.multiselect(
            'Filtrar por Categoria (SLA):',
            options=sorted(sla_data['Categoria'].unique())
        )

    # Aplicar filtros SLA
    sla_filtered = sla_data
    if sla_prioridade_filter:
        sla_filtered = sla_filtered[sla_filtered['Prioridade'].isin(sla_prioridade_filter)]
    if sla_categoria_filter:
        sla_filtered = sla_filtered[sla_filtered['Categoria'].isin(sla_categoria_filter)]

    # Tabela SLA
    st.dataframe(
        sla_filtered[[
            'ID', 'Solicitante', 'Solicitado em', 'Categoria', 
            'Prioridade', 'Status', 'Tempo decorrido',
            'HORAS EM NÚMEROS', 'MÉDIA'
        ]].sort_values('Solicitado em', ascending=False),
        hide_index=True,
        column_config={
            'ID': st.column_config.NumberColumn('ID', format='%d'),
            'Solicitado em': st.column_config.DatetimeColumn('Solicitado em'),
            'HORAS EM NÚMEROS': st.column_config.NumberColumn('Horas', format='%.2f'),
            'MÉDIA': st.column_config.NumberColumn('Média', format='%.2f'),
            'Tempo decorrido': st.column_config.TextColumn('Tempo Decorrido', width='medium')
        }
    )

    # Download dos dados SLA
    csv = sla_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download dos dados SLA (CSV)",
        data=csv,
        file_name="dados_sla.csv",
        mime="text/csv"
    )
