"""
Página 3: Painel de Integração FastAPI
Descrição: Interface para envio e consulta de dados em tempo real conectada à API REST.
"""

import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="API FastAPI - ESG", page_icon="⚡", layout="wide")

st.title("⚡ Interface de Comunicação com a API FastAPI")
st.caption("Consumo em tempo real dos endpoints RESTful desenvolvidos para a plataforma.")

URL_API = "http://127.0.0.1:8000"

# Verifico o status da API
st.subheader("📊 Status da Conexão Backend")

try:
    resposta_ping = requests.get(f"{URL_API}/", timeout=2)
    if resposta_ping.status_code == 200:
        st.success(f"Servidor FastAPI Conectado! Output: {resposta_ping.json()}")
        api_online = True
    else:
        st.error("Servidor respondeu com erro.")
        api_online = False
except Exception:
    st.warning("Servidor FastAPI deslogado ou inacessível no endereço http://127.0.0.1:8000.")
    st.info("Para iniciar a API no terminal execute: `uvicorn src.api.main:app --reload`")
    api_online = False

st.divider()

if api_online:
    tab_get, tab_post = st.tabs(["📥 Consultar Dados (GET /noticias)", "📤 Enviar Dados (POST /noticias)"])
    
    with tab_get:
        st.subheader("Notícias Retornadas pela API")
        res = requests.get(f"{URL_API}/noticias")
        if res.status_code == 200:
            dados = res.json()
            df_api = pd.DataFrame(dados)
            st.dataframe(df_api, use_container_width=True, hide_index=True)
        else:
            st.error("Erro ao buscar dados da API.")

    with tab_post:
        st.subheader("Cadastrar Novo Registro na API")
        
        with st.form("form_post_api"):
            titulo_in = st.text_input("Título:")
            resumo_in = st.text_area("Resumo:")
            link_in = st.text_input("Link:", value="https://")
            submitted = st.form_submit_button("Enviar para a API")
            
            if submitted:
                if titulo_in.strip() and resumo_in.strip():
                    payload = {
                        "Titulo": titulo_in.strip(),
                        "Resumo": resumo_in.strip(),
                        "Link": link_in.strip(),
                        "Fonte": "Streamlit_Frontend"
                    }
                    res_post = requests.post(f"{URL_API}/noticias", json=payload)
                    if res_post.status_code == 201:
                        st.success("Notícia enviada e cadastrada na API com sucesso!")
                        st.json(res_post.json())
                    else:
                        st.error(f"Erro ao enviar: {res_post.status_code}")
                else:
                    st.warning("Preencha título e resumo.")