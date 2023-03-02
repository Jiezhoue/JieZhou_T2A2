from flask import jsonify, Blueprint, request, abort
from main import db
from models.users import User
from schema.user_schema import user_schema, users_schema
from main import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.bookings import Booking
from schema.booking_schema import booking_schema, bookings_schema
from models.treatments import Treatment
from schema.treatment_schema import treatment_schema, treatments_schema



patient = Blueprint('patient', __name__, url_prefix='/patient')

@patient.get("/info")
@jwt_required()
def patient_info():
    user_name = get_jwt_identity()
    user = User.query.filter_by(username=user_name).first()
    if not user:
        return abort(401, description="Invaild user")
    
    result = user_schema.dump(user)
    return jsonify(result)


@patient.delete("/cancel")
@jwt_required()
def cancel_booking():
    user_name = get_jwt_identity()
    user = User.query.filter_by(username=user_name).first()
    if not user:
        return abort(401, description="Invaild user")
    
    booking = Booking.query.filter_by(user_id=user.id, status="Open").first()
    if not booking:
        return abort(400, description="no booking in the system")
    db.session.delete(booking)
    db.session.commit()

    return jsonify(booking_schema.dump(booking))
    


@patient.get("/treatment")
def treatment():
    treatment = Treatment.query.all()

    return jsonify(treatments_schema.dump(treatment))


@patient.get("/bookings")
def bookings():
    bookings = Booking.query.all()

    return jsonify(bookings_schema.dump(bookings))

    

