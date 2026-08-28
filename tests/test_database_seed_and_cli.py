"""Integration tests for database seeds and CLI commands."""

import pytest
from sqlalchemy import func, select
from werkzeug.security import check_password_hash

from moffat_bay.db import db
from moffat_bay.models import Customer, Reservation, RoomType
from moffat_bay.seeds import seed_development_data

pytestmark = pytest.mark.database


def row_count(model):
    return db.session.scalar(select(func.count()).select_from(model))


def test_development_seed_is_idempotent(database):
    seed_development_data()
    seed_development_data()

    assert row_count(Customer) == 3
    assert row_count(RoomType) == 4
    assert row_count(Reservation) == 3
    assert check_password_hash(db.session.get(Customer, 1).password_hash, "moffat-dev-maya-01")
    assert db.session.get(Reservation, 1).total_cost == 540


def test_database_cli_commands(database, database_app):
    runner = database_app.test_cli_runner()

    assert runner.invoke(args=["db-ping"]).exit_code == 0
    assert runner.invoke(args=["seed-db"]).output == "Seeded development data.\n"
    result = runner.invoke(args=["init-db"])

    assert result.exit_code == 0
    assert result.output == "Database initialized and seeded.\n"
    assert row_count(Customer) == 3
