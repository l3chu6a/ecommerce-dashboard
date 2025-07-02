from app import create_app
from app.models import db, AmazonOrder
from datetime import date
import random

app = create_app()

dummy_data = [
    {
        "order_id": f"AMZ-{1000+i}",
        "order_date": date(2025, 7, i % 28 + 1),
        "customer": f"Customer {i}",
        "product_name": f"Product {i}",
        "sku": f"SKU{i}",
        "quantity": random.randint(1, 3),
        "item_price": round(random.uniform(10, 100), 2),
        "amazon_fee": round(random.uniform(1, 10), 2),
        "fba_fee": round(random.uniform(2, 8), 2),
        "refund": round(random.choice([0.0, 5.0]), 2),
    }
    for i in range(20)
]

with app.app_context():
    for row in dummy_data:
        net = (row["item_price"] * row["quantity"]) - row["amazon_fee"] - row["fba_fee"] - row["refund"]
        order = AmazonOrder(
            order_id=row["order_id"],
            order_date=row["order_date"],
            customer=row["customer"],
            product_name=row["product_name"],
            sku=row["sku"],
            quantity=row["quantity"],
            item_price=row["item_price"],
            amazon_fee=row["amazon_fee"],
            fba_fee=row["fba_fee"],
            refund=row["refund"],
            net_profit=round(net, 2)
        )
        db.session.add(order)
    db.session.commit()
    print("✅ Datos dummy insertados")
