import pandas as pd
import requests
import streamlit as st


# ============================================================
# HELPER: REQUEST SEGURO
# ============================================================

def safe_get(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning(f"[ERRO API] {url} → {e}")
        return None


# ============================================================
# BUSCA GLOBAL COM PAGINAÇÃO (WORLD BANK)
# ============================================================

def fetch_global_indicator(indicator: str, tipo: str):
    rows = []
    page = 1

    while True:
        url = (
            f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
            f"?format=json&page={page}&per_page=1000"
        )

        data = safe_get(url)
        if not data or len(data) < 2:
            break

        meta = data[0]
        values = data[1]

        for item in values:
            if item["value"] is None:
                continue

            country = item["country"]["id"]
            name = item["country"]["value"]

            # remover regiões agregadas
            if country in ["WLD", "OED", "HIC", "MIC", "LIC", "ECS", "EAS", "LCN"]:
                continue

            # converter ano com segurança
            try:
                ano = int(str(item["date"]).strip()[:4])
            except:
                continue

            rows.append({
                "ano": ano,
                "regiao": name,
                "valor": float(item["value"]),
                "tipo": tipo
            })

        # parar quando não há mais páginas
        if page >= meta.get("pages", 1):
            break

        page += 1

    return pd.DataFrame(rows)


# ============================================================
# ETL FINAL: desemprego, saúde e investimentos globais
# ============================================================

@st.cache_data(ttl=3660)
def run_etl():
    st.info("🌍 Coletando dados globais (World Bank)...")

    df_desemp = fetch_global_indicator(
        indicator="SL.UEM.TOTL.ZS",
        tipo="desemprego_global"
    )

    df_saude = fetch_global_indicator(
        indicator="SH.XPD.CHEX.GD.ZS",
        tipo="saude_global"
    )

    df_invest = fetch_global_indicator(
        indicator="NE.GDI.TOTL.ZS",
        tipo="investimento_global"
    )

    df = pd.concat([df_desemp, df_saude, df_invest], ignore_index=True)
    df = df.sort_values("ano")

    st.success("✔ Dados globais carregados com sucesso!")

    return df
