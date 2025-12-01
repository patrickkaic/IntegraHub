import plotly.express as px
import pandas as pd

def chart_desemprego(df: pd.DataFrame):
    df = df[df["tipo"] == "desemprego"]

    fig = px.line(
        df,
        x="ano",
        y="valor",
        color="regiao",
        markers=True,
        title="Unemployment Trend"
    )
    fig.update_layout(template="plotly_white")
    return fig


def chart_saude(df: pd.DataFrame):
    df = df[df["tipo"] == "saude"]

    fig = px.bar(
        df,
        x="regiao",
        y="valor",
        color="regiao",
        title="Regional Unemployment"
    )
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig


def chart_investimentos(df: pd.DataFrame):
    df = df[df["tipo"] == "investimentos"]

    fig = px.line(
        df,
        x="regiao",
        y="valor",
        markers=True,
        title="Prediction"
    )
    fig.update_layout(template="plotly_white")
    return fig
