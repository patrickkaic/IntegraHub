import pandas as pd
import requests

# ================================
# API 1 — DESEMPREGO (IBGE)
# ================================
def fetch_desemprego_mundial():
    url = "https://api.worldbank.org/v2/country/BRA/indicator/SL.UEM.TOTL.ZS?format=json"
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        raise Exception("Erro ao consultar API World Bank")

    data = r.json()[1]  # série temporal

    rows = []
    for item in data:
        ano = item["date"]
        valor = item["value"]
        if valor is None:
            continue
        rows.append({
            "tipo": "desemprego",
            "ano": int(ano),
            "regiao": "Brasil",
            "valor": float(valor)
        })

    return pd.DataFrame(rows)



# ================================
# API 2 — SAÚDE (OpenDataSUS / CNES)
# ================================
def fetch_saude_opendatasoft():
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=world-hospitals&q=brasil&rows=500"
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        raise Exception("Erro ao consultar API de hospitais (OpenDataSoft)")

    data = r.json()["records"]

    rows = []
    for item in data:
        fields = item["fields"]
        regiao = fields.get("country", "Brasil")
        rows.append({
            "tipo": "saude_estabelecimentos",
            "ano": 2024,
            "regiao": regiao,
            "valor": 1
        })

    df = pd.DataFrame(rows)
    return df.groupby(["tipo", "regiao", "ano"], as_index=False).sum()

# ================================
# API 3 — INVESTIMENTOS (SICONFI)
# ================================
def fetch_investimentos_oecd():
    url = "https://stats.oecd.org/sdmx-json/data/DP_LIVE/BRA.GOVEXP.TOT.A?contentType=json"
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        raise Exception("Erro ao consultar API da OECD")

    data = r.json()["dataSets"][0]["series"]["0:0:0:0"]["observations"]

    # Mapa das datas
    series_info = r.json()["structure"]["dimensions"]["observation"][0]["values"]

    rows = []
    for key, value in data.items():
        ano = int(series_info[int(key)]["id"])
        valor = float(value[0])
        rows.append({
            "tipo": "investimentos",
            "ano": ano,
            "regiao": "Brasil",
            "valor": valor
        })

    return pd.DataFrame(rows)


# ================================
# FUNÇÃO FINAL — UNIFICAÇÃO DO ETL
# ================================
def run_etl():
    df1 = fetch_desemprego_mundial()
    df2 = fetch_saude_opendatasoft()
    df3 = fetch_investimentos_oecd()

    df_final = pd.concat([df1, df2, df3], ignore_index=True)
    return df_final