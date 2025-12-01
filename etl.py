import pandas as pd

def run_etl():
    # Simulação de dados IBGE (seguro, rápido, sem API)
    data = [
        {"ano": 2020, "regiao": "Norte", "taxa": 6.5},
        {"ano": 2021, "regiao": "Norte", "taxa": 7.0},
        {"ano": 2022, "regiao": "Norte", "taxa": 7.8},
        {"ano": 2023, "regiao": "Norte", "taxa": 7.3},
        {"ano": 2020, "regiao": "Sudeste", "taxa": 8.1},
        {"ano": 2021, "regiao": "Sudeste", "taxa": 8.4},
        {"ano": 2022, "regiao": "Sudeste", "taxa": 9.2},
        {"ano": 2023, "regiao": "Sudeste", "taxa": 8.6},
    ]

    df = pd.DataFrame(data)
    return df
