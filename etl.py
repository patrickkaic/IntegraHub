import pandas as pd

def fetch_desemprego_generico():
    data = [
        {"ano": 2020, "regiao": "Norte", "valor": 8.1},
        {"ano": 2021, "regiao": "Norte", "valor": 7.4},
        {"ano": 2022, "regiao": "Norte", "valor": 6.9},
        {"ano": 2023, "regiao": "Norte", "valor": 6.7},

        {"ano": 2020, "regiao": "Sudeste", "valor": 11.2},
        {"ano": 2021, "regiao": "Sudeste", "valor": 10.1},
        {"ano": 2022, "regiao": "Sudeste", "valor": 9.3},
        {"ano": 2023, "regiao": "Sudeste", "valor": 8.8},
    ]

    df = pd.DataFrame(data)
    df["tipo"] = "desemprego"
    return df


def fetch_saude_generico():
    data = [
        {"ano": 2023, "regiao": "Norte", "valor": 120},
        {"ano": 2023, "regiao": "Nordeste", "valor": 240},
        {"ano": 2023, "regiao": "Centro-Oeste", "valor": 90},
        {"ano": 2023, "regiao": "Sudeste", "valor": 310},
        {"ano": 2023, "regiao": "Sul", "valor": 150},
    ]

    df = pd.DataFrame(data)
    df["tipo"] = "saude"
    return df


def fetch_investimentos_generico():
    data = [
        {"ano": 2023, "regiao": "Norte", "valor": 3.2},
        {"ano": 2023, "regiao": "Nordeste", "valor": 4.5},
        {"ano": 2023, "regiao": "Centro-Oeste", "valor": 2.1},
        {"ano": 2023, "regiao": "Sudeste", "valor": 8.4},
        {"ano": 2023, "regiao": "Sul", "valor": 3.9},
    ]

    df = pd.DataFrame(data)
    df["tipo"] = "investimentos"
    return df


def run_etl():
    df1 = fetch_desemprego_generico()
    df2 = fetch_saude_generico()
    df3 = fetch_investimentos_generico()
    df_final = pd.concat([df1, df2, df3], ignore_index=True)
    return df_final
