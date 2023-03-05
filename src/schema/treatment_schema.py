from main import ma


class TreatmentSchema(ma.Schema):
    class Meta:
        ordered= True

        fields = ("id", "service", "fee", "booking_id")
        load_only = ["booking_id"]



treatment_schema = TreatmentSchema()
treatments_schema = TreatmentSchema(many=True)