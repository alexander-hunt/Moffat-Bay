"""MySQL connection helpers shared by application features."""

import mysql.connector
from flask import current_app, g


def get_connection():
    """Return one MySQL connection for the current request context."""
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["MYSQL_HOST"],
            port=current_app.config["MYSQL_PORT"],
            database=current_app.config["MYSQL_DATABASE"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
        )
    return g.db


def close_connection(_error=None):
    """Close the current request's connection, if one exists."""
    connection = g.pop("db", None)
    if connection is not None and connection.is_connected():
        connection.close()


def init_app(app):
    """Register database cleanup with a Flask application."""
    app.teardown_appcontext(close_connection)

