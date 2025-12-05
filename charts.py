import plotly.express as px
import pandas as pd


# ============================================================
# 1) Desemprego Global – Linha temporal
# ============================================================

def chart_desemprego_global(df: pd.DataFrame):
    data = df[df["tipo"] == "desemprego_global"]

    fig = px.line(
        data,
        x="ano",
        y="valor",
        color="regiao",
        title="Taxa de Desemprego Global (%)",
        markers=True
    )

    fig.update_layout(
        template="plotly_white",
        legend_title="País",
        yaxis_title="Percentual (%)"
    )

    return fig


# ============================================================
# 2) Saúde Global – Gasto em Saúde (% do PIB)
# ============================================================

def chart_saude_global(df: pd.DataFrame):
    data = df[df["tipo"] == "saude_global"]

    # Exibir apenas 20 países para não poluir o gráfico
    top_paises = (
        data.groupby("regiao")["valor"]
        .mean()
        .sort_values(ascending=False)
        .head(20)
        .index
    )

    data = data[data["regiao"].isin(top_paises)]

    fig = px.bar(
        data,
        x="regiao",
        y="valor",
        title="Gasto em Saúde (% do PIB) – Top 20 Países",
        color="regiao"
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        xaxis_title="País",
        yaxis_title="% do PIB"
    )

    return fig


# ============================================================
# 3) Investimentos Globais – Linha temporal
# ============================================================

def chart_investimentos_global(df: pd.DataFrame):
    data = df[df["tipo"] == "investimento_global"]

    fig = px.line(
        data,
        x="ano",
        y="valor",
        color="regiao",
        title="Formação Bruta de Capital (% do PIB) – Investimentos Globais",
        markers=True
    )

    fig.update_layout(
        template="plotly_white",
        legend_title="País",
        yaxis_title="% do PIB"
    )

    return fig


# ============================================================
# 4) Ranking – Comparativo rápido de ano específico
# ============================================================

def chart_ranking(df: pd.DataFrame, tipo: str, ano: int):
    """
    Gera ranking de qualquer indicador global em um ano específico.
    Exemplo:
    chart_ranking(df, "desemprego_global", 2020)
    """

    data = df[(df["tipo"] == tipo) & (df["ano"] == ano)]
    data = data.sort_values("valor", ascending=False).head(20)

    fig = px.bar(
        data,
        x="regiao",
        y="valor",
        color="regiao",
        title=f"Ranking {tipo.replace('_', ' ').title()} – {ano}"
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        xaxis_title="País",
        yaxis_title="Valor"
    )

    return fig

import plotly.express as px

def chart_compare(df, tipo):
    df_tipo = df[df["tipo"] == tipo]

    if df_tipo.empty:
        return px.line(title="Sem dados suficientes")

    fig = px.line(
        df_tipo,
        x="ano",
        y="valor",
        color="regiao",
        markers=True,
        line_shape="spline",
        title=""
    )

    fig.update_layout(
        height=350,
        legend_title_text="País",
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig
