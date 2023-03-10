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


class BookingDentistSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "date", "time", "status", "user_id", "user", "treatment")
        load_only = ["user_id"]

    treatment = ma.List(ma.Nested("TreatmentSchema"))
    user = ma.Nested("UserSchema", exclude=("id", "username", "password", "mobile", "admin", "booking",))


booking_dentist_schema = BookingDentistSchema()
bookings_dentist_schema = BookingDentistSchema(many=True)

is there anyway to combine those two schema, but still need to return different fields