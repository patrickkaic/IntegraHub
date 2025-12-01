import pandas as pd
import random

# -----------------------------
# Gera dados de desemprego (2014–2024)
# -----------------------------
def fetch_desemprego_extenso():
    regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    anos = list(range(2014, 2025))
    base_regiao = {
        "Norte": 8.5,
        "Nordeste": 10.2,
        "Centro-Oeste": 7.3,
        "Sudeste": 11.0,
        "Sul": 6.1
    }

    data = []
    for ano in anos:
        for reg in regioes:
            variacao = random.uniform(-0.8, 0.8)
            valor = max(4.0, base_regiao[reg] + (ano - 2014) * random.uniform(-0.3, 0.2) + variacao)
            data.append({"ano": ano, "regiao": reg, "valor": round(valor, 1), "tipo": "desemprego"})
    return pd.DataFrame(data)


# -----------------------------
# Gera dados de saúde (Hospitais por região)
# Crescimento moderado anual (2014–2024)
# -----------------------------
def fetch_saude_extenso():
    regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    anos = list(range(2014, 2025))

    base = {
        "Norte": 80,
        "Nordeste": 150,
        "Centro-Oeste": 60,
        "Sudeste": 260,
        "Sul": 140
    }

    data = []
    for ano in anos:
        for reg in regioes:
            crescimento = (ano - 2014) * random.uniform(1.2, 3.0)
            valor = base[reg] + crescimento
            data.append({"ano": ano, "regiao": reg, "valor": int(valor), "tipo": "saude"})
    return pd.DataFrame(data)


# -----------------------------
# Gera dados de investimentos (Bilhões)
# Relacionados com desemprego (quanto mais investimento → menor desemprego)
# -----------------------------
def fetch_investimentos_extenso():
    regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    anos = list(range(2014, 2025))

    base = {
        "Norte": 2.0,
        "Nordeste": 3.5,
        "Centro-Oeste": 1.7,
        "Sudeste": 8.0,
        "Sul": 4.0
    }

    data = []
    for ano in anos:
        for reg in regioes:
            crescimento = (ano - 2014) * random.uniform(0.1, 0.35)
            variacao = random.uniform(-0.2, 0.4)
            valor = base[reg] + crescimento + variacao
            data.append({"ano": ano, "regiao": reg, "valor": round(valor, 2), "tipo": "investimentos"})
    return pd.DataFrame(data)


# -----------------------------
# ETL Final — junta tudo
# -----------------------------
def run_etl():
    df1 = fetch_desemprego_extenso()
    df2 = fetch_saude_extenso()
    df3 = fetch_investimentos_extenso()

    df = pd.concat([df1, df2, df3], ignore_index=True)
    return df
