"""Shared SQLAlchemy and Flask-Migrate instances."""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pymysql import err as pymysql_err

# MySQL reports CHECK violations as error 3819, which PyMySQL does not map
# to its integrity-error family by default.
pymysql_err.error_map[3819] = pymysql_err.IntegrityError

db = SQLAlchemy()
migrate = Migrate()


def init_app(app):
    """Bind the shared db and migrate instances to an application."""
    db.init_app(app)
    migrate.init_app(app, db)
