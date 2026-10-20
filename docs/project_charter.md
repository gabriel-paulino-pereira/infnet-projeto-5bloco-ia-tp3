# Project Charter - Plataforma de Gestão Sustentável e ESG (ODS 11) - Fase TP3

## 1. Visão Geral e Justificativa do Projeto (Revisada - TP3)
O crescimento acelerado dos centros urbanos impõe desafios crescentes de gestão pública e privada, exigindo um acompanhamento ágil sobre consumo de recursos, descarte de resíduos e políticas sustentáveis. Este projeto evolui a solução analítica em Python para uma arquitetura orientada a microsserviços, integrando o frontend interativo em Streamlit a uma API RESTful em FastAPI e pipelines de raspagem dinâmica com Selenium. A solução permanece alinhada ao **ODS 11 (Cidades e Comunidades Sustentáveis)** e ao **ODS 12 (Consumo e Produção Responsáveis)** da Agenda 2030 das Nações Unidas.

Nesta terceira fase, amplia-se a capacidade de ingestão com captura de dados dinâmicos, desacopla-se o consumo de dados via endpoints REST e estrutura-se o ecossistema textual para futura integração com Large Language Models (LLMs).

## 2. Objetivos de Negócio e Metas Reavaliadas
- **Arquitetura Desacoplada e Escalável:** Construir uma API com FastAPI para servir dados de sustentabilidade via protocolos HTTP (`GET` e `POST`), garantindo a interoperabilidade com outros sistemas.
- **Captura Avançada de Dados (Scraping Dinâmico):** Expandir a extração de notícias e dados públicos utilizando `Selenium` para contornar renderizações assíncronas em JavaScript.
- **Navegação Modular (Multipáginas):** Reestruturar a interface gráfica em páginas independentes no Streamlit, melhorando a usabilidade e a distribuição das análises.
- **Preparação para Inteligência Artificial:** Estruturar e sanear os corpos textuais coletados para viabilizar tarefas de Processamento de Linguagem Natural (PLN) e modelos de linguagem (LLMs) no TP4.

## 3. Escopo do Projeto (Atualizado - TP3)

### No Escopo (Entregas TP1, TP2 e TP3):
- **Evolução de Arquitetura:** Estruturação da aplicação multipáginas no Streamlit no diretório `pages/`.
- **Backend com FastAPI:** Implementação do servidor web em `src/api/main.py` com rotas documentadas (`/docs` e `/redoc`).
- **Scraping Dinâmico:** Script em Python utilizando `Selenium WebDriver` para extração em portais com carregamento via script/AJAX.
- **Consumo de API:** Frontend Streamlit realizando requisições assíncronas/HTTP para a API em FastAPI.
- **Governança e Preparação para IA:** Mapeamento de casos de uso para LLMs (resumos automáticos, análise de sentimento e Q&A).
- **Documentação de Processo:** Atualização completa dos relatórios TDSP/CRISP-DM na pasta `docs/`.

### Fora do Escopo:
- Fine-tuning ou treinamento do zero de LLMs proprietárias (serão utilizadas APIs/modelos pré-treinados na etapa TP4).
- Implantação do servidor FastAPI em contêineres Docker em ambiente de produção (Kubernetes/AWS).

## 4. Stakeholders e Papéis
- **Avaliadores e Docentes:** Professores e comissão técnica do Instituto Infnet.
- **Desenvolvedor e Engenheiro de Dados:** Responsável pela construção dos pipelines de raspagem (Selenium/BeautifulSoup), desenvolvimento da API em FastAPI e arquitetura Streamlit.
- **Gestores Urbanos e Analistas ESG:** Usuários finais que utilizam a plataforma para visualização de indicadores e consulta de notícias.

## 5. Critérios de Sucesso e KPIs (Fase TP3)
- **Disponibilidade da API:** Resposta dos endpoints `/noticias` em tempo inferior a 300ms.
- **Eficácia da Raspagem Dinâmica:** Coleta bem-sucedida de elementos dinâmicos sem falhas de timeout com Selenium.
- **Modularidade da Interface:** Navegação fluida entre pelo menos 4 páginas estruturadas na aplicação.
- **Prontidão para LLMs:** Base textual rotulada e sanitizada pronta para pipelines de embeddings e inferência.