from flask import Flask

from app.config import Config
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    from app import models

    from app.routes.usuarios import bp as usuarios_bp
    from app.routes.bairros import bp as bairros_bp
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(bairros_bp)

    return app
