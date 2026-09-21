"""
Aplicação Streamlit - TP2: Gestão ESG e ODS 11
Descrição: Adição de serviços de upload (st.file_uploader) e download (st.download_button)
para arquivos CSV, integrados ao estado da sessão (st.session_state) e cache.
"""

import os
import streamlit as st
import pandas as pd

# Defino as configurações da interface com layout amplo
st.set_page_config(
    page_title="Painel ESG & ODS 11",
    page_icon="🌱",
    layout="wide"
)

# Renderizo a identidade visual da aplicação
st.title("🌱 Plataforma de Gestão Sustentável e ODS 11")
st.caption("Evolução TP2: Cache, Session State e Serviços de Upload/Download de Dados")
st.divider()

# ==========================================================
# 1. IMPLEMENTAÇÃO DE CACHE (@st.cache_data)
# ==========================================================
@st.cache_data(show_spinner="Carregando dados raspados do disco...")
def carregar_dados_raspados():
    """
    Realizo a leitura em disco dos dados coletados pelo scraping.
    Armazeno em cache para evitar leituras repetitivas do sistema de arquivos.
    """
    caminho_csv = os.path.join("data", "raw", "noticias_sustentabilidade.csv")
    caminho_txt = os.path.join("data", "raw", "corpus_noticias.txt")
    
    # Inspeciono a existência prévia dos arquivos
    if os.path.exists(caminho_csv):
        df = pd.read_csv(caminho_csv)
    else:
        df = pd.DataFrame(columns=["Titulo", "Resumo", "Link"])
        
    texto_corpus = ""
    if os.path.exists(caminho_txt):
        with open(caminho_txt, "r", encoding="utf-8") as f:
            texto_corpus = f.read()
            
    return df, texto_corpus

# Executo a função cacheada
df_base, corpus_texto = carregar_dados_raspados()

# ==========================================================
# 2. IMPLEMENTAÇÃO DE ESTADO DE SESSÃO (st.session_state)
# ==========================================================
if "noticias_ativas" not in st.session_state:
    st.session_state.noticias_ativas = df_base.copy()

if "total_interacoes" not in st.session_state:
    st.session_state.total_interacoes = 0

# Função auxiliar para converter o DataFrame em CSV pronto para download
@st.cache_data
def converter_df_para_csv(df):
    """
    Converto o DataFrame em bytes codificados em UTF-8 com BOM (utf-8-sig)
    para garantir compatibilidade ao abrir diretamente no Excel.
    """
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

# ==========================================================
# 3. BARRA LATERAL (CONTROLES E INSERÇÃO MANUAL)
# ==========================================================
with st.sidebar:
    st.header("⚙️ Painel de Controle")
    st.metric(label="Total de Interações", value=st.session_state.total_interacoes)
    st.metric(label="Registros Ativos", value=len(st.session_state.noticias_ativas))
    
    st.divider()
    
    st.subheader("➕ Inserção Individual")
    novo_titulo = st.text_input("Título:")
    novo_resumo = st.text_area("Resumo:")
    novo_link = st.text_input("Link:", value="https://")
    
    if st.button("Adicionar Registro"):
        if novo_titulo.strip() and novo_resumo.strip():
            novo_registro = pd.DataFrame([{
                "Titulo": novo_titulo.strip(),
                "Resumo": novo_resumo.strip(),
                "Link": novo_link.strip()
            }])
            
            # Adiciono ao DataFrame persistido na sessão
            st.session_state.noticias_ativas = pd.concat(
                [novo_registro, st.session_state.noticias_ativas], 
                ignore_index=True
            )
            st.session_state.total_interacoes += 1
            st.success("Registro adicionado com sucesso!")
            st.rerun()
        else:
            st.warning("Preencha título e resumo para adicionar.")

    if st.button("Restaurar Base Padrão"):
        st.session_state.noticias_ativas = df_base.copy()
        st.session_state.total_interacoes = 0
        st.info("Base restaurada com sucesso.")
        st.rerun()

# ==========================================================
# 4. ÁREA PRINCIPAL: NAVEGAÇÃO E SERVIÇO DE ARQUIVOS
# ==========================================================

aba_dados, aba_arquivos = st.tabs(["📋 Registros em Memória", "📁 Central de Upload / Download"])

with aba_dados:
    st.subheader("Base Operacional de Notícias e Sustentabilidade")
    st.markdown(
        "A tabela abaixo reflete as informações atualmente carregadas em memória no sistema. "
        "Novos dados inseridos manualmente ou via upload CSV são consolidados dinamicamente nesta visualização."
    )
    st.dataframe(
        st.session_state.noticias_ativas,
        use_container_width=True,
        hide_index=True
    )

with aba_arquivos:
    st.subheader("Gerenciamento de Arquivos CSV")
    st.markdown(
        "Utilize esta seção para exportar a base de dados consolidada ou importar novos lotes de "
        "registros para enriquecer a aplicação."
    )
    
    col_upload, col_download = st.columns(2)
    
    # --- SERVIÇO DE DOWNLOAD ---
    with col_download:
        st.markdown("#### 📥 Exportar Dados")
        st.write("Faça o download de todos os dados ativos no sistema em formato `.csv`:")
        
        csv_bytes = converter_df_para_csv(st.session_state.noticias_ativas)
        
        st.download_button(
            label="Baixar Base de Dados (CSV)",
            data=csv_bytes,
            file_name="base_consolidada_sustentabilidade.csv",
            mime="text/csv",
            key="btn_download_csv"
        )
        st.caption("Arquivo exportado com codificação UTF-8.")
        
    # --- SERVIÇO DE UPLOAD ---
    with col_upload:
        st.markdown("#### 📤 Importar Novos Dados")
        st.write("Envie um arquivo CSV contendo colunas compatíveis (`Titulo`, `Resumo`, `Link`):")
        
        arquivo_enviado = st.file_uploader(
            "Selecione um arquivo CSV para upload",
            type=["csv"],
            key="uploader_csv"
        )
        
        if arquivo_enviado is not None:
            try:
                # Realizo a leitura do arquivo enviado pelo usuário
                df_upload = pd.read_csv(arquivo_enviado)
                
                # Valido se as colunas essenciais estão presentes
                colunas_obrigatorias = {"Titulo", "Resumo", "Link"}
                if colunas_obrigatorias.issubset(set(df_upload.columns)):
                    st.write(f"Arquivo lido com sucesso: **{len(df_upload)}** novos registros encontrados.")
                    
                    if st.button("Integrar Dados ao Sistema"):
                        # Concateno os novos dados à sessão existente
                        st.session_state.noticias_ativas = pd.concat(
                            [st.session_state.noticias_ativas, df_upload],
                            ignore_index=True
                        ).drop_duplicates(subset=["Titulo"]) # Evito duplicidades pelo título
                        
                        st.session_state.total_interacoes += 1
                        st.success("Dados integrados com sucesso à base principal!")
                        st.rerun()
                else:
                    st.error("O arquivo CSV enviado não contém as colunas necessárias: 'Titulo', 'Resumo', 'Link'.")
            except Exception as e:
                st.error(f"Erro ao processar o arquivo CSV: {e}")