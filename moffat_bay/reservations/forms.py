"""Form definitions for reservation requests."""

from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class ReservationForm(FlaskForm):
    """Collect a room selection and stay details."""

    room_type_id = SelectField("Room", coerce=int, validators=[DataRequired()])
    guest_count = IntegerField(
        "Number of guests", validators=[DataRequired(), NumberRange(min=1, max=10)]
    )
    check_in_date = DateField("Check-in date", validators=[DataRequired()])
    check_out_date = DateField("Check-out date", validators=[DataRequired()])
    submit = SubmitField("Review reservation")

    def __init__(self, room_types, *args, **kwargs):
        """Set choices and retain the server-authoritative room records."""
        super().__init__(*args, **kwargs)
        self.room_types_by_id = {room_type.room_type_id: room_type for room_type in room_types}
        self.room_type_id.choices = [
            (
                room_type.room_type_id,
                f"{room_type.room_name} - ${room_type.current_nightly_rate:.2f} per night",
            )
            for room_type in room_types
        ]

    def validate_room_type_id(self, field):
        """Reject inactive or altered room selections."""
        if field.data not in self.room_types_by_id:
            raise ValidationError("Select an available room.")

    def validate_guest_count(self, field):
        """Require the selected room to accommodate every guest."""
        room_type = self.room_types_by_id.get(self.room_type_id.data)
        if room_type is not None and field.data is not None and field.data > room_type.max_guests:
            raise ValidationError(
                f"{room_type.room_name} accommodates up to {room_type.max_guests} guests."
            )

    def validate_check_out_date(self, field):
        """Require checkout after check-in."""
        if self.check_in_date.data is not None and field.data is not None:
            if field.data <= self.check_in_date.data:
                raise ValidationError("Check-out must be after check-in.")


class ReservationLookupForm(FlaskForm):
    """Collect a reservation ID or the signed-in customer's email address."""

    query = StringField(
        "Reservation ID or email address", validators=[DataRequired(), Length(max=254)]
    )
    submit = SubmitField("Search reservations")
