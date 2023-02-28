from main import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(), nullable=False)
    l_name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    mobile = db.Column(db.String())
    admin = db.Column(db.Boolean(), default=False)

    booking = db.relationship(
        "Booking",
        backref="user",
        cascade="all, delete"
    )
