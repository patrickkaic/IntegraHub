import sqlalchemy as sa
from sqlalchemy import text

DB_URL = "sqlite:///integrahub.db"
engine = sa.create_engine(DB_URL)

def init_db():
    ddl = """
    CREATE TABLE IF NOT EXISTS indicadores_desemprego(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ano INTEGER,
        regiao TEXT,
        taxa REAL
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))
