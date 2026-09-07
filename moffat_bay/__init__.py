"""Moffat Bay Lodge Flask application."""

from flask import Flask, jsonify

from .cli import register_cli
from .config import Config
from .db import init_app as init_db


def create_app(config_object: type[Config] = Config) -> Flask:
    """Create and configure an application instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    init_db(app)
    register_cli(app)

    from . import models  # noqa: F401 register models with SQLAlchemy metadata
    from .auth import auth_bp
    from .public import public_bp
    from .reservations import reservations_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(reservations_bp)

    @app.get("/health")
    def health():
        return jsonify(status="ok", service="moffat-bay")

    return app
