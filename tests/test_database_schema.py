"""Integration tests for the migrated MySQL schema."""

from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from moffat_bay.db import db
from moffat_bay.models import Customer, Reservation, RoomType

pytestmark = pytest.mark.database


def make_customer(**changes):
    values = {
        "first_name": "Maya",
        "last_name": "Chen",
        "email": "maya.chen@example.com",
        "telephone": "360-555-0101",
        "password_hash": "hashed-password",
    }
    values.update(changes)
    return Customer(**values)


def make_room_type(**changes):
    values = {
        "room_name": "Queen",
        "room_size": "One queen bed",
        "max_guests": 2,
        "current_nightly_rate": Decimal("135.00"),
        "active": True,
    }
    values.update(changes)
    return RoomType(**values)


def make_reservation(customer, room_type, **changes):
    values = {
        "customer": customer,
        "room_type": room_type,
        "guest_count": 2,
        "check_in_date": date(2026, 9, 14),
        "check_out_date": date(2026, 9, 18),
        "number_of_nights": 4,
        "nightly_rate": Decimal("135.00"),
        "total_cost": Decimal("540.00"),
    }
    values.update(changes)
    return Reservation(**values)


def test_migration_persists_valid_reservation_graph(database):
    customer = make_customer()
    room_type = make_room_type()
    reservation = make_reservation(customer, room_type)
    db.session.add(reservation)
    db.session.commit()

    persisted = db.session.get(Reservation, reservation.reservation_id)
    assert persisted.customer.email == "maya.chen@example.com"
    assert persisted.room_type.room_name == "Queen"
    assert persisted.total_cost == Decimal("540.00")


def test_migration_rejects_duplicate_customer_email(database):
    db.session.add(make_customer())
    db.session.commit()
    db.session.add(make_customer(first_name="Daniel"))

    with pytest.raises(IntegrityError):
        db.session.commit()


@pytest.mark.parametrize(
    ("factory", "changes"),
    [
        (make_customer, {"first_name": "   "}),
        (make_room_type, {"max_guests": 0}),
    ],
)
def test_migration_rejects_invalid_required_values(database, factory, changes):
    db.session.add(factory(**changes))

    with pytest.raises(IntegrityError):
        db.session.commit()


@pytest.mark.parametrize(
    "changes",
    [
        {"guest_count": 0},
        {"check_out_date": date(2026, 9, 14)},
        {"number_of_nights": 3},
        {"total_cost": Decimal("539.99")},
    ],
)
def test_migration_rejects_invalid_reservation_values(database, changes):
    customer = make_customer()
    room_type = make_room_type()
    db.session.add(make_reservation(customer, room_type, **changes))

    with pytest.raises(IntegrityError):
        db.session.commit()


def test_migration_rejects_missing_reservation_parents(database):
    db.session.add(
        Reservation(
            customer_id=999,
            room_type_id=999,
            guest_count=2,
            check_in_date=date(2026, 9, 14),
            check_out_date=date(2026, 9, 18),
            number_of_nights=4,
            nightly_rate=Decimal("135.00"),
            total_cost=Decimal("540.00"),
        )
    )

    with pytest.raises(IntegrityError):
        db.session.commit()


def test_migration_creates_reservation_stay_date_index(database):
    indexes = inspect(db.engine).get_indexes("reservation")

    assert {index["name"] for index in indexes} >= {"ix_reservation_stay_dates"}
