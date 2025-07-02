from flask import Blueprint, render_template
from .models import db

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
def index():
    return render_template("dashboard.html", data=[])
    