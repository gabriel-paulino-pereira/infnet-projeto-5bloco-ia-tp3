"""
Página 1: Painel Principal e Visualização de Dados
Descrição: Exibe notícias salvas no disco (via scraping), métricas e busca por palavras-chave.
"""

import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Painel Principal - ESG", page_icon="📊", layout="wide")

st.title("📊 Painel de Monitoramento de Notícias e Notificações")
st.caption("Consolidação de conteúdos coletados via rotinas automatizadas de Web Scraping.")

# Função cacheada para carregar a base de dados
@st.cache_data(show_spinner="Carregando dados da base...")
def carregar_dados():
    caminho_csv = os.path.join("data", "raw", "noticias_sustentabilidade.csv")
    if os.path.exists(caminho_csv):
        return pd.read_csv(caminho_csv)
    return pd.DataFrame(columns=["Titulo", "Resumo", "Link"])

df_noticias = carregar_dados()

# Métricas rápidas no topo
col1, col2, col3 = st.columns(3)
col1.metric("Total de Notícias Coletadas", len(df_noticias))
col2.metric("Fonte Principal", "Agência Brasil")
col3.metric("Status do Pipeline", "Ativo / Atualizado")

st.divider()

# Filtro de busca por palavra-chave na interface
termo_busca = st.text_input("🔍 Pesquisar por termo no título ou resumo:", "")

if termo_busca.strip():
    df_filtrado = df_noticias[
        df_noticias["Titulo"].str.contains(termo_busca, case=False, na=False) |
        df_noticias["Resumo"].str.contains(termo_busca, case=False, na=False)
    ]
    st.write(f"Exibindo **{len(df_filtrado)}** resultados para '{termo_busca}':")
else:
    df_filtrado = df_noticias

# Exibição dos dados
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)