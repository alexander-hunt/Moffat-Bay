"""SQLAlchemy models mirroring database/migrations/001_create_erd_schema.sql."""

from sqlalchemy import CheckConstraint, UniqueConstraint, func

from .db import db


class Customer(db.Model):
    __tablename__ = "customer"

    customer_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    telephone = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    reservations = db.relationship("Reservation", back_populates="customer")

    __table_args__ = (
        UniqueConstraint("email", name="uk_customer_email"),
        CheckConstraint(
            "CHAR_LENGTH(TRIM(first_name)) > 0", name="chk_customer_first_name_not_blank"
        ),
        CheckConstraint(
            "CHAR_LENGTH(TRIM(last_name)) > 0", name="chk_customer_last_name_not_blank"
        ),
        CheckConstraint("CHAR_LENGTH(TRIM(email)) > 0", name="chk_customer_email_not_blank"),
        CheckConstraint(
            "CHAR_LENGTH(TRIM(telephone)) > 0", name="chk_customer_telephone_not_blank"
        ),
        CheckConstraint(
            "CHAR_LENGTH(TRIM(password_hash)) > 0", name="chk_customer_password_hash_not_blank"
        ),
    )


class RoomType(db.Model):
    __tablename__ = "room_type"

    room_type_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    room_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    max_guests = db.Column(db.SmallInteger, nullable=False)
    current_nightly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    reservations = db.relationship("Reservation", back_populates="room_type")

    __table_args__ = (
        UniqueConstraint("room_name", name="uk_room_type_room_name"),
        CheckConstraint(
            "CHAR_LENGTH(TRIM(room_name)) > 0", name="chk_room_type_room_name_not_blank"
        ),
        CheckConstraint(
            "CHAR_LENGTH(TRIM(description)) > 0",
            name="chk_room_type_description_not_blank",
        ),
        CheckConstraint("max_guests > 0", name="chk_room_type_max_guests_positive"),
        CheckConstraint("current_nightly_rate > 0", name="chk_room_type_rate_positive"),
    )


class Reservation(db.Model):
    __tablename__ = "reservation"

    reservation_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.BigInteger, db.ForeignKey("customer.customer_id"), nullable=False, index=True
    )
    room_type_id = db.Column(
        db.SmallInteger, db.ForeignKey("room_type.room_type_id"), nullable=False, index=True
    )
    guest_count = db.Column(db.SmallInteger, nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    number_of_nights = db.Column(db.SmallInteger, nullable=False)
    nightly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    total_cost = db.Column(db.Numeric(12, 2), nullable=False)
    confirmed_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    customer = db.relationship("Customer", back_populates="reservations")
    room_type = db.relationship("RoomType", back_populates="reservations")

    __table_args__ = (
        CheckConstraint("guest_count > 0", name="chk_reservation_guest_count_positive"),
        CheckConstraint("check_out_date > check_in_date", name="chk_reservation_date_order"),
        CheckConstraint("number_of_nights > 0", name="chk_reservation_nights_positive"),
        CheckConstraint("nightly_rate > 0", name="chk_reservation_rate_positive"),
        CheckConstraint("total_cost > 0", name="chk_reservation_total_positive"),
        CheckConstraint(
            "number_of_nights = DATEDIFF(check_out_date, check_in_date)",
            name="chk_reservation_night_count",
        ),
        CheckConstraint(
            "total_cost = ROUND(nightly_rate * number_of_nights, 2)",
            name="chk_reservation_total",
        ),
        db.Index("ix_reservation_stay_dates", "check_in_date", "check_out_date"),
    )
