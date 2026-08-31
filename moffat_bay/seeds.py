"""Idempotent fictional development data for the Flask application."""

from datetime import date, datetime

from werkzeug.security import generate_password_hash

from .db import db
from .models import Customer, Reservation, RoomType

ROOM_TYPES = [
    {
        "room_type_id": 1,
        "room_name": "Pinewood Studio",
        "description": "Cozy room for 1 or 2. Some views of Joviedsa forest area.",
        "max_guests": 2,
        "current_nightly_rate": "145.00",
        "active": True,
    },
    {
        "room_type_id": 2,
        "room_name": "Alder Suite",
        "description": (
            "Large bedroom with open entertainment room. Amazing views of the Puget Sound."
        ),
        "max_guests": 5,
        "current_nightly_rate": "195.00",
        "active": True,
    },
    {
        "room_type_id": 3,
        "room_name": "Maple Cabin",
        "description": (
            "3 bedrooms and a spacious family room. Direct access to Joviedsa hiking "
            "trails and canoeing access to the Puget Sound."
        ),
        "max_guests": 6,
        "current_nightly_rate": "245.00",
        "active": True,
    },
    {
        "room_type_id": 4,
        "room_name": "Douglas Fir Outpost",
        "description": (
            "Ultimate Family Retreat. Large private cabin with 5 bedrooms, family room, "
            "game room, seating areas indoors/outdoors."
        ),
        "max_guests": 10,
        "current_nightly_rate": "495.00",
        "active": True,
    },
]

# Fictional development-only credentials; plaintext is never stored.
CUSTOMERS = [
    {
        "customer_id": 1,
        "first_name": "Maya",
        "last_name": "Chen",
        "email": "maya.chen@example.com",
        "telephone": "360-555-0101",
        "password": "moffat-dev-maya-01",
    },
    {
        "customer_id": 2,
        "first_name": "Daniel",
        "last_name": "Ruiz",
        "email": "daniel.ruiz@example.com",
        "telephone": "360-555-0102",
        "password": "moffat-dev-daniel-02",
    },
    {
        "customer_id": 3,
        "first_name": "Priya",
        "last_name": "Patel",
        "email": "priya.patel@example.com",
        "telephone": "360-555-0103",
        "password": "moffat-dev-priya-03",
    },
]

RESERVATIONS = [
    {
        "reservation_id": 1,
        "customer_id": 1,
        "room_type_id": 2,
        "guest_count": 2,
        "check_in_date": date(2026, 9, 14),
        "check_out_date": date(2026, 9, 18),
        "number_of_nights": 4,
        "nightly_rate": "135.00",
        "total_cost": "540.00",
        "confirmed_at": datetime(2026, 8, 28, 10, 0, 0),
    },
    {
        "reservation_id": 2,
        "customer_id": 2,
        "room_type_id": 4,
        "guest_count": 2,
        "check_in_date": date(2026, 10, 2),
        "check_out_date": date(2026, 10, 5),
        "number_of_nights": 3,
        "nightly_rate": "160.00",
        "total_cost": "480.00",
        "confirmed_at": datetime(2026, 8, 28, 10, 5, 0),
    },
    {
        "reservation_id": 3,
        "customer_id": 3,
        "room_type_id": 3,
        "guest_count": 4,
        "check_in_date": date(2026, 11, 20),
        "check_out_date": date(2026, 11, 25),
        "number_of_nights": 5,
        "nightly_rate": "150.00",
        "total_cost": "750.00",
        "confirmed_at": datetime(2026, 8, 28, 10, 10, 0),
    },
]


def seed_development_data():
    """Insert or update the fixed fictional dev dataset. Safe to run repeatedly."""
    for row in ROOM_TYPES:
        room_type = db.session.get(RoomType, row["room_type_id"])
        if room_type is None:
            room_type = RoomType(room_type_id=row["room_type_id"])
            db.session.add(room_type)
        for key, value in row.items():
            setattr(room_type, key, value)

    for row in CUSTOMERS:
        customer = db.session.get(Customer, row["customer_id"])
        if customer is None:
            customer = Customer(customer_id=row["customer_id"])
            db.session.add(customer)
        customer.first_name = row["first_name"]
        customer.last_name = row["last_name"]
        customer.email = row["email"]
        customer.telephone = row["telephone"]
        customer.password_hash = generate_password_hash(row["password"])

    for row in RESERVATIONS:
        reservation = db.session.get(Reservation, row["reservation_id"])
        if reservation is None:
            reservation = Reservation(reservation_id=row["reservation_id"])
            db.session.add(reservation)
        for key, value in row.items():
            setattr(reservation, key, value)

    db.session.commit()
