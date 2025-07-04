from flask import request, jsonify
from sqlalchemy import create_engine, text
from . import portal
import os
from dotenv import load_dotenv
from pathlib import Path
import os

# Cargar .env desde el directorio raíz del proyecto
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Verificación (esto debería mostrar tu URL de DB)
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@portal.route("/api/data/<client_id>")
def get_dashboard_data(client_id):
    filter_type = request.args.get("filter")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    sku = request.args.get("sku")
    amount_description = request.args.get("amount_description")

    base_query = f"""
        SELECT date, sku, amount_description, SUM(amount) as total
        FROM {client_id}.vw_dashboard_settlement
        WHERE 1=1
    """

    params = {}
    if start_date and end_date:
        base_query += " AND date BETWEEN :date AND :date"
        params["start_date"] = start_date
        params["end_date"] = end_date
    if sku:
        base_query += " AND sku = :sku"
        params["sku"] = sku.strip()
    if amount_description:
        base_query += " AND amount_description = :amount_description"
        params["amount_description"] = amount_description.strip()

    base_query += " GROUP BY date, sku, amount_description ORDER BY date"

    print("==== DASHBOARD QUERY ====")
    print("Client:", client_id)
    print("Query:")
    print(base_query)
    print("Params:", params)
    print("=========================")

    with engine.begin() as conn:
        result = conn.execute(text(base_query), params)

    print("Resultado crudo:", rows)
    return jsonify(rows)
