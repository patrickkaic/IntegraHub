import streamlit as st
import pandas as pd

from database import init_db
from repository import insert_dataframe, get_all
from etl import run_etl
from charts import chart_desemprego

st.set_page_config(page_title="IntegraHub", layout="wide")
st.title("IntegraHub")

# Inicializa banco
init_db()

col1, col2 = st.columns([1, 2])

with col1:
    st.header("⚙️ Controle")
    if st.button("Rodar ETL (IBGE Mock)"):
        df = run_etl()
        insert_dataframe(df)
        st.success("ETL executado com sucesso!")

with col2:
    st.header("📌 Dados Coletados")
    data = get_all()
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("Nenhum dado carregado. Execute o ETL.")
    else:
        st.dataframe(df, use_container_width=True)

st.divider()

if not df.empty:
    st.header("📈 Visualização")
    chart = chart_desemprego(df)
    st.plotly_chart(chart, use_container_width=True)

