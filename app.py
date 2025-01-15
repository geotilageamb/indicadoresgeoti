import streamlit as st
import dashboard_indicadores
import dashboard_sla

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard de Indicadores GeoTI")

# Título principal
st.title('Dashboard de Indicadores GeoTI')

# Criação das abas principais
tab_indicadores, tab_sla = st.tabs([
    "Indicadores GeoTI",
    "SLA dos Chamados"
])

# Renderiza o dashboard de indicadores
with tab_indicadores:
    dashboard_indicadores.show_dashboard()

# Renderiza o dashboard de SLA
with tab_sla:
    dashboard_sla.show_dashboard()
