import pandas as pd
import requests
import streamlit as st

# ============================================================
# SAFE REQUEST
# ============================================================

def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning(f"[ERRO API] {url} → {e}")
        return None


# ============================================================
# 1) DESEMPREGO – IBGE (FUNCIONA)
# ============================================================

def fetch_desemprego_api():
    url = "https://servicodados.ibge.gov.br/api/v1/paises/BR/indicadores/4716"
    data = safe_get(url)

    if not data:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    serie = data[0]["series"][0]["serie"]

    rows = []
    for ano, valor in serie.items():
        rows.append({
            "ano": int(ano),
            "regiao": "Brasil",
            "valor": float(valor.replace(",", ".")),
            "tipo": "desemprego"
        })

    return pd.DataFrame(rows)


# ============================================================
# 2) SAÚDE – Brasil.IO (FUNCIONA)
# Estabelecimentos por município/UF
# ============================================================

def fetch_saude_api():
    url = "https://brasil.io/api/dataset/cnes/estabelecimentos/data/"
    data = safe_get(url)

    if not data or "results" not in data:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    df = pd.DataFrame(data["results"])

    # Campos podem variar → normalização
    if "estado_sigla" not in df:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    df["regiao"] = df["estado_sigla"]
    df["ano"] = 2024
    df["valor"] = 1

    df = df.groupby(["regiao", "ano"])["valor"].sum().reset_index()
    df["tipo"] = "saude"

    return df


# ============================================================
# 3) INVESTIMENTOS – Tesouro Nacional (FUNCIONA)
# Execução orçamentária por ano
# ============================================================

def fetch_investimentos_api():
    url = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/resultados"
    params = {"size": 2000}

    data = safe_get(url, params)
    if not data or "items" not in data:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    df = pd.DataFrame(data["items"])

    # Normaliza os campos relevantes
    if "ano" not in df or "valor" not in df:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    df = df[["ano", "valor"]]
    df["regiao"] = "Brasil"
    df["tipo"] = "investimentos"

    return df


# ============================================================
# ETL FINAL – COM CACHE
# ============================================================

@st.cache_data(ttl=3600)
def run_etl():
    st.info("Carregando dados das APIs públicas...")

    df1 = fetch_desemprego_api()
    df2 = fetch_saude_api()
    df3 = fetch_investimentos_api()

    df = pd.concat([df1, df2, df3], ignore_index=True)
    df["ano"] = df["ano"].astype(int)
    df = df.sort_values("ano")

    st.success("Dados carregados com sucesso!")
    return df
