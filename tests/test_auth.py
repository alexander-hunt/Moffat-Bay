"""Database-backed authentication workflow tests."""

import pytest
from werkzeug.security import check_password_hash, generate_password_hash

from moffat_bay.db import db
from moffat_bay.models import Customer

pytestmark = pytest.mark.database


def make_customer(**changes):
    values = {
        "first_name": "Maya",
        "last_name": "Chen",
        "email": "maya.chen@example.com",
        "telephone": "360-555-0101",
        "password_hash": generate_password_hash("ValidPass1"),
    }
    values.update(changes)
    return Customer(**values)


def test_account_page_loads(database, database_app):
    response = database_app.test_client().get("/account")

    assert response.status_code == 200
    assert b"Create an account" in response.data


def test_registration_creates_hashed_customer_and_session(database, database_app):
    client = database_app.test_client()
    response = client.post(
        "/register",
        data={
            "first_name": "Priya",
            "last_name": "Patel",
            "email": "PRIYA.PATEL@example.com",
            "telephone": "360-555-0103",
            "password": "ValidPass1",
            "confirm_password": "ValidPass1",
        },
    )

    customer = Customer.query.filter_by(email="priya.patel@example.com").one()
    assert response.status_code == 302
    assert check_password_hash(customer.password_hash, "ValidPass1")
    assert customer.password_hash != "ValidPass1"
    with client.session_transaction() as session:
        assert session["customer_id"] == customer.customer_id


def test_registration_rejects_duplicate_email(database, database_app):
    db.session.add(make_customer())
    db.session.commit()

    response = database_app.test_client().post(
        "/register",
        data={
            "first_name": "Maya",
            "last_name": "Chen",
            "email": "MAYA.CHEN@example.com",
            "telephone": "360-555-0101",
            "password": "ValidPass1",
            "confirm_password": "ValidPass1",
        },
    )

    assert response.status_code == 400
    assert b"An account already exists" in response.data


@pytest.mark.parametrize("field", ["first_name", "last_name", "email", "telephone", "password"])
def test_registration_requires_each_course_field(database, database_app, field):
    data = {
        "first_name": "Priya",
        "last_name": "Patel",
        "email": "priya.patel@example.com",
        "telephone": "360-555-0103",
        "password": "ValidPass1",
        "confirm_password": "ValidPass1",
    }
    data[field] = ""

    response = database_app.test_client().post("/register", data=data)

    assert response.status_code == 400


def test_registration_rejects_invalid_email_and_password_confirmation(database, database_app):
    response = database_app.test_client().post(
        "/register",
        data={
            "first_name": "Priya",
            "last_name": "Patel",
            "email": "not-an-email",
            "telephone": "360-555-0103",
            "password": "ValidPass1",
            "confirm_password": "DifferentPass1",
        },
    )

    assert response.status_code == 400
    assert b"Invalid email address." in response.data
    assert b"Field must be equal to password." in response.data


@pytest.mark.parametrize(
    "password", ["short1A", "alllowercase1", "ALLUPPERCASE1", "NoNumberPassword"]
)
def test_registration_enforces_password_policy(database, database_app, password):
    response = database_app.test_client().post(
        "/register",
        data={
            "first_name": "Priya",
            "last_name": "Patel",
            "email": "priya.patel@example.com",
            "telephone": "360-555-0103",
            "password": password,
            "confirm_password": password,
        },
    )

    assert response.status_code == 400
    assert b"Use at least 8 characters" in response.data


def test_login_starts_session_for_valid_credentials(database, database_app):
    customer = make_customer()
    db.session.add(customer)
    db.session.commit()
    client = database_app.test_client()

    response = client.post(
        "/login", data={"email": "MAYA.CHEN@example.com", "password": "ValidPass1"}
    )

    assert response.status_code == 302
    with client.session_transaction() as session:
        assert session["customer_id"] == customer.customer_id


def test_login_rejects_invalid_credentials(database, database_app):
    client = database_app.test_client()
    response = client.post(
        "/login", data={"email": "unknown@example.com", "password": "ValidPass1"}
    )

    assert response.status_code == 401
    assert b"Invalid email address or password." in response.data


def test_logout_clears_customer_session(database, database_app):
    client = database_app.test_client()
    with client.session_transaction() as session:
        session["customer_id"] = 1

    response = client.post("/logout")

    assert response.status_code == 302
    with client.session_transaction() as session:
        assert "customer_id" not in session
