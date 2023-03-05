from main import ma


class DentistSchema(ma.Schema):
    
    class Meta:
        ordered= True

        fields = ("id", "f_name", "l_name", "username", "password", "speciality")
        load_only = ["username", "password"]



dentist_schema = DentistSchema()
dentists_schema = DentistSchema(many=True)