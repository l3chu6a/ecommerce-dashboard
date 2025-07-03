from flask import request, jsonify
from sqlalchemy import create_engine, text
from . import portal
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@portal.route("/api/data/<client_id>")
def get_dashboard_data(client_id):
    filter_type = request.args.get("filter")
    start_date = request.args.get("date")
    end_date = request.args.get("date")
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
        params["date"] = start_date
        params["date"] = end_date
    if sku:
        base_query += " AND sku = :sku"
        params["sku"] = sku
    if amount_description:
        base_query += " AND amount_description = :amount_description"
        params["amount_description"] = amount_description

    base_query += " GROUP BY date, sku, amount_description ORDER BY date"

    with engine.begin() as conn:
        result = conn.execute(text(base_query), params)
        rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]


    return jsonify(rows)
