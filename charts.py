import plotly.express as px
import pandas as pd

def chart_desemprego(df: pd.DataFrame):
    fig = px.line(
        df,
        x="ano",
        y="taxa",
        color="regiao",
        markers=True,
        title="Evolução da Taxa de Desemprego por Região"
    )
    return fig
