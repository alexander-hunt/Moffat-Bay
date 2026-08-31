"""Authentication request handlers."""

from flask import flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import db
from ..models import Customer
from . import auth_bp
from .forms import LoginForm, RegistrationForm
from .helpers import log_in, log_out


@auth_bp.get("/account")
def account():
    """Render the combined login and registration page."""
    return render_template(
        "auth/account.html", login_form=LoginForm(), registration_form=RegistrationForm()
    )


@auth_bp.post("/login")
def login():
    """Authenticate a customer and start a session."""
    login_form = LoginForm()
    registration_form = RegistrationForm()
    if not login_form.validate_on_submit():
        return render_template(
            "auth/account.html", login_form=login_form, registration_form=registration_form
        ), 400

    email = login_form.email.data.strip().lower()
    customer = Customer.query.filter_by(email=email).first()
    if customer is None or not check_password_hash(
        customer.password_hash, login_form.password.data
    ):
        login_form.password.errors.append("Invalid email address or password.")
        return render_template(
            "auth/account.html", login_form=login_form, registration_form=registration_form
        ), 401

    log_in(customer)
    flash("You are now logged in.", "success")
    return redirect(url_for("public.index"))


@auth_bp.post("/register")
def register():
    """Create a customer account and authenticate the new customer."""
    login_form = LoginForm()
    registration_form = RegistrationForm()
    if not registration_form.validate_on_submit():
        return render_template(
            "auth/account.html", login_form=login_form, registration_form=registration_form
        ), 400

    customer = Customer(
        first_name=registration_form.first_name.data.strip(),
        last_name=registration_form.last_name.data.strip(),
        email=registration_form.email.data.strip().lower(),
        telephone=registration_form.telephone.data.strip(),
        password_hash=generate_password_hash(registration_form.password.data),
    )
    db.session.add(customer)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        registration_form.email.errors.append("An account already exists for this email address.")
        return render_template(
            "auth/account.html", login_form=login_form, registration_form=registration_form
        ), 400

    log_in(customer)
    flash("Your account has been created.", "success")
    return redirect(url_for("public.index"))


@auth_bp.post("/logout")
def logout():
    """End the authenticated session."""
    log_out()
    flash("You have been logged out.", "success")
    return redirect(url_for("public.index"))
