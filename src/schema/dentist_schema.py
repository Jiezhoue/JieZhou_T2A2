from main import ma
from marshmallow import fields, validate
from marshmallow.validate import Length

class DentistSchema(ma.Schema):
    
    class Meta:
        ordered= True

        fields = ("id", "f_name", "l_name", "username", "password", "speciality")
        load_only = ["username", "password"]
    username = fields.String(required=True, validate=validate.Length(min=4, error="Username must be at least 4 characters long."))
    password = ma.String(validate=Length(min=8, error="Password must be at least 8 characters long."))

dentist_schema = DentistSchema()
dentists_schema = DentistSchema(many=True)
