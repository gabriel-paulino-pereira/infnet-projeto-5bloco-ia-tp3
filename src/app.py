"""
Plataforma ESG - ODS 11 (Cidades e Comunidades Sustentáveis)
Arquivo Principal / Home Page
Descrição: Ponto de entrada da aplicação Streamlit estruturada em múltiplas páginas.
"""

import streamlit as st

# Configuro as propriedades globais da aplicação
st.set_page_config(
    page_title="Plataforma ESG - ODS 11",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e cabeçalho principal
st.title("🌱 Plataforma de Gestão Sustentável e ODS 11")
st.caption("Solução para monitoramento de indicadores urbanos e notícias ESG - Agenda 2030")

st.divider()

# Apresentação do projeto e contextualização
st.markdown("""
### 📌 Bem-vindo à Plataforma de Inteligência ESG
Esta aplicação foi desenvolvida para consolidar, analisar e disponibilizar informações sobre **sustentabilidade urbana**, alinhada ao **ODS 11 (Cidades e Comunidades Sustentáveis)**.

Utilize o **menu de navegação à esquerda** para alternar entre as seções da plataforma:

1. **📊 Painel Principal:** Visualização de indicadores, tabela de notícias coletadas e filtros dinâmicos.
2. **📁 Gestão de Arquivos:** Central de upload e download de arquivos CSV para integração de novos lotes de dados.
3. **⚡ Integração FastAPI:** Monitoramento e consulta à API RESTful desenvolvida em FastAPI.
4. **🤖 Preparação para IA:** Visão geral da estruturação de dados textuais para pipelines de LLMs (TP4).
""")

st.divider()

# Destaques dos Objetivos ESG
col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 🏙️ ODS 11\nCidades e Comunidades Sustentáveis: Foco em mobilidade, gestão de resíduos e resiliência urbana.")

with col2:
    st.success("### 🔄 ODS 12\nConsumo e Produção Responsáveis: Monitoramento de eficiência energética e descarte adequado.")

with col3:
    st.warning("### 🧠 Inteligência Artificial\nPreparação de corpora textuais para sumarização automática e classificação de sentimento.")