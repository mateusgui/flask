from flask import Flask, jsonify
from sqlalchemy import text

from app.config import Config
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.get("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            database_status = "ok"
        except Exception:
            database_status = "erro"

        return jsonify({"status": "ok", "database": database_status})

    return app
