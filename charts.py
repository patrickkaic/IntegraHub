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
        title="📉 Taxa de Desemprego por Região",
        labels={"valor": "%", "ano": "Ano", "regiao": "Região"}
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
        title="🏥 Estabelecimentos de Saúde por Região",
        labels={"valor": "Quantidade", "regiao": "Região"}
    )
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig


def chart_investimentos(df: pd.DataFrame):
    df = df[df["tipo"] == "investimentos"]

    fig = px.bar(
        df,
        y="regiao",
        x="valor",
        orientation="h",
        color="regiao",
        title="💰 Investimentos Públicos por Região (Bilhões)",
        labels={"valor": "Investimento (bi)", "regiao": "Região"}
    )
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig
