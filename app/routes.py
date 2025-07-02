from flask import Blueprint, render_template
from .models import db, AmazonOrder

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
def index():
    data = AmazonOrder.query.order_by(AmazonOrder.order_date.desc()).limit(10).all()
    return render_template("dashboard.html", data=data)
