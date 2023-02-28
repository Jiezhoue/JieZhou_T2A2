from main import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    dentist_id = db.Column(db.Integer, db.ForeignKey("dentists.id"), nullable=False)



