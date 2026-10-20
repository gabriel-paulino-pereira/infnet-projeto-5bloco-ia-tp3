# Data Summary Report - Consolidação e Governança de Dados - Fase TP3

## 1. Visão Geral da Ingestão de Dados
Na fase TP3, a estratégia de aquisição de dados foi expandida para suportar interações dinâmicas e distribuição via microsserviços. Os dados agora alimentam tanto arquivos físicos no diretório `data/raw/` quanto o serviço em memória servido pela API em **FastAPI**, que passa a intermediar a entrega para o frontend em Streamlit.

---

## 2. Mapeamento Detalhado das Fontes de Dados (Incluindo Scraping Dinâmico)

| Identificador | Origem / Fonte | Formato / Protocolo | Script / Módulo | Armazenamento | Finalidade Analítica / Uso em IA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SRC-01** | Agência Brasil (EBC) - Estático | HTML / Web Scraping (`BeautifulSoup`) | `src/data/scraping_noticias.py` | `data/raw/noticias_sustentabilidade.csv` | Fornecer notícias sobre sustentabilidade urbana e ODS 11. |
| **SRC-02** | Corpus Textual Agregado | Texto Plano (`.txt`) | `src/data/scraping_noticias.py` | `data/raw/corpus_noticias.txt` | Base para sumarização e extração de palavras-chave via LLM. |
| **SRC-03** | Portais de Notícias Urbanas (Dinâmico) | HTML + JS / Selenium WebDriver | `src/data/scraping_dinamico.py` | `data/raw/noticias_dinamicas.csv` | Capturar conteúdos que exigem renderização assíncrona ou rolar de tela. |
| **SRC-04** | Arquivos CSV de Usuário (Upload) | CSV / Form Upload | `pages/2_📁_Gestao_Arquivos.py` | `st.session_state` / API | Permitir que gestores injetem bases proprietárias na sessão. |
| **SRC-05** | Servidor de Dados REST | JSON / HTTP (FastAPI) | `src/api/main.py` | Memória / JSON | Prover rotas `GET` e `POST` padronizadas para consumo da aplicação. |

---

## 3. Dicionário de Variáveis do Schema Expandido

A tabela abaixo descreve o contrato de dados mantido pela API e consumido pela interface gráfica:

| Nome do Campo | Tipo na API | Tipo em Pandas | Descrição | Exemplo de Conteúdo |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `integer` | `int64` | Identificador único numérico do registro. | `1` |
| `Titulo` | `string` | `object` | Título ou manchete da publicação sobre ESG/ODS 11. | *"Expansão de parques solares em áreas urbanas"* |
| `Resumo` | `string` | `object` | Breve descrição ou lide da matéria. | *"Projeto prevê redução de 20% na pegada de carbono."* |
| `Link` | `string` | `object` | Endereço URL completo da fonte da notícia. | `"https://agenciabrasil.ebc.com.br/..."` |
| `Fonte` | `string` | `object` | Mapeamento da origem (`BeautifulSoup`, `Selenium` ou `Manual`). | `"Selenium_Scraper"` |

---

## 4. Governança, Tratamento e Preparação para LLMs

1. **Padronização RESTful:**
   - A conversão entre os dados em disco/memória e as respostas HTTP é tratada utilizando modelos Pydantic na API, garantindo tipagem forte e validação automática.
2. **Sanitização de Texto para Modelos de Linguagem:**
   - Caracteres especiais, quebras de linha duplicadas e marcas d'água de scraping são limpos antes do armazenamento no corpus textual, preparando os dados para etapas de embeddings e prompts.
3. **Controle de Redundância:**
   - A inclusão de novos registros via endpoint `POST` da FastAPI realiza checagem de duplicidade com base no título da matéria.