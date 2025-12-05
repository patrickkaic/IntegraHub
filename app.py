import streamlit as st
from etl import run_etl
import charts

st.set_page_config(
    page_title="IntegraHub Dashboard",
    layout="wide",
)

# ========== STYLES (CSS premium) ==========

st.markdown("""
<style>

.card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.08);
    border: 1px solid #EDEDED;
    display: flex;
    align-items: center;
    gap: 15px;
}

.card-icon {
    background-color: #F3F6FF;
    padding: 12px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.card-title {
    font-size: 14px;
    font-weight: 600;
    color: #555;
    margin-bottom: 2px;
}

.card-value {
    font-size: 26px;
    font-weight: 700;
    color: #111;
}

</style>
""", unsafe_allow_html=True)


# ========== HEADER ==========

st.markdown("""
# IntegraHub  
### Dashboard Global de Indicadores
""")


# ========== LOAD DATA ==========

df = run_etl()

# Lista dinâmica de países
paises = sorted(df["regiao"].unique())
paises = ["Todos"] + paises

col1 = st.columns(1)[0]
selected_country = col1.selectbox("Selecione um país:", paises)

if selected_country != "Todos":
    df_filtered = df[df["regiao"] == selected_country]
else:
    df_filtered = df.copy()

# ========== KPIs (globais ou do país escolhido) ==========

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
            <div class="card-title">Gasto Médio em Saúde</div>
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
            <div class="card-title">Investimento Médio</div>
            <div class="card-value">{invest:.2f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ========== GRÁFICOS ==========

st.markdown("## ")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### Tendência Global de Desemprego")
    st.plotly_chart(charts.chart_desemprego_global(df_filtered), use_container_width=True)

with c2:
    st.markdown("#### Gasto Global em Saúde")
    st.plotly_chart(charts.chart_saude_global(df_filtered), use_container_width=True)

with c3:
    st.markdown("#### Tendência Global de Investimentos")
    st.plotly_chart(charts.chart_investimentos_global(df_filtered), use_container_width=True)


# ========== RANKING ==========

st.markdown("## 🌍 Ranking Global por Ano")

ano_min = int(df["ano"].min())
ano_max = int(df["ano"].max())

selected_year = st.slider("Selecione um ano:", ano_min, ano_max, ano_max)

tab1, tab2, tab3 = st.tabs(["Desemprego", "Saúde", "Investimentos"])

with tab1:
    st.plotly_chart(charts.chart_ranking(df, "desemprego_global", selected_year), use_container_width=True)

with tab2:
    st.plotly_chart(charts.chart_ranking(df, "saude_global", selected_year), use_container_width=True)

with tab3:
    st.plotly_chart(charts.chart_ranking(df, "investimento_global", selected_year), use_container_width=True)