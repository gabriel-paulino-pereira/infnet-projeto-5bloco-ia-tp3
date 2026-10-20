"""
Módulo de Preparação e Sanitização para LLMs (TP3/TP4)
Descrição: Lê os dados brutos acumulados, limpa ruídos de scraping,
divide os textos em blocos (chunks) e exporta em formato JSON para o pipeline de IA.
"""

import os
import re
import json
import pandas as pd

# Defino caminhos de entrada e saída
DIRETORIO_RAW = os.path.join("data", "raw")
DIRETORIO_PROCESSED = os.path.join("data", "processed")
os.makedirs(DIRETORIO_PROCESSED, exist_ok=True)

ARQUIVO_TXT = os.path.join(DIRETORIO_RAW, "corpus_noticias.txt")
ARQUIVO_JSON_LLM = os.path.join(DIRETORIO_PROCESSED, "dataset_llm_prep.json")

def limpar_texto(texto: str) -> str:
    """Realizo a limpeza de ruídos, espaços duplicados e quebras de linha."""
    texto = re.sub(r'\s+', ' ', texto)  # Remove múltiplos espaços e novas linhas
    texto = re.sub(r'Resumo indisponível.*', '', texto)  # Remove mensagens padrão de fallback
    return texto.strip()

def processar_corpus_para_llm():
    """Gero um dataset sanitizado e estruturado para tarefas de PLN / LLM."""
    if not os.path.exists(ARQUIVO_TXT):
        print(f"Aviso: Arquivo '{ARQUIVO_TXT}' não encontrado.")
        return []

    with open(ARQUIVO_TXT, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    documentos_preparados = []
    
    for idx, linha in enumerate(linhas, start=1):
        texto_limpo = limpar_texto(linha)
        if len(texto_limpo) > 15:  # Filtro textos insignificantes
            documentos_preparados.append({
                "id": idx,
                "texto": texto_limpo,
                "tamanho_caracteres": len(texto_limpo),
                "tarefas_recomendadas": ["Sumarização", "Classificação de Sentimento", "Q&A"]
            })

    # Salvo o dataset estruturado em JSON
    with open(ARQUIVO_JSON_LLM, "w", encoding="utf-8") as f_out:
        json.dump(documentos_preparados, f_out, ensure_ascii=False, indent=4)

    print(f"Sucesso: {len(documentos_preparados)} documentos sanitizados e salvos em '{ARQUIVO_JSON_LLM}'.")
    return documentos_preparados

if __name__ == "__main__":
    processar_corpus_para_llm()