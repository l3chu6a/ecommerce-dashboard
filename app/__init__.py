from flask import Flask
from .routes import dashboard
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    app.register_blueprint(dashboard)
    return app
