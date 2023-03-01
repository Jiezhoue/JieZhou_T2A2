from flask import Blueprint, jsonify, request, abort

from models.dentists import Dentist
from schema.dentist_schema import dentist_schema, dentists_schema
from main import db

from main import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User

from models.bookings import Booking
from schema.booking_schema import booking_schema, bookings_schema


dentist = Blueprint('dentist', __name__, url_prefix="/dentists")

@dentist.get("/")
def get_dentist():
    dentist = Dentist.query.all()
    result = dentists_schema.dump(dentist)

    return jsonify(result)


@dentist.post("/login")
def dentist_login():
        
    dentist_fields = dentist_schema.load(request.json)
    dentist = Dentist.query.filter_by(username=dentist_fields["username"]).first()
    if not dentist:
        return abort(401, description="username is not exist")
    elif not bcrypt.check_password_hash(dentist.password, dentist_fields["password"]):
        return abort(401, description="password is not right")
    access_token = create_access_token(identity=str(dentist.username))
    return jsonify({"dentist": dentist.username, "token": access_token})


@dentist.post("/signup")
@jwt_required()
def dentist_signup():
    user_username = get_jwt_identity()
    user = User.query.filter_by(username=user_username).first()
    if not user:
        return abort(400, description="Invalid User")
    
    if not user.admin:
        return abort(400, description="You don't have permission to access system")

    dentist_fields = dentist_schema.load(request.json)
    dentist = Dentist.query.filter_by(username=dentist_fields["username"]).first()
    if dentist:
        return abort(401, description="This dentist is already registered.")

    dentist = Dentist()
    dentist.f_name = dentist_fields["f_name"]
    dentist.l_name = dentist_fields["l_name"]

    if "speciality" in dentist_fields:
        dentist.speciality = dentist_fields["speciality"]
    dentist.username = dentist_fields["username"]
    dentist.password = bcrypt.generate_password_hash(dentist_fields["password"]).decode("utf-8")

    db.session.add(dentist)
    db.session.commit()

    access_token = create_access_token(identity=str(dentist.username))
    return jsonify({"user": dentist.username, "token":access_token})


@dentist.post("/<int:id>/booking")
@jwt_required()
def book_treatment(id):
    user_name = get_jwt_identity()
    user = User.query.filter_by(username=user_name).first()
    if not user:
        return abort(401, description="Invaild user")
    
    booking_fields = booking_schema.load(request.json)
    booking = Booking()
    booking.date = booking_fields["date"]
    booking.time = booking_fields["time"]
    booking.user_id = user.id
    booking.dentist_id = id
    db.session.add(booking)
    db.session.commit()

    return jsonify(booking_schema.dump(booking))