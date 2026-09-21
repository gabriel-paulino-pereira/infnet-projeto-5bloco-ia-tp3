"""
Script de Web Scraping - Coleta de Conteúdo Real (ODS 11)
Descrição: Coleta notícias reais da Agência Brasil utilizando BeautifulSoup
com seletores otimizados e armazena em CSV e TXT no diretório data/raw/.
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Defino a URL da editoria geral da Agência Brasil
URL_ALVO = "https://agenciabrasil.ebc.com.br/geral"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# Configuro os caminhos de saída no diretório data/raw
DIRETORIO_SAIDA = os.path.join("data", "raw")
os.makedirs(DIRETORIO_SAIDA, exist_ok=True)

ARQUIVO_CSV = os.path.join(DIRETORIO_SAIDA, "noticias_sustentabilidade.csv")
ARQUIVO_TXT = os.path.join(DIRETORIO_SAIDA, "corpus_noticias.txt")

# Realizo a requisição HTTP
resposta = requests.get(URL_ALVO, headers=HEADERS, timeout=15)

if resposta.status_code == 200:
    # Faço o parsing do documento HTML
    sopa = BeautifulSoup(resposta.text, "html.parser")
    
    lista_noticias = []
    textos_acumulados = []
    
    # Busco todos os links contidos em títulos h2 e h3 da listagem
    elementos_titulos = sopa.select("h2 a, h3 a, .view-content a")
    
    links_processados = set()
    
    for el in elementos_titulos:
        titulo = el.get_text(strip=True)
        link = el.get("href", "")
        
        # Filtro links curtos ou que não representam notícias reais
        if len(titulo) > 25 and link and link not in links_processados:
            links_processados.add(link)
            
            # Normalizo o endereço do link
            if link.startswith("/"):
                link = f"https://agenciabrasil.ebc.com.br{link}"
                
            # Localizo o parágrafo ou resumo associado ao elemento pai
            pai = el.find_parent(["div", "article", "li"])
            resumo = ""
            if pai:
                tag_resumo = pai.find("p")
                if tag_resumo:
                    resumo = tag_resumo.get_text(strip=True)
            
            # Adiciono o registro à lista estruturada
            lista_noticias.append({
                "Titulo": titulo,
                "Resumo": resumo,
                "Link": link
            })
            
            # Agrupo o conteúdo para a composição do corpus textual
            textos_acumulados.append(f"{titulo}. {resumo}".strip())
    
    # Converto em DataFrame e exporto para CSV
    df_noticias = pd.DataFrame(lista_noticias)
    df_noticias.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig")
    
    # Escrevo o corpus textual consolidado no arquivo TXT
    with open(ARQUIVO_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(textos_acumulados))
        
    print(f"Sucesso: {len(df_noticias)} noticias extraidas e salvas com sucesso.")
else:
    print(f"Falha ao acessar o site. Status code: {resposta.status_code}")