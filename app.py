import streamlit as st
import pandas as pd
from etl import run_etl
import charts

st.set_page_config(
    page_title="IntegraHub Dashboard",
    layout="wide",
)

# ============================================================
# CSS PREMIUM 2.0
# ============================================================

st.markdown("""
<style>

body {
    background-color: #F7F9FC;
}

/* Título principal */
h1 {
    font-weight: 800 !important;
    color: #1F2937 !important;
}

/* Subtítulo */
h3 {
    color: #4B5563 !important;
    font-weight: 500 !important;
}

/* Cards de KPI */
.card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F4F7FF 100%);
    padding: 22px 24px;
    border-radius: 18px;
    border: 1px solid #E4E8F2;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    gap: 18px;
    transition: all 0.25s ease-in-out;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

/* Ícone do card */
.card-icon {
    background: #E9EDFA;
    padding: 16px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Título do KPI */
.card-title {
    font-size: 15px;
    font-weight: 600;
    color: #6B7280;
}

/* Valor do KPI */
.card-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 3px;
    color: #111827;
}

/* Subtítulos de seção */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #1F2937;
    margin-top: 40px;
    border-left: 4px solid #3B82F6;
    padding-left: 10px;
}

/* Separador elegante */
.divider {
    height: 1px;
    background: linear-gradient(to right, #D1D5DB, #F3F4F6);
    margin: 25px 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div style='margin-bottom: 10px;'>
    <h1>IntegraHub</h1>
    <h3>Dashboard Global de Indicadores Econômicos e Sociais</h3>
</div>
""", unsafe_allow_html=True)


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

df = run_etl()

# Lista de países dinâmica
paises = sorted(df["regiao"].unique()) if not df.empty else []
paises = ["Todos"] + paises

selected_country = st.selectbox("Selecione um país:", paises)

if selected_country != "Todos":
    df_filtered = df[df["regiao"] == selected_country]
else:
    df_filtered = df.copy()


# ============================================================
# CÁLCULO DOS KPIs
# ============================================================

desemp = df_filtered[df_filtered["tipo"] == "desemprego_global"]["valor"].mean()
saude = df_filtered[df_filtered["tipo"] == "saude_global"]["valor"].mean()
invest = df_filtered[df_filtered["tipo"] == "investimento_global"]["valor"].mean()

colA, colB, colC = st.columns(3)

with colA:
    st.markdown(f"""
    <div class="card">
        <div class="card-icon">
            <img src="https://img.icons8.com/ios-filled/50/3563E9/combo-chart.png" width="26">
        </div>
        <div>
            <div class="card-title">Desemprego Médio</div>
            <div class="card-value">{desemp:.2f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown(f"""
    <div class="card">
        <div class="card-icon">
            <img src="https://img.icons8.com/ios-filled/50/3563E9/healthy-food.png" width="26">
        </div>
        <div>
            <div class="card-title">Gasto em Saúde</div>
            <div class="card-value">{saude:.2f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with colC:
    st.markdown(f"""
    <div class="card">
        <div class="card-icon">
            <img src="https://img.icons8.com/ios-filled/50/3563E9/money-bag.png" width="26">
        </div>
        <div>
            <div class="card-title">Investimentos</div>
            <div class="card-value">{invest:.2f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SEÇÃO DE GRÁFICOS
# ============================================================

st.markdown("<div class='section-title'>Visualização Global</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("##### Tendência Global de Desemprego")
    st.plotly_chart(charts.chart_desemprego_global(df_filtered), use_container_width=True)

with c2:
    st.markdown("##### Gasto Global em Saúde")
    st.plotly_chart(charts.chart_saude_global(df_filtered), use_container_width=True)

with c3:
    st.markdown("##### Tendência Global de Investimentos")
    st.plotly_chart(charts.chart_investimentos_global(df_filtered), use_container_width=True)


# ============================================================
# SEÇÃO DE RANKING
# ============================================================

st.markdown("<div class='section-title'>Ranking Global por Ano</div>", unsafe_allow_html=True)
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Segurança contra DF vazio
if df.empty or "ano" not in df.columns or df["ano"].dropna().empty:
    st.error("Nenhum dado disponível para montar o ranking. Verifique se as APIs retornaram dados.")
    st.stop()

ano_min_real = df["ano"].dropna().min()
ano_max_real = df["ano"].dropna().max()

ano_min = int(ano_min_real)
ano_max = int(ano_max_real)

selected_year = st.slider("Selecione um ano:", ano_min, ano_max, ano_max)

tab1, tab2, tab3 = st.tabs(["Desemprego", "Saúde", "Investimentos"])

with tab1:
    st.plotly_chart(charts.chart_ranking(df, "desemprego_global", selected_year), use_container_width=True)

with tab2:
    st.plotly_chart(charts.chart_ranking(df, "saude_global", selected_year), use_container_width=True)

with tab3:
    st.plotly_chart(charts.chart_ranking(df, "investimento_global", selected_year), use_container_width=True)
