"""Form definitions for authentication requests."""

import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from ..models import Customer

PASSWORD_PATTERN = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}")


class LoginForm(FlaskForm):
    """Collect credentials for an existing customer."""

    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=254)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class RegistrationForm(FlaskForm):
    """Collect and validate required customer registration details."""

    first_name = StringField("First name", validators=[DataRequired(), Length(max=100)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email address", validators=[DataRequired(), Email(), Length(max=254)])
    telephone = StringField("Telephone", validators=[DataRequired(), Length(max=32)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Create account")

    def validate_email(self, field):
        """Reject email addresses that are already registered."""
        email = field.data.strip().lower()
        if Customer.query.filter_by(email=email).first() is not None:
            raise ValidationError("An account already exists for this email address.")

    def validate_password(self, field):
        """Require the course password policy."""
        if PASSWORD_PATTERN.fullmatch(field.data) is None:
            raise ValidationError(
                "Use at least 8 characters with an uppercase letter, lowercase letter, and number."
            )
