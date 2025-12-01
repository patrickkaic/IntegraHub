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
### Management Dashboard
""")

# ========== FILTERS ==========

col1, col2 = st.columns(2)
month = col1.selectbox("Month", ["April 2024", "March 2024", "February 2024"])
region = col2.selectbox("Region", ["All", "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"])

# ========== LOAD DATA ==========

df = run_etl()

if region != "All":
    df = df[df["regiao"] == region]

desemp = df[df["tipo"] == "desemprego"]["valor"].mean()

# ========== K P I   C A R D S ==========

colA, colB, colC = st.columns(3)

with colA:
    st.markdown(f"""
    <div class="card">
        <div class="card-icon">
            <img src="https://img.icons8.com/ios-filled/50/3563E9/combo-chart.png" width="26">
        </div>
        <div>
            <div class="card-title">Unemployment</div>
            <div class="card-value">{desemp:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown("""
    <div class="card">
        <div class="card-icon">
            <img src="https://img.icons8.com/ios-filled/50/3563E9/money-bag.png" width="26">
        </div>
        <div>
            <div class="card-title">GDP per Capita</div>
            <div class="card-value">R$ 38,200</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with colC:
    st.markdown("""
    <div class="card">
        <div class="card-icon">
            <img src="https://img.icons8.com/ios-filled/50/3563E9/classroom.png" width="26">
        </div>
        <div>
            <div class="card-title">Average Education</div>
            <div class="card-value">8.9 years</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== CHART GRID ==========

st.markdown("## ")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("#### Unemployment Trend")
    st.plotly_chart(charts.chart_desemprego(df), use_container_width=True)

with c2:
    st.markdown("#### Regional Unemployment")
    st.plotly_chart(charts.chart_saude(df), use_container_width=True)

with c3:
    st.markdown("#### Prediction")
    st.plotly_chart(charts.chart_investimentos(df), use_container_width=True)
