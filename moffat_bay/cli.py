"""Flask CLI commands for local database setup."""

import click
from flask_migrate import upgrade
from sqlalchemy import text

from .db import db
from .seeds import seed_development_data


def register_cli(app):
    """Attach database automation commands to a Flask application."""

    @app.cli.command("seed-db")
    def seed_db():
        """Load fictional development data."""
        seed_development_data()
        click.echo("Seeded development data.")

    @app.cli.command("init-db")
    def init_db():
        """Apply pending migrations, then load fictional development data."""
        upgrade()
        seed_development_data()
        click.echo("Database initialized and seeded.")

    @app.cli.command("db-ping")
    def db_ping():
        """Check that the configured MySQL connection is reachable."""
        db.session.execute(text("SELECT 1"))
        click.echo("Database connection OK.")
