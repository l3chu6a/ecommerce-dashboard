import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar credenciales
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Base de carpetas
BASE_PATH = "data"

# Recorremos cada cliente
for client_id in os.listdir(BASE_PATH):
    client_folder = os.path.join(BASE_PATH, client_id)

    if not os.path.isdir(client_folder):
        continue

    schema = client_id.lower()
    print(f"\n🚀 Ejecutando procedures para cliente: {schema}")

    try:
        with engine.begin() as conn:
            conn.execute(text(f"CALL {schema}.etl_raw_to_stg();"))
            print(f"✅ {schema}.etl_raw_to_stg() ejecutado")

            conn.execute(text(f"CALL {schema}.etl_stg_to_prod();"))
            print(f"✅ {schema}.etl_stg_to_prod() ejecutado")

    except Exception as e:
        print(f"❌ Error para {schema}: {e}")
