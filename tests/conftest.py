"""Shared pytest fixtures."""

import pytest

from moffat_bay import create_app
from moffat_bay.config import Config


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-only-secret"


@pytest.fixture()
def app():
    return create_app(TestConfig)


@pytest.fixture()
def client(app):
    return app.test_client()
