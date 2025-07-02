from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class AmazonOrder(db.Model):
    __tablename__ = 'amazon_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    customer = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    amazon_fee = db.Column(db.Float, nullable=False)
    fba_fee = db.Column(db.Float, nullable=False)
    refund = db.Column(db.Float, nullable=False)
    net_profit = db.Column(db.Float, nullable=False)