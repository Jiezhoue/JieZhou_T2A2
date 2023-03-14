from main import ma
from marshmallow.validate import Length
from schema.booking_schema import booking_schema, bookings_schema
from marshmallow import fields, validate


# BASIC USER SCHEMAS AREA
class UserSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "f_name", "l_name", "username", "password", "mobile", "admin", "booking")
        load_only = ["username", "password", "admin"]

    booking = ma.List(ma.Nested("BookingSchema", exclude=("user_id", "user",)))

user_schema = UserSchema()
users_schema = UserSchema(many=True)


#This schema is only using for the new user registeration.
class UserRegisterSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "f_name", "l_name", "username", "password", "mobile", "admin", "booking")
        load_only = ["username", "password", "admin"]

    f_name = fields.String(required=True, validate=validate.Length(min=1, error="First name must not be empty."))
    l_name = fields.String(required=True, validate=validate.Length(min=1, error="Last name must not be empty." ))
    username = fields.String(required=True, validate=validate.Length(min=4, error="Username must be at least 4 characters long."))
    mobile = fields.String(validate=validate.Regexp(regex=r'^\d{10}$', error='Mobile number must be a 10-digit number.'))
    password = ma.String(validate=Length(min=8, error="Password must be at least 8 characters long."))

    booking = ma.List(ma.Nested("BookingSchema", exclude=("user_id",)))

user_register_schema = UserRegisterSchema()



#This schema is only used when user do the login
class UserLoginSchema(ma.Schema):

    username = fields.String(required=True, validate=validate.Length(min=4, error="Username must be at least 4 characters long."))
    password = ma.String(validate=Length(min=8, error="Password must be at least 8 characters long."))

user_login_schema = UserLoginSchema()