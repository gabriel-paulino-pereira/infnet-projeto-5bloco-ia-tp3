# Data Summary Report - Consolidação e Governança de Dados

## 1. Visão Geral da Ingestão de Dados
O projeto adota uma estratégia mista de aquisição de dados, combinando a extração externa automatizada com a capacidade de ingestão contínua por meio de arquivos fornecidos pelo usuário. Todos os dados são convertidos para estruturas tabulares processáveis (`pandas.DataFrame`) e preservados em disco ou em memória de sessão.

---

## 2. Mapeamento Detalhado das Fontes de Dados

| Identificador | Origem / Fonte | Formato / Protocolo | Script / Módulo | Armazenamento | Finalidade Analítica |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SRC-01** | Agência Brasil (EBC) - Editoria Geral | HTML / Web Scraping (`BeautifulSoup`) | `src/data/scraping_noticias.py` | `data/raw/noticias_sustentabilidade.csv` | Fornecer notícias reais sobre cidades, clima e saneamento para análise temática e extração de insights. |
| **SRC-02** | Agência Brasil (EBC) - Corpus Consolidado | Texto Plano (`.txt`) | `src/data/scraping_noticias.py` | `data/raw/corpus_noticias.txt` | Servir de base textual contínua para análises de processamento de linguagem natural e geração de nuvem de palavras. |
| **SRC-03** | Arquivos CSV de Usuário (Upload) | CSV / Multipart Upload (`st.file_uploader`) | `src/app.py` | `st.session_state.noticias_ativas` (Memória) | Permitir que gestores integrem bases de dados proprietárias para complementação analítica. |

---

## 3. Dicionário de Variáveis (Esquema Canônico)

A tabela principal de dados (`noticias_sustentabilidade.csv` e `st.session_state.noticias_ativas`) obedece ao seguinte schema:

| Nome da Coluna | Tipo de Dado | Obrigatório | Descrição | Exemplo de Valor |
| :--- | :--- | :--- | :--- | :--- |
| `Titulo` | Texto (`object` / `string`) | Sim | Título ou manchete da publicação. Utilizado como chave primária de unicidade para evitar duplicatas. | *"Prefeitura expande programa de coleta seletiva"* |
| `Resumo` | Texto (`object` / `string`) | Sim | Texto introdutório, lide ou síntese do fato noticiado. | *"Nova diretriz abrange 15 bairros com foco em reciclagem."* |
| `Link` | Texto (`object` / `string`) | Sim | Endereço URL completo apontando para a fonte pública original da informação. | `"https://agenciabrasil.ebc.com.br/geral/noticia/..."` |

---

## 4. Avaliação de Qualidade e Tratamento dos Dados

1. **Remoção de Duplicidades:** 
   - No processo de upload e inserção manual, aplico deduplicação automática baseada na coluna `Titulo` através do método `drop_duplicates()`.
2. **Normalização de Links:**
   - O script de scraping valida e converte links relativos (`/geral/...`) em URLs absolutas (`https://agenciabrasil.ebc.com.br/...`).
3. **Consistência de Codificação:**
   - As exportações e gravações em disco utilizam a codificação `utf-8-sig` (UTF-8 com BOM) para evitar corrupção de acentuação e caracteres especiais em softwares de planilhas como o Microsoft Excel.
4. **Resiliência a Falhas:**
   - A função de carregamento (`carregar_dados_raspados`) implementa checagem de existência prévia de arquivos (`os.path.exists`), instanciando DataFrames vazios em caso de ausência e evitando quebras de execução.