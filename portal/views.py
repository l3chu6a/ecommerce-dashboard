from flask import render_template
from . import portal  # este es el Blueprint

@portal.route("/dashboard/<client_id>")
def render_dashboard(client_id):
    return render_template("dashboard.html", client_id=client_id)
