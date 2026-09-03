"""Reservation feature routes and forms."""

from flask import Blueprint

reservations_bp = Blueprint("reservations", __name__, url_prefix="/reservations")

from . import routes  # noqa: E402, F401
