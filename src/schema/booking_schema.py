from main import ma


class BookingSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "date", "time", "status", "user_id", "user", "dentist_id", "dentist", "treatment")
    treatment = ma.List(ma.Nested("TreatmentSchema"))
    dentist = ma.Nested("DentistSchema")
    user = ma.Nested("UserSchema", exclude=("id", "username", "password", "mobile", "admin", "booking",))


booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)