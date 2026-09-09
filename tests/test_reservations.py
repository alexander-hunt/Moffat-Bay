"""Reservation workflow tests."""

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


def make_room(room_name="Queen", max_guests=2, nightly_rate="135.00", active=True):
    """Build a room type for a test stay."""
    return RoomType(
        room_name=room_name,
        description="A restful room.",
        max_guests=max_guests,
        current_nightly_rate=nightly_rate,
        active=active,
    )


def booking_data(
    room_type_id, guest_count=2, check_in_date="2026-10-10", check_out_date="2026-10-13"
):
    """Return a valid reservation form payload by default."""
    return {
        "room_type_id": room_type_id,
        "guest_count": guest_count,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
    }


def test_booking_requires_login(client):
    response = client.get("/reservations/book")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/account")


def test_booking_renders_only_active_room_choices(database, database_app):
    active_room = make_room(room_name="King", nightly_rate="160.00")
    inactive_room = make_room(room_name="Closed Cabin", active=False)
    customer = make_customer()
    db.session.add_all([active_room, inactive_room, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    response = client.get("/reservations/book")

    assert response.status_code == 200
    assert b"King - $160.00 per night" in response.data
    assert b"Closed Cabin" not in response.data


def test_booking_stores_server_calculated_pending_reservation(database, database_app):
    room_type = make_room()
    customer = make_customer()
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    response = client.post("/reservations/book", data=booking_data(room_type.room_type_id))

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


@pytest.mark.parametrize(
    ("payload", "expected_error"),
    [
        ({"room_type_id": 999}, b"Select an available room."),
        ({"guest_count": 3}, b"accommodates up to 2 guests"),
        ({"check_out_date": "2026-10-10"}, b"Check-out must be after check-in."),
    ],
)
def test_booking_rejects_invalid_stay_details(database, database_app, payload, expected_error):
    room_type = make_room()
    customer = make_customer()
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)
    form_data = booking_data(room_type.room_type_id)
    form_data.update(payload)

    response = client.post("/reservations/book", data=form_data)

    assert response.status_code == 400
    assert expected_error in response.data


def test_cancel_discards_pending_reservation_without_persisting(database, database_app):
    room_type = make_room()
    customer = make_customer()
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)
    client.post("/reservations/book", data=booking_data(room_type.room_type_id))

    response = client.post("/reservations/cancel")

    assert response.status_code == 302
    assert Reservation.query.count() == 0
    with client.session_transaction() as session:
        assert "pending_reservation" not in session


def test_summary_and_confirmation_create_one_customer_owned_reservation(database, database_app):
    room_type = make_room(room_name="Alder Suite", max_guests=5, nightly_rate="204.75")
    customer = make_customer()
    db.session.add_all([room_type, customer])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)
    client.post("/reservations/book", data=booking_data(room_type.room_type_id))

    summary_response = client.get("/reservations/summary")
    confirm_response = client.post("/reservations/confirm")

    reservation = Reservation.query.one()
    assert summary_response.status_code == 200
    assert b"$204.75" in summary_response.data
    assert b"$614.25" in summary_response.data
    assert confirm_response.status_code == 302
    assert reservation.customer_id == customer.customer_id
    assert reservation.room_type_id == room_type.room_type_id
    assert reservation.number_of_nights == 3
    assert reservation.nightly_rate == 204.75
    assert reservation.total_cost == 614.25

    repeat_response = client.post("/reservations/confirm")
    assert repeat_response.status_code == 302
    assert Reservation.query.count() == 1


def test_confirmation_is_limited_to_the_signed_in_customer(database, database_app):
    room_type = make_room()
    owner = make_customer()
    other_customer = make_customer(email="other@example.com")
    db.session.add_all([room_type, owner, other_customer])
    db.session.flush()
    reservation = Reservation(
        customer_id=owner.customer_id,
        room_type_id=room_type.room_type_id,
        guest_count=2,
        check_in_date="2026-10-10",
        check_out_date="2026-10-13",
        number_of_nights=3,
        nightly_rate="135.00",
        total_cost="405.00",
    )
    db.session.add(reservation)
    db.session.commit()
    client = database_app.test_client()
    log_in(client, other_customer)

    response = client.get(f"/reservations/confirmation/{reservation.reservation_id}")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/reservations/book")


def test_confirmation_displays_the_reservation_historical_nightly_rate(database, database_app):
    room_type = make_room(room_name="Alder Suite", max_guests=5, nightly_rate="204.75")
    customer = make_customer()
    db.session.add_all([room_type, customer])
    db.session.flush()
    reservation = Reservation(
        customer_id=customer.customer_id,
        room_type_id=room_type.room_type_id,
        guest_count=2,
        check_in_date="2026-10-10",
        check_out_date="2026-10-13",
        number_of_nights=3,
        nightly_rate="195.00",
        total_cost="585.00",
    )
    db.session.add(reservation)
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    response = client.get(f"/reservations/confirmation/{reservation.reservation_id}")

    assert response.status_code == 200
    assert b"$195.00" in response.data
    assert b"$204.75" not in response.data
