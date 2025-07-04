import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar credenciales desde .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Ruta base donde están las carpetas por cliente
# BASE_PATH = "data"
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

# Recorremos cada subcarpeta en "data/"
for client_id in os.listdir(BASE_PATH):
    client_folder = os.path.join(BASE_PATH, client_id)

    if not os.path.isdir(client_folder):
        continue

    # Buscar archivo que empiece con "upload_" y termine en ".csv"
    csv_files = [f for f in os.listdir(client_folder) if f.startswith("upload_") and f.endswith(".csv")]
    
    if not csv_files:
        print(f"⚠️ No se encontró archivo válido para cliente '{client_id}'")
        continue

    csv_path = os.path.join(client_folder, csv_files[0])
    schema_name = client_id.lower()

    print(f"\n🔄 Procesando cliente: {schema_name}")

    try:
        with engine.begin() as conn:
            # Crear esquema si no existe
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))

            # Crear tabla raw si no existe
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.raw_amazon_settlement (
                    settlement_id           TEXT,
                    date                    TEXT,
                    order_id                TEXT,
                    sku                     TEXT,
                    marketplace             TEXT,
                    transaction_type        TEXT,  
                    amount_type             TEXT,
                    amount_description      TEXT,
                    amount                  NUMERIC,
                    currency                TEXT,
                    inserted_at TIMESTAMP DEFAULT NOW()
                );
            """))

        # Leer CSV e insertar
        df = pd.read_csv(csv_path)
        df.to_sql("raw_amazon_settlement", engine, schema=schema_name, if_exists="append", index=False)

        print(f"✅ Datos cargados correctamente para cliente '{schema_name}'")

    except Exception as e:
        print(f"❌ Error al procesar cliente '{schema_name}': {e}")
