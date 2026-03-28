IntegraHub Dashboard

Dashboard interativo de indicadores econômicos globais com foco em análise de dados, visualização e pipeline ETL.

📌 Visão Geral

O IntegraHub é uma aplicação desenvolvida em Streamlit que consome dados públicos da API do World Bank e os transforma em visualizações analíticas interativas.

Permite explorar indicadores como:

Desemprego
Gastos em saúde
Investimentos

Com foco em análise temporal e comparação entre países.

🧱 Arquitetura
app.py          → Interface (Streamlit)
etl.py          → Pipeline ETL (World Bank API)
charts.py       → Visualizações (Plotly)
database.py     → Estrutura inicial de banco (SQLite)
repository.py   → Camada de dados (em evolução)
⚙️ Pipeline ETL
1. Extract
Consumo da API do World Bank
Paginação automática
Tratamento de erros
2. Transform
Normalização dos dados
Conversão de tipos
Remoção de regiões agregadas
3. Load
Consolidação em DataFrame
Cache com st.cache_data
📊 Funcionalidades
✅ Implementadas
Coleta de dados em tempo real
Filtro por país
KPIs agregados
Gráficos interativos
Comparação entre países
Ranking global por ano
Interface customizada (CSS)

🚧 Em desenvolvimento
Persistência em banco
Camada de repositório
Exportação de dados
Otimização de performance

📈 Indicadores
Desemprego → SL.UEM.TOTL.ZS
Saúde (% PIB) → SH.XPD.CHEX.GD.ZS
Investimentos (% PIB) → NE.GDI.TOTL.ZS

Fonte: World Bank API

🛠️ Tecnologias
Python
Streamlit
Pandas
Plotly
Requests
SQLite

🚀 Execução
git clone https://github.com/seu-usuario/integrahub
cd integrahub

pip install -r requirements.txt

streamlit run app.py

⚠️ Limitações
Dependência de API externa
Sem persistência ativa
Sem autenticação
Acoplamento entre ETL e UI
