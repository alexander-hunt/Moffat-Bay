"""Moffat Bay Lodge Flask application."""

from flask import Flask, jsonify

from .config import Config
from .db import init_app as init_db


def create_app(config_object: type[Config] = Config) -> Flask:
    """Create and configure an application instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)
    init_db(app)

    from .public import public_bp

    app.register_blueprint(public_bp)

    @app.get("/health")
    def health():
        return jsonify(status="ok", service="moffat-bay")

    return app

