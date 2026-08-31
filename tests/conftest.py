"""Shared pytest fixtures."""

import os

import pytest
from alembic.runtime.migration import MigrationContext
from flask_migrate import upgrade
from sqlalchemy import text
from sqlalchemy.engine import make_url

from moffat_bay import create_app
from moffat_bay.config import Config
from moffat_bay.db import db


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-only-secret"
    WTF_CSRF_ENABLED = False


def test_database_url() -> str:
    """Return the dedicated test database URL or skip database tests."""
    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("TEST_DATABASE_URL is not configured")
    if make_url(database_url).database != "moffat_bay_test":
        pytest.fail("TEST_DATABASE_URL must target the disposable moffat_bay_test database")
    return database_url


class DatabaseTestConfig(TestConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


@pytest.fixture()
def app():
    return create_app(TestConfig)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def database_app():
    """Provide an application migrated against the dedicated MySQL test database."""
    test_database_url()
    application = create_app(DatabaseTestConfig)
    with application.app_context():
        upgrade()
        with db.engine.connect() as connection:
            assert MigrationContext.configure(connection).get_current_revision()
    return application


@pytest.fixture()
def database(database_app):
    """Isolate each database test by deleting data after its transaction completes."""
    with database_app.app_context():
        try:
            yield
        finally:
            db.session.rollback()
            db.session.execute(text("DELETE FROM reservation"))
            db.session.execute(text("DELETE FROM customer"))
            db.session.execute(text("DELETE FROM room_type"))
            db.session.commit()
            db.session.remove()
