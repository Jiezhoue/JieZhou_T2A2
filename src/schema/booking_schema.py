from main import ma


class BookingSchema(ma.Schema):
  class Meta:
    ordered= True

    fields = ("id", "date", "time", "status", "user_id", "dentist_id")



booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)