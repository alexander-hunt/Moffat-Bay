"""Reservation workflow tests."""

from datetime import date

import pytest

from moffat_bay.db import db
from moffat_bay.models import Customer, Reservation, RoomType

pytestmark = pytest.mark.database


def log_in(client, customer):
    """Authenticate a fixture customer in the test session."""
    with client.session_transaction() as session:
        session["customer_id"] = customer.customer_id


def make_customer(email="maya@example.com"):
    """Build a valid test customer."""
    return Customer(
        first_name="Maya",
        last_name="Chen",
        email=email,
        telephone="360-555-0101",
        password_hash="hash",
    )


def make_room(room_name="Queen", max_guests=2, nightly_rate="135.00"):
    """Build an active room type for a test stay."""
    return RoomType(
        room_name=room_name,
        description="A restful room.",
        max_guests=max_guests,
        current_nightly_rate=nightly_rate,
        active=True,
    )


def test_booking_requires_login(client):
    """Guests must authenticate before starting a reservation."""
    response = client.get("/reservations/book")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/account")


def test_booking_renders_active_room_choices(database, database_app):
    room_type = RoomType(
        room_name="King",
        description="A spacious room.",
        max_guests=2,
        current_nightly_rate="160.00",
        active=True,
    )
    customer = Customer(
        first_name="Maya",
        last_name="Chen",
        email="maya@example.com",
        telephone="360-555-0101",
        password_hash="hash",
    )
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    response = client.get("/reservations/book")

    assert response.status_code == 200
    assert b"King - $160.00 per night" in response.data


def test_booking_stores_server_calculated_pending_reservation(database, database_app):
    room_type = RoomType(
        room_name="Queen",
        description="A restful room.",
        max_guests=2,
        current_nightly_rate="135.00",
        active=True,
    )
    customer = Customer(
        first_name="Maya",
        last_name="Chen",
        email="maya@example.com",
        telephone="360-555-0101",
        password_hash="hash",
    )
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    response = client.post(
        "/reservations/book",
        data={
            "room_type_id": room_type.room_type_id,
            "guest_count": 2,
            "check_in_date": "2026-10-10",
            "check_out_date": "2026-10-13",
        },
    )

    assert response.status_code == 302
    with client.session_transaction() as session:
        assert session["pending_reservation"] == {
            "room_type_id": room_type.room_type_id,
            "guest_count": 2,
            "check_in_date": "2026-10-10",
            "check_out_date": "2026-10-13",
            "number_of_nights": 3,
            "total_cost": "405.00",
        }


def test_booking_rejects_guests_over_room_capacity(database, database_app):
    room_type = RoomType(
        room_name="King",
        description="A spacious room.",
        max_guests=2,
        current_nightly_rate="160.00",
        active=True,
    )
    customer = Customer(
        first_name="Maya",
        last_name="Chen",
        email="maya@example.com",
        telephone="360-555-0101",
        password_hash="hash",
    )
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    response = client.post(
        "/reservations/book",
        data={
            "room_type_id": room_type.room_type_id,
            "guest_count": 3,
            "check_in_date": "2026-10-10",
            "check_out_date": "2026-10-13",
        },
    )

    assert response.status_code == 400
    assert b"accommodates up to 2 guests" in response.data


def test_summary_and_confirmation_create_one_reservation(database, database_app):
    room_type = make_room()
    customer = make_customer()
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    client.post(
        "/reservations/book",
        data={
            "room_type_id": room_type.room_type_id,
            "guest_count": 2,
            "check_in_date": "2026-10-10",
            "check_out_date": "2026-10-13",
        },
    )
    summary_response = client.get("/reservations/summary")
    confirm_response = client.post("/reservations/confirm")

    reservation = Reservation.query.one()
    assert summary_response.status_code == 200
    assert b"$405.00" in summary_response.data
    assert confirm_response.status_code == 302
    assert reservation.customer_id == customer.customer_id
    assert reservation.room_type_id == room_type.room_type_id
    assert reservation.number_of_nights == 3
    assert reservation.total_cost == 405

    repeat_response = client.post("/reservations/confirm")
    assert repeat_response.status_code == 302
    assert Reservation.query.count() == 1


def test_booking_rejects_checkout_before_checkin(database, database_app):
    room_type = make_room()
    customer = make_customer()
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    response = client.post(
        "/reservations/book",
        data={
            "room_type_id": room_type.room_type_id,
            "guest_count": 2,
            "check_in_date": "2026-10-13",
            "check_out_date": "2026-10-10",
        },
    )

    assert response.status_code == 400
    assert b"Check-out must be after check-in." in response.data


def test_lookup_returns_only_signed_in_customer_reservations(database, database_app):
    room_type = make_room()
    customer = make_customer()
    other_customer = make_customer(email="other@example.com")
    db.session.add_all([room_type, customer, other_customer])
    db.session.flush()
    own_reservation = Reservation(
        customer_id=customer.customer_id,
        room_type_id=room_type.room_type_id,
        guest_count=1,
        check_in_date=date(2026, 10, 10),
        check_out_date=date(2026, 10, 12),
        number_of_nights=2,
        nightly_rate="135.00",
        total_cost="270.00",
    )
    other_reservation = Reservation(
        customer_id=other_customer.customer_id,
        room_type_id=room_type.room_type_id,
        guest_count=1,
        check_in_date=date(2026, 10, 14),
        check_out_date=date(2026, 10, 16),
        number_of_nights=2,
        nightly_rate="135.00",
        total_cost="270.00",
    )
    db.session.add_all([own_reservation, other_reservation])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    own_email_response = client.post("/reservations/lookup", data={"query": customer.email})
    other_id_response = client.post(
        "/reservations/lookup", data={"query": other_reservation.reservation_id}
    )
    other_email_response = client.post("/reservations/lookup", data={"query": other_customer.email})

    assert own_email_response.status_code == 200
    assert f"Reservation {own_reservation.reservation_id}".encode() in own_email_response.data
    assert f"Reservation {other_reservation.reservation_id}".encode() not in own_email_response.data
    assert b"No reservations matched that search." in other_id_response.data
    assert other_email_response.status_code == 400
    assert b"Enter your reservation ID" in other_email_response.data
