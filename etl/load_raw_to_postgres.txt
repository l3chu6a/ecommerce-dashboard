import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Conexión a PostgreSQL
engine = create_engine(DATABASE_URL)

# Crear tabla si no existe (con timestamp)
create_table_sql = """
CREATE TABLE IF NOT EXISTS raw_amazon_settlement (
    settlement_id TEXT,
    order_id TEXT,
    sku TEXT,
    amount_type TEXT,
    amount_description TEXT,
    amount NUMERIC,
    date DATE,
    inserted_at TIMESTAMP DEFAULT NOW()
);
"""

with engine.begin() as conn:
    conn.execute(text(create_table_sql))
    print("✅ Tabla raw_amazon_settlement verificada/creada")

# Leer CSV guardado por la API
csv_path = "data/uploaded_settlement.csv"
df = pd.read_csv(csv_path)

# Insertar datos (timestamp se autocompleta)
df.to_sql("raw_amazon_settlement", engine, if_exists="append", index=False)
print("✅ Datos insertados correctamente en raw_amazon_settlement")
