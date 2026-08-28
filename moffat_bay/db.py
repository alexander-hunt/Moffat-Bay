"""Shared SQLAlchemy and Flask-Migrate instances."""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def init_app(app):
    """Bind the shared db and migrate instances to an application."""
    db.init_app(app)
    migrate.init_app(app, db)
