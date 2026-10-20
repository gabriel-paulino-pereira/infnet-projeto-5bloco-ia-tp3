"""
Script de Web Scraping Dinâmico com Selenium
Descrição: Automatiza a navegação em páginas dinâmicas para extrair notícias
e atualiza a base mantida em data/raw/.
"""

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuro caminhos e arquivos de saída
DIRETORIO_SAIDA = os.path.join("data", "raw")
os.makedirs(DIRETORIO_SAIDA, exist_ok=True)

ARQUIVO_CSV_DINAMICO = os.path.join(DIRETORIO_SAIDA, "noticias_dinamicas.csv")
ARQUIVO_TXT = os.path.join(DIRETORIO_SAIDA, "corpus_noticias.txt")

# Defino as opções do Chrome para execução em segundo plano (headless)
opcoes_chrome = Options()
opcoes_chrome.add_argument("--headless")
opcoes_chrome.add_argument("--no-sandbox")
opcoes_chrome.add_argument("--disable-dev-shm-usage")
opcoes_chrome.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

print("Iniciando o navegador Selenium em modo headless...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opcoes_chrome
)

try:
    # Acesso a página de notícias com carregamento assíncrono
    URL_ALVO = "https://agenciabrasil.ebc.com.br/geral"
    driver.get(URL_ALVO)
    
    # Aguardo a renderização dinâmica dos elementos no DOM
    time.sleep(4)
    
    # Localizo os títulos e links dinâmicos na árvore HTML
    elementos_links = driver.find_elements(By.CSS_SELECTOR, "h2 a, h3 a, .view-content a")
    
    lista_noticias = []
    textos_acumulados = []
    links_processados = set()
    
    for el in elementos_links:
        try:
            titulo = el.text.strip()
            link = el.get_attribute("href")
            
            if titulo and len(titulo) > 20 and link not in links_processados:
                links_processados.add(link)
                
                # Busco o elemento pai para extrair resumos associados
                resumo = ""
                try:
                    pai = el.find_element(By.XPATH, "./ancestor::article | ./ancestor::div[contains(@class, 'views-row')]")
                    paragrafo = pai.find_element(By.TAG_NAME, "p")
                    resumo = paragrafo.text.strip()
                except Exception:
                    resumo = "Resumo indisponível no carregamento dinâmico."
                
                lista_noticias.append({
                    "Titulo": titulo,
                    "Resumo": resumo,
                    "Link": link,
                    "Fonte": "Selenium_Dynamic"
                })
                textos_acumulados.append(f"{titulo}. {resumo}")
        except Exception:
            continue
            
    # Salvo os dados obtidos em arquivo CSV específico para raspagem dinâmica
    df_dinamico = pd.DataFrame(lista_noticias)
    df_dinamico.to_csv(ARQUIVO_CSV_DINAMICO, index=False, encoding="utf-8-sig")
    
    # Anexo os novos textos ao corpus acumulado
    if textos_acumulados:
        with open(ARQUIVO_TXT, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(textos_acumulados))
            
    print(f"Sucesso: {len(df_dinamico)} noticias dinâmicas extraídas e salvas em '{ARQUIVO_CSV_DINAMICO}'.")

finally:
    # Encerro a sessão do Selenium WebDriver
    driver.quit()