from flask import Flask
from .routes import AuthRoutes, AlertaRoutes, SensoresRoutes, ColmenaRoutes, ReportesRoutes

def create_app():
    app = Flask(__name__, static_folder="../static", static_url_path="/static")
    app.config.from_object("src.config.Config")

    app.register_blueprint(AuthRoutes.main, url_prefix="/auth")
    app.register_blueprint(AlertaRoutes.main, url_prefix="/alertas")
    app.register_blueprint(SensoresRoutes.main, url_prefix="/sensores")
    app.register_blueprint(ColmenaRoutes.main, url_prefix="/colmenas")
    # app.register_blueprint(ReportesRoutes.main, url_prefix="/reportes")

    return app
