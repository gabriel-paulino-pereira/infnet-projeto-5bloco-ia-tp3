"""
API RESTful com FastAPI - Plataforma ESG / ODS 11
Descrição: Servidor backend para disponibilizar rotas de consulta (GET) e
envio de dados (POST) sobre sustentabilidade e notícias urbanas.
"""

import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Instancio a aplicação FastAPI com metadados para documentação OpenAPI
app = FastAPI(
    title="API de Gestão ESG & ODS 11",
    description="Interface RESTful para consulta e ingestão de dados sobre cidades sustentáveis.",
    version="1.0.0"
)

# Defino o schema do Pydantic para validação do corpo das requisições POST
class NoticiaSchema(BaseModel):
    Titulo: str
    Resumo: str
    Link: str
    Fonte: Optional[str] = "API_Post"

# Função utilitária para carregar os dados dos arquivos CSV para a memória
def carregar_base_dados():
    caminho_estatico = os.path.join("data", "raw", "noticias_sustentabilidade.csv")
    caminho_dinamico = os.path.join("data", "raw", "noticias_dinamicas.csv")
    
    dfs = []
    if os.path.exists(caminho_estatico):
        df_est = pd.read_csv(caminho_estatico)
        if "Fonte" not in df_est.columns:
            df_est["Fonte"] = "BeautifulSoup_Static"
        dfs.append(df_est)
        
    if os.path.exists(caminho_dinamico):
        df_din = pd.read_csv(caminho_dinamico)
        if "Fonte" not in df_din.columns:
            df_din["Fonte"] = "Selenium_Dynamic"
        dfs.append(df_din)
        
    if dfs:
        df_consolidado = pd.concat(dfs, ignore_index=True).drop_duplicates(subset=["Titulo"])
        # Limpo valores nulos para não quebrar a serialização JSON
        df_consolidado["Resumo"] = df_consolidado["Resumo"].fillna("Resumo não disponível.")
        df_consolidado["Fonte"] = df_consolidado["Fonte"].fillna("Desconhecida")
        df_consolidado["id"] = range(1, len(df_consolidado) + 1)
        return df_consolidado
    
    return pd.DataFrame(columns=["id", "Titulo", "Resumo", "Link", "Fonte"])

# Base de dados em memória inicial
base_noticias = carregar_base_dados()


@app.get("/", summary="Rota Raiz", tags=["Geral"])
def rota_raiz():
    """Retorna mensagem de verificação de status do servidor."""
    return {"status": "Online", "mensagem": "API ESG & ODS 11 operacional."}


@app.get("/noticias", summary="Listar Notícias", tags=["Notícias"])
def listar_noticias():
    """
    **Rota GET:** Retorna a lista completa de notícias de sustentabilidade
    cadastradas na base de dados.
    """
    try:
        # Converto e garanto tratamento de NaNs para evitar erro de serialização
        dados = base_noticias.fillna("").to_dict(orient="records")
        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar dados: {str(e)}")


@app.get("/noticias/{noticia_id}", summary="Consultar Notícia por ID", tags=["Notícias"])
def obter_noticia_por_id(noticia_id: int):
    """
    **Rota GET com Parâmetro:** Consulta e retorna uma notícia específica
    com base no seu identificador numérico (`id`).
    """
    registro = base_noticias[base_noticias["id"] == noticia_id]
    if registro.empty:
        raise HTTPException(status_code=404, detail="Notícia não encontrada com o ID informado.")
    return registro.fillna("").to_dict(orient="records")[0]


@app.post("/noticias", summary="Cadastrar Nova Notícia", tags=["Notícias"], status_code=201)
def cadastrar_noticia(nova_noticia: NoticiaSchema):
    """
    **Rota POST:** Recebe um objeto JSON com os campos `Titulo`, `Resumo` e `Link`,
    valida a estrutura via Pydantic e adiciona o novo registro à base de dados.
    """
    global base_noticias
    
    novo_id = len(base_noticias) + 1 if not base_noticias.empty else 1
    
    novo_registro = {
        "id": novo_id,
        "Titulo": nova_noticia.Titulo,
        "Resumo": nova_noticia.Resumo,
        "Link": nova_noticia.Link,
        "Fonte": nova_noticia.Fonte
    }
    
    df_novo = pd.DataFrame([novo_registro])
    base_noticias = pd.concat([base_noticias, df_novo], ignore_index=True)
    
    return {
        "mensagem": "Notícia cadastrada com sucesso via API!",
        "registro": novo_registro
    }