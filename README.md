## IntegraHub Dashboard

Dashboard interativo de indicadores econômicos globais construído com foco em análise de dados, visualização e pipeline ETL.

📌 Visão Geral

O IntegraHub é uma aplicação desenvolvida em Streamlit que consome dados públicos do World Bank e os transforma em visualizações analíticas interativas.

O sistema permite explorar indicadores globais como:

Desemprego
Gastos em saúde
Investimentos

com foco em comparação entre países e análise temporal.

🧱 Arquitetura

O projeto segue uma separação clara de responsabilidades:

app.py          → Interface e layout (Streamlit)
etl.py          → Coleta e transformação de dados (World Bank API)
charts.py       → Construção dos gráficos (Plotly)
database.py     → Estrutura inicial de persistência (SQLite - opcional)
repository.py   → Camada de acesso a dados (em evolução)
⚙️ Pipeline de Dados (ETL)

O fluxo de dados é composto por:

Extract
Consumo da API do World Bank
Paginação automática
Tratamento de falhas de requisição
Transform
Normalização dos dados
Conversão de tipos
Remoção de regiões agregadas
Load
Consolidação em DataFrame único
Cache com st.cache_data para performance
📊 Funcionalidades
✅ Implementadas
Coleta de dados globais em tempo real
Filtro por país
KPIs agregados
Gráficos interativos (linha e barra)
Comparação entre múltiplos países
Ranking global por ano
Interface customizada com CSS
🚧 Em desenvolvimento
Persistência em banco de dados
Camada de repositório estruturada
Exportação de dados
Melhorias de performance
📈 Indicadores Utilizados
Desemprego: SL.UEM.TOTL.ZS
Saúde (% PIB): SH.XPD.CHEX.GD.ZS
Investimentos (% PIB): NE.GDI.TOTL.ZS

Fonte: World Bank API

🛠️ Tecnologias
Python
Streamlit
Pandas
Plotly
Requests
SQLite (estrutura inicial)
🚀 Como rodar o projeto
git clone https://github.com/seu-usuario/integrahub
cd integrahub

pip install -r requirements.txt

streamlit run app.py
⚠️ Limitações
Dependência direta de API externa (latência e disponibilidade)
Sem persistência ativa de dados
Sem autenticação ou multiusuário
Alto acoplamento entre ETL e camada de visualização
