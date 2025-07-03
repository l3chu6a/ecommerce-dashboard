# portal/__init__.py
from flask import Blueprint

portal = Blueprint("portal", __name__)

from . import data_api, views # asegúrate de que routes.py y api.py usen `from . import portal`
