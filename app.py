# from flask import Flask
# from api.routes import api

# app = Flask(__name__)
# app.register_blueprint(api)

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask
# from api.routes import api as api_blueprint
# from portal.routes import portal as portal_blueprint

# app = Flask(__name__)
# app.register_blueprint(api_blueprint, url_prefix="/")
# app.register_blueprint(portal_blueprint, url_prefix="/")

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask
from api import api as api_blueprint                    # ✔️ tu módulo de carga de archivos
from portal import portal as portal_blueprint           # ✔️ dashboard web

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix="/")   # carga archivos (ej: POST /upload)
app.register_blueprint(portal_blueprint, url_prefix="/") # dashboard (ej: GET /dashboard/prune)

if __name__ == "__main__":
    app.run(debug=True)


