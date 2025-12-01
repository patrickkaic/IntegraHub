import streamlit as st
from etl import run_etl
import charts

st.title("IntegraHub - Dashboard (Protótipo)")
st.write("Visualização de dados genéricos para demonstração.")

# Carrega dados
df = run_etl()
st.success("Dados carregados (modo protótipo com dados genéricos).")

st.subheader("Visualização por Indicador")

tipo = st.selectbox(
    "Selecione o indicador:",
    ["desemprego", "saude", "investimentos"]
)

if tipo == "desemprego":
    st.plotly_chart(charts.chart_desemprego(df), use_container_width=True)

elif tipo == "saude":
    st.plotly_chart(charts.chart_saude(df), use_container_width=True)

elif tipo == "investimentos":
    st.plotly_chart(charts.chart_investimentos(df), use_container_width=True)
