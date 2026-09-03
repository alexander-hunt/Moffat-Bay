"""Reservation request handlers."""

from datetime import date
from functools import wraps

from flask import flash, redirect, render_template, session, url_for
from sqlalchemy.exc import IntegrityError

from ..auth.helpers import CUSTOMER_SESSION_KEY
from ..db import db
from ..models import Customer, Reservation, RoomType
from . import reservations_bp
from .forms import ReservationForm, ReservationLookupForm

PENDING_RESERVATION_SESSION_KEY = "pending_reservation"


def login_required(view):
    """Redirect guests to account access before reservation actions."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get(CUSTOMER_SESSION_KEY) is None:
            return redirect(url_for("auth.account"))
        return view(*args, **kwargs)

    return wrapped_view


def pending_reservation_details():
    """Rebuild trustworthy pending details from the selected room and dates."""
    pending = session.get(PENDING_RESERVATION_SESSION_KEY)
    if not isinstance(pending, dict):
        return None

    try:
        room_type_id = int(pending["room_type_id"])
        guest_count = int(pending["guest_count"])
        check_in_date = date.fromisoformat(pending["check_in_date"])
        check_out_date = date.fromisoformat(pending["check_out_date"])
    except (KeyError, TypeError, ValueError):
        return None

    room_type = db.session.get(RoomType, room_type_id)
    if (
        room_type is None
        or not room_type.active
        or guest_count < 1
        or guest_count > room_type.max_guests
        or check_out_date <= check_in_date
    ):
        return None

    number_of_nights = (check_out_date - check_in_date).days
    return {
        "room_type": room_type,
        "guest_count": guest_count,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "number_of_nights": number_of_nights,
        "total_cost": room_type.current_nightly_rate * number_of_nights,
    }


def current_customer():
    """Return the authenticated customer, if the session remains valid."""
    return db.session.get(Customer, session.get(CUSTOMER_SESSION_KEY))


@reservations_bp.get("/book")
@login_required
def book():
    """Render the room and stay selection page."""
    room_types = RoomType.query.filter_by(active=True).order_by(RoomType.room_type_id).all()
    return render_template("reservations/book.html", form=ReservationForm(room_types))


@reservations_bp.post("/book")
@login_required
def review_booking():
    """Validate a stay selection and store it for review."""
    room_types = RoomType.query.filter_by(active=True).order_by(RoomType.room_type_id).all()
    form = ReservationForm(room_types)
    if not form.validate_on_submit():
        return render_template("reservations/book.html", form=form), 400

    room_type = form.room_types_by_id[form.room_type_id.data]
    number_of_nights = (form.check_out_date.data - form.check_in_date.data).days
    total_cost = room_type.current_nightly_rate * number_of_nights
    session[PENDING_RESERVATION_SESSION_KEY] = {
        "room_type_id": room_type.room_type_id,
        "guest_count": form.guest_count.data,
        "check_in_date": form.check_in_date.data.isoformat(),
        "check_out_date": form.check_out_date.data.isoformat(),
        "number_of_nights": number_of_nights,
        "total_cost": str(total_cost),
    }
    return redirect(url_for("reservations.summary"))


@reservations_bp.get("/summary")
@login_required
def summary():
    """Render the pending reservation summary."""
    reservation = pending_reservation_details()
    if reservation is None:
        session.pop(PENDING_RESERVATION_SESSION_KEY, None)
        flash("Choose valid stay details before reviewing your reservation.", "error")
        return redirect(url_for("reservations.book"))
    return render_template("reservations/summary.html", reservation=reservation)


@reservations_bp.post("/cancel")
@login_required
def cancel_booking():
    """Discard a pending selection without saving a reservation."""
    session.pop(PENDING_RESERVATION_SESSION_KEY, None)
    flash("Your pending reservation has been cancelled.", "success")
    return redirect(url_for("reservations.book"))


@reservations_bp.post("/confirm")
@login_required
def confirm_booking():
    """Persist one validated pending reservation for the authenticated customer."""
    customer = current_customer()
    reservation_details = pending_reservation_details()
    session.pop(PENDING_RESERVATION_SESSION_KEY, None)
    if customer is None or reservation_details is None:
        flash("Choose valid stay details before confirming your reservation.", "error")
        return redirect(url_for("reservations.book"))

    reservation = Reservation(
        customer_id=customer.customer_id,
        room_type_id=reservation_details["room_type"].room_type_id,
        guest_count=reservation_details["guest_count"],
        check_in_date=reservation_details["check_in_date"],
        check_out_date=reservation_details["check_out_date"],
        number_of_nights=reservation_details["number_of_nights"],
        nightly_rate=reservation_details["room_type"].current_nightly_rate,
        total_cost=reservation_details["total_cost"],
    )
    db.session.add(reservation)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("We could not confirm that reservation. Please start again.", "error")
        return redirect(url_for("reservations.book"))

    return redirect(url_for("reservations.confirmation", reservation_id=reservation.reservation_id))


@reservations_bp.get("/confirmation/<int:reservation_id>")
@login_required
def confirmation(reservation_id):
    """Display a confirmed reservation belonging to the signed-in customer."""
    customer = current_customer()
    reservation = Reservation.query.filter_by(
        reservation_id=reservation_id, customer_id=customer.customer_id if customer else None
    ).first()
    if reservation is None:
        flash("Reservation not found.", "error")
        return redirect(url_for("reservations.lookup"))
    return render_template("reservations/confirmation.html", reservation=reservation)


@reservations_bp.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    """Find confirmed reservations that belong to the signed-in customer."""
    form = ReservationLookupForm()
    reservations = None
    if form.validate_on_submit():
        customer = current_customer()
        query = form.query.data.strip()
        if customer is None:
            return redirect(url_for("auth.account"))
        if query.isdigit():
            reservations = Reservation.query.filter_by(
                reservation_id=int(query), customer_id=customer.customer_id
            ).all()
        elif query.lower() == customer.email.lower():
            reservations = Reservation.query.filter_by(customer_id=customer.customer_id).all()
        else:
            form.query.errors.append("Enter your reservation ID or your account email address.")
            return render_template("reservations/lookup.html", form=form, reservations=None), 400
    return render_template("reservations/lookup.html", form=form, reservations=reservations)
