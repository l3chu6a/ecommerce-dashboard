from app import create_app
from app.models import db
from dotenv import load_dotenv
import os

# 👇 Esto carga las variables de .env
load_dotenv()

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tablas creadas correctamente")
