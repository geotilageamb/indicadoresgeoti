import streamlit as st
import pandas as pd
import plotly.express as px

def load_sla_data():
    try:
        return pd.read_excel('geoti_sla.xlsx')
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
                tempo_medio = sla_data['Tempo decorrido números'].mean()
                st.metric("Tempo Médio de Atendimento", f"{tempo_medio:.2f} horas")

            with col3:
                chamados_no_prazo = len(sla_data[sla_data['Tempo decorrido números'] <= 24])
                percentual_sla = (chamados_no_prazo / total_chamados * 100)
                st.metric("% Dentro do SLA (24h)", f"{percentual_sla:.1f}%")

            # Gráficos do SLA
            col1, col2 = st.columns(2)

            with col1:
                tempo_categoria = sla_data.groupby('Categoria')['Tempo decorrido números'].mean().reset_index()
                fig_tempo = px.bar(
                    tempo_categoria,
                    x='Categoria',
                    y='Tempo decorrido números',
                    title='Tempo Médio de Atendimento por Categoria'
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
                    'Tempo decorrido números', 'MÉDIA'
                ]].sort_values('Solicitado em', ascending=False),
                hide_index=True,
                column_config={
                    'ID': st.column_config.NumberColumn('ID', format='%d'),
                    'Solicitado em': st.column_config.DatetimeColumn('Solicitado em'),
                    'Tempo decorrido números': st.column_config.NumberColumn('Horas', format='%.2f'),
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
