from main import db

class Treatment(db.Model):
    __tablename__ = 'treatments'
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(), nullable=False)
    fee = db.Column(db.Numeric(10,2), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)

