"""Reservation workflow tests."""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from werkzeug.datastructures import MultiDict

from moffat_bay.db import db
from moffat_bay.models import Customer, Reservation, RoomType
from moffat_bay.reservations.forms import ReservationLookupForm

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


def make_reservation(customer, room_type, check_in_date="2026-10-10", nightly_rate="135.00"):
    """Build a confirmed reservation for lookup tests."""
    check_in = date.fromisoformat(check_in_date)
    return Reservation(
        customer_id=customer.customer_id,
        room_type_id=room_type.room_type_id,
        guest_count=2,
        check_in_date=check_in,
        check_out_date=check_in + timedelta(days=3),
        number_of_nights=3,
        nightly_rate=nightly_rate,
        total_cost=Decimal(nightly_rate) * 3,
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


def test_stays_requires_login(client):
    response = client.get("/reservations/stays")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/account")


def test_lookup_form_accepts_reservation_id_when_csrf_is_enabled(app):
    app.config["WTF_CSRF_ENABLED"] = True
    with app.test_request_context("/reservations/stays?query=6"):
        form = ReservationLookupForm(formdata=MultiDict({"query": "6"}))

        assert form.validate()


def test_stays_lists_customer_reservations_in_date_order_and_uses_historical_prices(
    database, database_app
):
    room_type = make_room(room_name="Alder Suite", max_guests=5, nightly_rate="204.75")
    customer = make_customer()
    other_customer = make_customer(email="other@example.com")
    db.session.add_all([room_type, customer, other_customer])
    db.session.flush()
    later_reservation = make_reservation(customer, room_type, check_in_date="2026-11-10")
    earlier_reservation = make_reservation(
        customer, room_type, check_in_date="2026-10-10", nightly_rate="195.00"
    )
    other_reservation = make_reservation(other_customer, room_type)
    db.session.add_all([later_reservation, earlier_reservation, other_reservation])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    response = client.get("/reservations/stays")

    assert response.status_code == 200
    assert b"My stays" in response.data
    assert b"Coming soon" not in response.data
    assert response.data.index(str(earlier_reservation.reservation_id).encode()) < (
        response.data.index(str(later_reservation.reservation_id).encode())
    )
    assert f"<h2>Reservation {other_reservation.reservation_id}</h2>".encode() not in response.data
    assert b"$195.00" in response.data
    assert b"$204.75" not in response.data


def test_stays_filters_by_reservation_id_or_normalized_account_email(database, database_app):
    room_type = make_room()
    customer = make_customer()
    db.session.add_all([room_type, customer])
    db.session.flush()
    first_reservation = make_reservation(customer, room_type, check_in_date="2026-10-10")
    second_reservation = make_reservation(customer, room_type, check_in_date="2026-11-10")
    db.session.add_all([first_reservation, second_reservation])
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    id_response = client.get(f"/reservations/stays?query={first_reservation.reservation_id}")
    email_response = client.get("/reservations/stays?query=%20MAYA%40EXAMPLE.COM%20")
    first_heading = f"<h2>Reservation {first_reservation.reservation_id}</h2>".encode()
    second_heading = f"<h2>Reservation {second_reservation.reservation_id}</h2>".encode()

    assert first_heading in id_response.data
    assert second_heading not in id_response.data
    assert b"No confirmed stays match that lookup." not in id_response.data
    assert first_heading in email_response.data
    assert second_heading in email_response.data


def test_stays_rejects_invalid_lookup_and_hides_other_customers_reservations(
    database, database_app
):
    room_type = make_room()
    customer = make_customer()
    other_customer = make_customer(email="other@example.com")
    db.session.add_all([room_type, customer, other_customer])
    db.session.flush()
    other_reservation = make_reservation(other_customer, room_type)
    db.session.add(other_reservation)
    db.session.commit()
    client = database_app.test_client()
    log_in(client, customer)

    invalid_response = client.get("/reservations/stays?query=not-a-lookup")
    foreign_id_response = client.get(
        f"/reservations/stays?query={other_reservation.reservation_id}"
    )
    foreign_email_response = client.get("/reservations/stays?query=other%40example.com")

    assert invalid_response.status_code == 400
    assert b"Enter a positive reservation ID or a valid email address." in invalid_response.data
    assert foreign_id_response.status_code == 200
    assert foreign_email_response.status_code == 200
    assert b"No confirmed stays match that lookup." in foreign_id_response.data
    assert b"No confirmed stays match that lookup." in foreign_email_response.data
    assert (
        f"<h2>Reservation {other_reservation.reservation_id}</h2>".encode()
        not in foreign_id_response.data
    )
