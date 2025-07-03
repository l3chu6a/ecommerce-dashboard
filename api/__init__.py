from flask import Blueprint

api = Blueprint("api", __name__)

from . import routes  # importa las rutas de subida de archivos
