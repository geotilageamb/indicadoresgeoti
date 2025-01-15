import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def convert_time_to_hours(time_str):
    try:
        if pd.isna(time_str):
            return 0
        if isinstance(time_str, str):
            # Se for string no formato HH:MM:SS
            hours, minutes, seconds = map(float, time_str.split(':'))
            return hours + minutes/60 + seconds/3600
        elif isinstance(time_str, timedelta):
            # Se for timedelta
            return time_str.total_seconds() / 3600
        else:
            # Para outros formatos de tempo
            total_seconds = time_str.hour * 3600 + time_str.minute * 60 + time_str.second
            return total_seconds / 3600
    except:
        return 0

def load_sla_data():
    try:
        # Carrega os dados do Excel
        df = pd.read_excel('geoti_sla.xlsx')

        # Converte a coluna de tempo para horas
        if 'Tempo decorrido' in df.columns:
            df['Tempo decorrido números'] = df['Tempo decorrido'].apply(convert_time_to_hours)

        # Calcula a média geral
        df['MÉDIA'] = df['Tempo decorrido números'].mean()

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
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_chamados = len(sla_data)
                st.metric("Total de Chamados", total_chamados)

            with col2:
                tempo_medio = sla_data['Tempo decorrido números'].mean()
                st.metric("Tempo médio de conclusão dos chamados", f"{tempo_medio:.2f} horas")

            with col3:
                chamados_no_prazo = len(sla_data[sla_data['Tempo decorrido números'] <= 24])
                percentual_sla = (chamados_no_prazo / total_chamados * 100)
                st.metric("% Dentro do SLA (24h)", f"{percentual_sla:.1f}%")

            with col4:
                media_geral = sla_data['MÉDIA'].iloc[0]
                st.metric("Média geral", f"{media_geral:.2f} horas")

            # Gráficos do SLA
            col1, col2 = st.columns(2)

            with col1:
                tempo_categoria = sla_data.groupby('Categoria')['Tempo decorrido números'].mean().reset_index()
                fig_tempo = px.bar(
                    tempo_categoria,
                    x='Categoria',
                    y='Tempo decorrido números',
                    title='Tempo médio de conclusão dos chamados por Categoria (horas)'
                )
                fig_tempo.add_hline(
                    y=media_geral,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Média geral: {media_geral:.2f}h"
                )
                st.plotly_chart(fig_tempo, use_container_width=True)

            with col2:
                fig_prioridade = px.pie(
                    sla_data,
                    names='Prioridade',
                    title='Distribuição de Chamados por Prioridade'
                )
                st.plotly_chart(fig_prioridade, use_container_width=True)

            # Análise temporal
            st.subheader('Evolução do Tempo médio de conclusão dos chamados')

            # Converter 'Solicitado em' para datetime se ainda não estiver
            sla_data['Solicitado em'] = pd.to_datetime(sla_data['Solicitado em'])

            # Criar coluna de mês/ano
            sla_data['Mês/Ano'] = sla_data['Solicitado em'].dt.strftime('%Y-%m')

            # Calcular média mensal
            media_mensal = sla_data.groupby('Mês/Ano')['Tempo decorrido números'].agg([
                ('Média', 'mean'),
                ('Quantidade', 'count')
            ]).reset_index()

            # Ordenar por mês/ano
            media_mensal = media_mensal.sort_values('Mês/Ano')

            # Criar gráfico combinado de linha e barras
            fig_temporal = px.line(
                media_mensal,
                x='Mês/Ano',
                y='Média',
                title='Evolução do Tempo médio de conclusão dos chamados por mês',
                markers=True
            )

            # Adicionar barras para quantidade de chamados
            fig_temporal.add_bar(
                x=media_mensal['Mês/Ano'],
                y=media_mensal['Quantidade'],
                name='Quantidade de Chamados',
                yaxis='y2',
                opacity=0.3
            )

            # Configurar eixos
            fig_temporal.update_layout(
                yaxis=dict(
                    title='Tempo Médio (horas)',
                    side='left'
                ),
                yaxis2=dict(
                    title='Quantidade de Chamados',
                    side='right',
                    overlaying='y',
                    showgrid=False
                ),
                xaxis=dict(
                    title='Mês/Ano',
                    tickangle=45
                ),
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                )
            )

            # Adicionar linha da média geral
            fig_temporal.add_hline(
                y=media_geral,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Média geral: {media_geral:.2f}h"
            )

            st.plotly_chart(fig_temporal, use_container_width=True)

            # Comparação com a média (Scatter Plot)
            st.subheader('Distribuição dos Tempos de Atendimento')
            fig_comp = px.scatter(
                sla_data,
                x='Solicitado em',
                y='Tempo decorrido números',
                color='Categoria',
                title='Tempo de Atendimento por Chamado ao Longo do Tempo',
                hover_data=['ID', 'Solicitante', 'Status']
            )
            fig_comp.add_hline(
                y=media_geral,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Média geral: {media_geral:.2f}h"
            )

            # Melhorar o layout
            fig_comp.update_layout(
                xaxis_title="Data de Solicitação",
                yaxis_title="Tempo de Atendimento (horas)",
                hovermode='closest'
            )

            st.plotly_chart(fig_comp, use_container_width=True)

            # Tabela com os dados mensais
            st.subheader('Dados Mensais')
            media_mensal['Média'] = media_mensal['Média'].round(2)
            st.dataframe(
                media_mensal,
                hide_index=True,
                column_config={
                    'Mês/Ano': st.column_config.TextColumn('Mês/Ano'),
                    'Média': st.column_config.NumberColumn('Tempo Médio (horas)', format='%.2f'),
                    'Quantidade': st.column_config.NumberColumn('Quantidade de Chamados')
                }
            )

            # Filtros
            st.subheader('Filtros')
            col1, col2, col3 = st.columns(3)
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
            with col3:
                status_sla = st.multiselect(
                    'Filtrar por Status:',
                    options=sorted(sla_data['Status'].unique())
                )

            # Aplicar filtros
            df_sla_filtered = sla_data.copy()
            if categoria_sla:
                df_sla_filtered = df_sla_filtered[df_sla_filtered['Categoria'].isin(categoria_sla)]
            if prioridade_sla:
                df_sla_filtered = df_sla_filtered[df_sla_filtered['Prioridade'].isin(prioridade_sla)]
            if status_sla:
                df_sla_filtered = df_sla_filtered[df_sla_filtered['Status'].isin(status_sla)]

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
                    'MÉDIA': st.column_config.NumberColumn('Média geral', format='%.2f'),
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
