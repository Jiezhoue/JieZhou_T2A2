from main import ma


class BookingSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "date", "time", "status", "user_id", "user", "dentist_id", "dentist", "treatment")
        load_only = ["user_id", "dentist_id"]

    treatment = ma.List(ma.Nested("TreatmentSchema"))
    dentist = ma.Nested("DentistSchema", exclude=("id", "speciality",))
    user = ma.Nested("UserSchema", exclude=("id", "username", "password", "mobile", "admin", "booking",))

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)



# class BookingUserSchema(ma.Schema):
#     class Meta:
#         ordered= True

#         fields = ("id", "date", "time", "status", "user", "dentist_id", "dentist")
#         load_only = ["user_id", "dentist_id"]

#     dentist = ma.Nested("DentistSchema", exclude=("id", "speciality",))
#     user = ma.Nested("UserSchema", exclude=("id", "username", "password", "mobile", "admin", "booking",))

# booking_user_schema = BookingUserSchema()
# bookings_user_schema = BookingUserSchema(many=True)


# BookingDentistSchema inherits from BookingSchema and overrides the fields to return different fields as needed.
class BookingDentistSchema(BookingSchema):
    class Meta:
        ordered = True
        fields = ("id", "date", "time", "status", "user_id", "user", "treatment")
        load_only = ["user_id"]

booking_dentist_schema = BookingDentistSchema()
bookings_dentist_schema = BookingDentistSchema(many=True)