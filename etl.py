import pandas as pd
import requests
import streamlit as st

# ============================================================
#  FUNÇÃO AUXILIAR – REQUEST SEGURO
# ============================================================

def safe_get(url, params=None):
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.warning(f"[ERRO API] {url} → {e}")
        return None

# ============================================================
# 1) DESEMPREGO – IBGE
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
# 2) SAÚDE – DataSUS
# ============================================================

def fetch_saude_api():
    url = "https://apidadosabertos.saude.gov.br/v1/cnes/estabelecimentos"
    params = {"limit": 5000}

    data = safe_get(url, params)
    if not data:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    df = pd.DataFrame(data)

    # Campos variáveis nas APIs → normaliza
    df["uf"] = df.get("uf", "BR")
    df["anoReferencia"] = df.get("anoReferencia", 2024)

    df = df.rename(columns={"uf": "regiao", "anoReferencia": "ano"})
    df["valor"] = 1  # Cada linha = 1 hospital

    df = df.groupby(["regiao", "ano"])["valor"].sum().reset_index()
    df["tipo"] = "saude"

    return df

# ============================================================
# 3) INVESTIMENTOS – Banco Central
# ============================================================

def fetch_investimentos_api():
    url = "https://dadosabertos.bcb.gov.br/api/3/action/datastore_search"
    params = {
        "resource_id": "f0f8f047-3494-4f1d-bd0c-eb874ebf07c6",
        "limit": 5000
    }

    data = safe_get(url, params)
    if not data:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    records = data["result"]["records"]
    df = pd.DataFrame(records)

    if "Ano" not in df or "Investimentos" not in df:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    df = df.rename(columns={"Ano": "ano", "Investimentos": "valor"})
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")

    df["regiao"] = "Brasil"
    df["tipo"] = "investimentos"

    df = df.dropna(subset=["ano", "valor"])

    return df[["ano", "regiao", "valor", "tipo"]]

# ============================================================
#  ETL FINAL – COM CACHE DO STREAMLIT
# ============================================================

@st.cache_data(ttl=3600)  # Cache por 1h → evita chamadas desnecessárias
def run_etl():
    df1 = fetch_desemprego_api()
    df2 = fetch_saude_api()
    df3 = fetch_investimentos_api()

    df = pd.concat([df1, df2, df3], ignore_index=True)
    df["ano"] = df["ano"].astype(int)
    df = df.sort_values("ano")

    return df