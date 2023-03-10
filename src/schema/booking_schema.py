from main import ma


class BookingSchema(ma.Schema):
    class Meta:
        ordered= True

        # fields = ("id", "date", "time", "status", "user_id", "user", "dentist_id", "dentist", "treatment")
        fields = ("id", "date", "time", "status", "user_id", "dentist_id", "dentist", "treatment")
        load_only = ["user_id", "dentist_id"]

    treatment = ma.List(ma.Nested("TreatmentSchema"))
    dentist = ma.Nested("DentistSchema", exclude=("id", "speciality",))
    user = ma.Nested("UserSchema", exclude=("id", "username", "password", "mobile", "admin", "booking",))


booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

class SimpleBookingSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "date", "time", "status", "user", "dentist_id", "dentist")
        load_only = ["user_id", "dentist_id"]

    dentist = ma.Nested("DentistSchema", exclude=("id", "speciality",))
    user = ma.Nested("UserSchema", exclude=("id", "username", "password", "mobile", "admin", "booking",))


simple_booking_schema = SimpleBookingSchema()
simple_bookings_schema = SimpleBookingSchema(many=True)

class TreatmentBookingSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "date", "time", "status", "user", "dentist_id", "treatment")
        load_only = ["user_id", "dentist_id"]
        
    treatment = ma.List(ma.Nested("TreatmentSchema"))
    dentist = ma.Nested("DentistSchema", exclude=("id", "speciality",))
    user = ma.Nested("UserSchema", exclude=("id", "username", "password", "mobile", "admin", "booking",))


treatment_booking_schema = TreatmentBookingSchema()
treatment_bookings_schema = TreatmentBookingSchema(many=True)