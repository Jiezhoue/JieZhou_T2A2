from main import ma


class DentistSchema(ma.Schema):
    
    class Meta:
        ordered= True

        fields = ("id", "f_name", "l_name", "username", "password", "speciality")
        load_only = ["username", "password"]
    # booking = ma.List(ma.Nested("BookingSchema", exclude=("id", "user_id", "dentist_id", "dentist", "treatment",)))


dentist_schema = DentistSchema()
dentists_schema = DentistSchema(many=True)