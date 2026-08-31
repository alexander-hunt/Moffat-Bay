"""Small helpers for the authenticated customer session."""

from flask import session

from ..models import Customer

CUSTOMER_SESSION_KEY = "customer_id"


def log_in(customer: Customer) -> None:
    """Start a new authenticated session for a customer."""
    session.clear()
    session[CUSTOMER_SESSION_KEY] = customer.customer_id


def log_out() -> None:
    """Remove the authenticated customer from the session."""
    session.clear()
