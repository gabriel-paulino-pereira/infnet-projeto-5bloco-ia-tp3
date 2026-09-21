# Project Charter - Plataforma de Gestão Sustentável e ESG (ODS 11)

## 1. Visão Geral e Justificativa do Projeto
O crescimento acelerado dos centros urbanos impõe desafios críticos de sustentabilidade, exigindo acompanhamento rigoroso do consumo de recursos, descarte de resíduos e disseminação de informações de impacto socioambiental. Este projeto desenvolve uma solução analítica e interativa em Python com o framework Streamlit, alinhada diretamente ao **ODS 11 (Cidades e Comunidades Sustentáveis)** e em consonância com o **ODS 12 (Consumo e Produção Responsáveis)** da Agenda 2030. 

A plataforma resolve a dispersão de dados ao consolidar notícias reais do setor via Web Scraping, possibilitar a importação de bases tabulares complementares e viabilizar o monitoramento integrado para tomada de decisão em ESG.

## 2. Objetivos de Negócio e Metas do Projeto
- **Centralização da Informação:** Coletar, processar e estruturar notícias públicas sobre sustentabilidade urbana através de extração automatizada.
- **Interatividade e Usabilidade:** Disponibilizar um painel responsivo com filtros, métricas dinâmicas e persistência de dados.
- **Flexibilidade Operacional:** Prover serviços de exportação e importação de bases de dados customizadas via arquivos CSV.
- **Eficiência Computacional:** Minimizar tempo de processamento por meio de rotinas de cache em memória (`@st.cache_data`) e gerenciamento de estado (`st.session_state`).

## 3. Escopo do Projeto

### No Escopo (Entregas TP1 e TP2):
- Implementação de arquitetura baseada no ciclo de vida TDSP e metodologia CRISP-DM.
- Coleta de dados reais via web scraping com a biblioteca `BeautifulSoup` em fontes públicas (Agência Brasil).
- Persistência dos dados estruturados em formatos `.csv` e corpus textual em `.txt` no diretório `data/raw/`.
- Aplicação web interativa desenvolvida em Streamlit com:
  - Cache de dados para otimização de leitura.
  - Estado de sessão para controle de dados em tempo de execução e contadores de auditoria.
  - Central de download e upload para arquivos CSV com validação de colunas.
  - Inserção manual dinâmica de registros sem reinício de processamento.
- Documentação formalizada em Markdown na pasta `docs/`.

### Fora do Escopo:
- Deploy automatizado em nuvem comercial com esteiras de CI/CD completas nesta etapa.
- Integração de modelos de aprendizado de máquina para predição numérica (planejada para etapas posteriores).
- Conexão direta com bancos de dados relacionais corporativos em produção.

## 4. Stakeholders e Papéis
- **Patrocinadores Acadêmicos / Avaliadores:** Professores e comissão avaliadora do Instituto Infnet.
- **Desenvolvedor e Analista de Dados:** Responsável pela arquitetura de dados, scripts de scraping, controle de versão e frontend em Streamlit.
- **Usuários Finais:** Gestores de sustentabilidade, analistas de ESG corporativos, secretarias de meio ambiente municipais e pesquisadores do terceiro setor.

## 5. Critérios de Sucesso e KPIs
- **Desempenho da Aplicação:** Latência de carregamento das tabelas em memória inferior a 1 segundo graças ao uso de `@st.cache_data`.
- **Integridade dos Dados:** Validação estrita das colunas obrigatórias (`Titulo`, `Resumo`, `Link`) no pipeline de upload.
- **Persistência Funcional:** Preservação de 100% dos dados adicionados durante a sessão do usuário via `st.session_state`.
- **Governança de Código:** Repositório estruturado seguindo rigorosamente o padrão TDSP com rastreabilidade via Git.