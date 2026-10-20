"""
Página 2: Gestão de Arquivos CSV
Descrição: Permite upload e download de arquivos CSV para integração de novos dados.
"""

import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão de Arquivos - ESG", page_icon="📁", layout="wide")

st.title("📁 Central de Ingestão e Exportação de Dados")
st.caption("Serviço de importação (upload) e exportação (download) de bases em formato CSV.")

# Inicializo o estado da sessão caso ainda não exista
if "noticias_ativas" not in st.session_state:
    caminho_csv = os.path.join("data", "raw", "noticias_sustentabilidade.csv")
    if os.path.exists(caminho_csv):
        st.session_state.noticias_ativas = pd.read_csv(caminho_csv)
    else:
        st.session_state.noticias_ativas = pd.DataFrame(columns=["Titulo", "Resumo", "Link"])

@st.cache_data
def converter_df_para_csv(df):
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

col_up, col_down = st.columns(2)

with col_down:
    st.subheader("📥 Exportar Dados Ativos")
    st.write("Baixe a base de dados consolidada mantida na sessão:")
    csv_bytes = converter_df_para_csv(st.session_state.noticias_ativas)
    st.download_button(
        label="Download CSV Consolidado",
        data=csv_bytes,
        file_name="base_sustentabilidade_exportada.csv",
        mime="text/csv"
    )

with col_up:
    st.subheader("📤 Importar Novo Lote CSV")
    arquivo_enviado = st.file_uploader("Selecione um arquivo CSV com colunas Titulo, Resumo, Link", type=["csv"])
    
    if arquivo_enviado is not None:
        try:
            df_upload = pd.read_csv(arquivo_enviado)
            if {"Titulo", "Resumo", "Link"}.issubset(set(df_upload.columns)):
                st.success(f"{len(df_upload)} novos registros identificados.")
                if st.button("Anexar à Base Ativa"):
                    st.session_state.noticias_ativas = pd.concat(
                        [st.session_state.noticias_ativas, df_upload],
                        ignore_index=True
                    ).drop_duplicates(subset=["Titulo"])
                    st.success("Dados integrados com sucesso!")
                    st.rerun()
            else:
                st.error("O arquivo precisa conter as colunas 'Titulo', 'Resumo' e 'Link'.")
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")

st.divider()
st.subheader("📋 Tabela Ativa na Sessão")
st.dataframe(st.session_state.noticias_ativas, use_container_width=True, hide_index=True)