from sqlalchemy import text
from database import engine

def insert_dataframe(df):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM indicadores_desemprego"))
        df.to_sql("indicadores_desemprego", conn, if_exists="append", index=False)

def get_all():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM indicadores_desemprego ORDER BY ano")).fetchall()
    return [dict(r._mapping) for r in rows]
