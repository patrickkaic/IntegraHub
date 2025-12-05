import pandas as pd
import requests
import streamlit as st


# ============================================================
# HELPER: REQUEST SEGURO
# ============================================================

def safe_get(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning(f"[ERRO API] {url} → {e}")
        return None


# ============================================================
# FUNÇÃO GERAL PARA BUSCAR QUALQUER INDICADOR GLOBAL
# ============================================================

def fetch_global_indicator(indicator: str, tipo: str):
    """
    Busca um indicador da API global do World Bank
    para TODOS os países, sem token.
    """
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?downloadformat=json&format=json&per_page=60000"

    data = safe_get(url)
    if not data or len(data) < 2:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    rows = []
    for item in data[1]:
        if item["value"] is None:
            continue

        # Filtra somente países (elimina "WLD", "ECS", etc.)
        if item["country"]["id"] in ["WLD", "OED", "HIC", "MIC", "LIC"]:
            continue

        rows.append({
            "ano": int(item["date"]),
            "regiao": item["country"]["value"],   # nome do país
            "valor": float(item["value"]),
            "tipo": tipo
        })

    return pd.DataFrame(rows)


# ============================================================
# ETL FINAL: desemprego, saúde e investimentos globais
# ============================================================

@st.cache_data(ttl=3660)
def run_etl():
    st.info("🌍 Coletando dados globais (World Bank)...")

    # DESMPREGO
    df_desemp = fetch_global_indicator(
        indicator="SL.UEM.TOTL.ZS",
        tipo="desemprego_global"
    )

    # SAÚDE
    df_saude = fetch_global_indicator(
        indicator="SH.XPD.CHEX.GD.ZS",
        tipo="saude_global"
    )

    # INVESTIMENTOS
    df_invest = fetch_global_indicator(
        indicator="NE.GDI.TOTL.ZS",
        tipo="investimento_global"
    )

    df = pd.concat([df_desemp, df_saude, df_invest], ignore_index=True)
    df = df.sort_values("ano")

    st.success("✔ Dados globais carregados com sucesso!")

    return df
