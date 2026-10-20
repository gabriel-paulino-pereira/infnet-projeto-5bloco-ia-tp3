"""
Página 4: Preparação e Planejamento para LLMs (TP3 / TP4)
Descrição: Interface interativa para sanitização do corpus e visualização
dos dados estruturados para inferência em modelos de linguagem.
"""

import os
import json
import streamlit as st
import pandas as pd
from src.data.preparacao_llm import processar_corpus_para_llm

st.set_page_config(page_title="Preparação para IA - ESG", page_icon="🤖", layout="wide")

st.title("🤖 Preparação de Dados para Recursos de IA (LLMs)")
st.caption("Tratamento de texto, sanitização e estruturação em JSON para os casos de uso do TP4.")

# Apresentação dos casos de uso de IA
st.markdown("""
### 🎯 Casos de Uso Estruturados para o TP4:

1. **📝 Sumarização Automática:** Síntese de matérias e relatórios em pontos focais de impacto ambiental.
2. **🏷️ Classificação de Sentimento ESG:** Rotação de textos para rótulos (*Positivo*, *Neutro*, *Alerta de Risco*).
3. **💬 Sistema de Perguntas e Respostas (Q&A / RAG):** Vetorização dos documentos para consultas contextuais.
""")

st.divider()

# Painel de execução do pipeline de sanitização
st.subheader("⚙️ Pipeline de Sanitização e Tokenização")

col1, col2 = st.columns([1, 2])

with col1:
    st.write("Clique no botão abaixo para processar o corpus bruto acumulado (`data/raw/corpus_noticias.txt`) e gerar o schema JSON sanitizado:")
    if st.button("Executar Sanitização para LLM"):
        docs = processar_corpus_para_llm()
        st.success(f"Pipeline concluído! {len(docs)} documentos sanitizados com sucesso.")
        st.rerun()

# Leitura e exibição do JSON processado
caminho_json = os.path.join("data", "processed", "dataset_llm_prep.json")

with col2:
    if os.path.exists(caminho_json):
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados_llm = json.load(f)
        
        st.metric("Total de Documentos Prontos para IA", len(dados_llm))
        df_llm = pd.DataFrame(dados_llm)
        st.dataframe(df_llm[["id", "texto", "tamanho_caracteres"]], use_container_width=True, hide_index=True)
    else:
        st.info("O dataset sanitizado ainda não foi gerado. Clique no botão ao lado para executar.")