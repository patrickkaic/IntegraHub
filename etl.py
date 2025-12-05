import pandas as pd
import requests
import streamlit as st
from datetime import datetime


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
# 1) WORLD BANK — ECONOMIA REAL
# PIB, desemprego e população
# ============================================================

def fetch_worldbank_indicator(country: str, indicator: str, tipo: str):
    """
    country = 'BRA'
    indicator = códigos World Bank (ex: SL.UEM.TOTL.ZS)
    tipo = nome do indicador no dataframe final
    """
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json"

    data = safe_get(url)
    if not data or len(data) < 2:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    rows = []
    for item in data[1]:  
        if item["value"] is None:
            continue
        rows.append({
            "ano": int(item["date"]),
            "regiao": country,
            "valor": float(item["value"]),
            "tipo": tipo
        })

    return pd.DataFrame(rows)


def fetch_economia_worldbank():
    df1 = fetch_worldbank_indicator("BRA", "NY.GDP.MKTP.CD", "pib")
    df2 = fetch_worldbank_indicator("BRA", "SL.UEM.TOTL.ZS", "desemprego")
    df3 = fetch_worldbank_indicator("BRA", "SP.POP.TOTL", "populacao")
    return pd.concat([df1, df2, df3], ignore_index=True)


# ============================================================
# 2) OPEN-METEO — CLIMA REAL
# Temperatura média diária em SP
# ============================================================

def fetch_clima_openmeteo():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=-23.55&longitude=-46.63"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&timezone=America%2FSao_Paulo"
    )

    data = safe_get(url)
    if not data:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    datas = data["daily"]["time"]
    temp_max = data["daily"]["temperature_2m_max"]

    rows = []
    for d, t in zip(datas, temp_max):
        ano = int(d.split("-")[0])
        rows.append({
            "ano": ano,
            "regiao": "SP",
            "valor": float(t),
            "tipo": "temperatura_max"
        })

    return pd.DataFrame(rows)


# ============================================================
# 3) FIPEAPI — Veículos
# Marcas de carros e quantidade
# ============================================================

def fetch_fipe_marcas():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    data = safe_get(url)

    if not data:
        return pd.DataFrame(columns=["ano", "regiao", "valor", "tipo"])

    ano_atual = datetime.now().year

    rows = []
    for item in data:
        rows.append({
            "ano": ano_atual,
            "regiao": "Brasil",
            "valor": 1,                # cada marca = 1 unidade
            "tipo": "marcas_veiculos"  # quantidade de marcas
        })

    df = pd.DataFrame(rows)
    df = df.groupby(["ano", "regiao", "tipo"])["valor"].sum().reset_index()

    return df


# ============================================================
# ETL FINAL COM CACHE
# ============================================================

@st.cache_data(ttl=3600)
def run_etl():
    st.info("🔄 Carregando dados econômicos, clima e FIPE...")

    df_econ = fetch_economia_worldbank()
    df_clima = fetch_clima_openmeteo()
    df_fipe  = fetch_fipe_marcas()

    df = pd.concat([df_econ, df_clima, df_fipe], ignore_index=True)
    df = df.sort_values("ano").reset_index(drop=True)

    st.success("✔ Dados carregados com sucesso!")
    return df
