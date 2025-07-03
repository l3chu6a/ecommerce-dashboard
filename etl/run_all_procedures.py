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
    print(f"\n🚀 Ejecutando stored procedures para cliente: {schema}")

    try:
        with engine.begin() as conn:
            conn.execute(text("CALL public.etl_raw_to_stg(:schema)"), {"schema": schema})
            print(f"✅ public.etl_raw_to_stg('{schema}') ejecutado")

            conn.execute(text("CALL public.etl_stg_to_prod(:schema)"), {"schema": schema})
            print(f"✅ public.etl_stg_to_prod('{schema}') ejecutado")
            
            conn.execute(text("CALL public.create_dashboard_view(:schema)"), {"schema": schema})
            print(f"✅ public.create_dashboard_view('{schema}') ejecutado")

    except Exception as e:
        print(f"❌ Error al ejecutar procedures para '{schema}': {e}")
