"""Integration tests for database seeds and CLI commands."""

from decimal import Decimal

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
    assert [
        (
            room_type.room_name,
            room_type.description,
            room_type.max_guests,
            room_type.current_nightly_rate,
            room_type.active,
        )
        for room_type in db.session.scalars(select(RoomType).order_by(RoomType.room_type_id))
    ] == [
        (
            "Pinewood Studio",
            "Cozy room for 1 or 2. Some views of Joviedsa forest area.",
            2,
            Decimal("145.00"),
            True,
        ),
        (
            "Alder Suite",
            "Large bedroom with open entertainment room. Amazing views of the Puget Sound.",
            5,
            Decimal("195.00"),
            True,
        ),
        (
            "Maple Cabin",
            "3 bedrooms and a spacious family room. Direct access to Joviedsa hiking "
            "trails and canoeing access to the Puget Sound.",
            6,
            Decimal("245.00"),
            True,
        ),
        (
            "Douglas Fir Outpost",
            "Ultimate Family Retreat. Large private cabin with 5 bedrooms, family room, "
            "game room, seating areas indoors/outdoors.",
            10,
            Decimal("495.00"),
            True,
        ),
    ]
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
