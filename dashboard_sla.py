import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def convert_time_to_hours(time_str):
    try:
        # Converte string de tempo (HH:MM:SS) para horas decimais
        if isinstance(time_str, str):
            hours, minutes, seconds = map(int, time_str.split(':'))
            return hours + minutes/60 + seconds/3600
        elif isinstance(time_str, timedelta):
            return time_str.total_seconds() / 3600
        else:
            return 0
    except:
        return 0

def load_sla_data():
    try:
        # Carrega os dados do Excel
        df = pd.read_excel('geoti_sla.xlsx')

        # Converte a coluna 'Tempo decorrido' para horas decimais
        df['Tempo_Horas'] = df['Tempo decorrido'].apply(convert_time_to_hours)

        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados do SLA: {str(e)}")
        return None

def show_dashboard():
    st.header('Análise de SLA dos Chamados')

    try:
        sla_data = load_sla_data()

        if sla_data is not None:
            # Métricas do SLA
            col1, col2, col3 = st.columns(3)
            with col1:
                total_chamados = len(sla_data)
                st.metric("Total de Chamados", total_chamados)

            with col2:
                tempo_medio = sla_data['Tempo_Horas'].mean()
                st.metric("Tempo Médio de Atendimento", f"{tempo_medio:.2f} horas")

            with col3:
                chamados_no_prazo = len(sla_data[sla_data['Tempo_Horas'] <= 24])
                percentual_sla = (chamados_no_prazo / total_chamados * 100)
                st.metric("% Dentro do SLA (24h)", f"{percentual_sla:.1f}%")

            # Gráficos do SLA
            col1, col2 = st.columns(2)

            with col1:
                tempo_categoria = sla_data.groupby('Categoria')['Tempo_Horas'].mean().reset_index()
                fig_tempo = px.bar(
                    tempo_categoria,
                    x='Categoria',
                    y='Tempo_Horas',
                    title='Tempo Médio de Atendimento por Categoria (horas)'
                )
                st.plotly_chart(fig_tempo, use_container_width=True)

            with col2:
                fig_prioridade = px.pie(
                    sla_data,
                    names='Prioridade',
                    title='Distribuição de Chamados por Prioridade'
                )
                st.plotly_chart(fig_prioridade, use_container_width=True)

            # Filtros
            st.subheader('Filtros')
            col1, col2 = st.columns(2)
            with col1:
                categoria_sla = st.multiselect(
                    'Filtrar por Categoria:',
                    options=sorted(sla_data['Categoria'].unique())
                )
            with col2:
                prioridade_sla = st.multiselect(
                    'Filtrar por Prioridade:',
                    options=sorted(sla_data['Prioridade'].unique())
                )

            # Aplicar filtros
            df_sla_filtered = sla_data.copy()
            if categoria_sla:
                df_sla_filtered = df_sla_filtered[df_sla_filtered['Categoria'].isin(categoria_sla)]
            if prioridade_sla:
                df_sla_filtered = df_sla_filtered[df_sla_filtered['Prioridade'].isin(prioridade_sla)]

            # Tabela de dados
            st.subheader('Detalhamento dos SLAs')
            st.dataframe(
                df_sla_filtered[[
                    'ID', 'Solicitante', 'Solicitado em', 'Categoria',
                    'Prioridade', 'Status', 'Tempo decorrido',
                    'Tempo_Horas', 'MÉDIA'
                ]].sort_values('Solicitado em', ascending=False),
                hide_index=True,
                column_config={
                    'ID': st.column_config.NumberColumn('ID', format='%d'),
                    'Solicitado em': st.column_config.DatetimeColumn('Solicitado em'),
                    'Tempo_Horas': st.column_config.NumberColumn('Horas', format='%.2f'),
                    'MÉDIA': st.column_config.NumberColumn('Média', format='%.2f'),
                    'Tempo decorrido': st.column_config.TextColumn('Tempo Decorrido', width='medium')
                }
            )

            # Download dos dados
            csv = df_sla_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download dos dados de SLA (CSV)",
                data=csv,
                file_name="dados_sla.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Erro ao processar dados do SLA: {str(e)}")
        st.info("Verifique se o arquivo 'geoti_sla.xlsx' está disponível e possui o formato correto.")

if __name__ == "__main__":
    show_dashboard()
