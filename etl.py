import pandas as pd
import requests

# ================================
# API 1 — DESEMPREGO (IBGE)
# ================================
def fetch_desemprego_ibge():
    url = "https://servicodados.ibge.gov.br/api/v3/agregados/4099/periodos/201901-202401/variaveis/4099"
    r = requests.get(url)

    if r.status_code != 200:
        raise Exception("Erro ao consultar API de desemprego do IBGE")

    data = r.json()[0]["resultados"][0]["series"]

    rows = []
    for serie in data:
        regiao = serie["localidade"]["nome"]
        for periodo, valor in serie["serie"].items():
            ano = int(periodo[:4])
            taxa = float(valor.replace(",", ".")) if valor else None
            rows.append({
                "tipo": "desemprego",
                "ano": ano,
                "regiao": regiao,
                "valor": taxa
            })

    return pd.DataFrame(rows)


# ================================
# API 2 — SAÚDE (OpenDataSUS / CNES)
# ================================
def fetch_saude_estabelecimentos():
    url = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos?limit=5000"
    r = requests.get(url)

    if r.status_code != 200:
        raise Exception("Erro ao consultar API de saúde (CNES)")

    data = r.json()["estabelecimentos"]

    rows = []
    for item in data:
        regiao = item.get("uf")
        tipo = item.get("tipoUnidade")

        rows.append({
            "tipo": "saude_estabelecimentos",
            "ano": 2024,
            "regiao": regiao,
            "valor": 1  # Cada registro = 1 unidade de saúde
        })

    df = pd.DataFrame(rows)
    return df.groupby(["tipo", "regiao", "ano"], as_index=False).sum()


# ================================
# API 3 — INVESTIMENTOS (SICONFI)
# ================================
def fetch_investimentos_siconfi():
    url = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/investimentosporexercicio?an_exercicio=2023"
    r = requests.get(url)

    if r.status_code != 200:
        raise Exception("Erro ao consultar API de investimentos (Siconfi)")

    data = r.json()["items"]

    rows = []
    for item in data:
        uf = item["sg_uf"]
        valor = float(item["vl_investimentos"]) if item["vl_investimentos"] else 0

        rows.append({
            "tipo": "investimentos",
            "ano": 2023,
            "regiao": uf,
            "valor": valor
        })

    return pd.DataFrame(rows)


# ================================
# FUNÇÃO FINAL — UNIFICAÇÃO DO ETL
# ================================
def run_etl():
    print("🔄 Executando ETL com 3 APIs reais...")

    df_desemprego = fetch_desemprego_ibge()
    df_saude = fetch_saude_estabelecimentos()
    df_invest = fetch_investimentos_siconfi()

    # Junta tudo em um dataframe só
    df_final = pd.concat(
        [df_desemprego, df_saude, df_invest],
        ignore_index=True
    )

    print("✔ ETL finalizado — Total de registros:", len(df_final))
    return df_final
