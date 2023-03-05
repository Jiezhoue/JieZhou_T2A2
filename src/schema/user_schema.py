from main import ma
from marshmallow.validate import Length
from schema.booking_schema import booking_schema, bookings_schema


# SCHEMAS AREA
class UserSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "f_name", "l_name", "username", "password", "mobile", "admin", "booking")
        load_only = ["username", "password", "admin"]
    password = ma.String(validate=Length(min=8))
    booking = ma.List(ma.Nested("BookingSchema", exclude=("user_id",)))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
