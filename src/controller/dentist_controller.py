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
from datetime import datetime

from models.treatments import Treatment
from schema.treatment_schema import treatment_schema, treatments_schema

from controller.user_controller import user_authentication

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


from controller.user_controller import admin_authentication

@dentist.post("/signup")
@jwt_required()
@admin_authentication
def dentist_signup():
    # user_username = get_jwt_identity()
    # user = User.query.filter_by(username=user_username).first()
    # if not user:
    #     return abort(400, description="Invalid User")
    
    # if not user.admin:
    #     return abort(400, description="You don't have permission to access system")

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

    dentist = Dentist.query.filter_by(id=id).first()

    if not dentist:
        return abort(400, description="dentist not exist")
    
    exist = Booking.query.filter_by(user_id=user.id, status="Open").first()
    if exist:
        return abort(400, description="You already have a open booking in the system. Before booking a new one, please ensure to cancel any existing booking in the system.")

    data = Booking.query.filter_by(dentist_id=id, date=booking_fields["date"])


    for book in data:
        t1 = datetime.strptime(str(book.time), '%H:%M:%S')
        print(t1)
        t2 = datetime.strptime(booking_fields["time"], '%H:%M:%S')
        print(t2)
        delta = t1 - t2
        sec = delta.total_seconds()
        if abs(sec) < 1800:
            return abort(400, description="This time period is already book out, please selete another time")

    booking = Booking()
    booking.date = booking_fields["date"]
    booking.time = booking_fields["time"]
    if "status" in booking_fields:
        booking.status = booking_fields["status"]
    booking.user_id = user.id
    booking.dentist_id = id
    db.session.add(booking)
    db.session.commit()

    return jsonify(booking_schema.dump(booking))


@dentist.put("/<int:id>/close")
@jwt_required()
def close_booking(id):
    dentist_name = get_jwt_identity()
    dentist = Dentist.query.filter_by(username=dentist_name).first()
    if not dentist:
        return abort(400, description="Invalid dentist account")
    
    booking = Booking.query.filter_by(id=id).first()
    if not booking:
        return abort(400, description="booking not exist")
    if booking.dentist_id != dentist.id:
        return abort(400, description="That's not your patient")
    

    booking.status = "Close"

    db.session.add(booking)
    db.session.commit()

    return jsonify(booking_schema.dump(booking))


@dentist.post("/<int:id>/add")
@jwt_required()
def add_treatment(id):
    dentist_name = get_jwt_identity()
    dentist = Dentist.query.filter_by(username=dentist_name).first()
    if not dentist:
        return abort(400, description="Invalid dentist account")
    
    booking = Booking.query.filter_by(id=id).first()
    if not booking:
        return abort(400, description="booking not exist")
    if booking.dentist_id != dentist.id:
        return abort(400, description="That's not your patient")
    if booking.status != "Close":
        return abort(400, description="You have to close this booking to add treatment details.")
    
    treatment_fields = treatment_schema.load(request.json)
    
    treatment = Treatment()
    treatment.service = treatment_fields["service"]
    treatment.fee = treatment_fields["fee"]
    treatment.booking_id = id

    db.session.add(treatment)
    db.session.commit()

    return jsonify(treatment_schema.dump(treatment))


@dentist.delete("/<int:booking_id>/<int:treatment_id>/delete")
@jwt_required()
def delete_treatment(booking_id, treatment_id):
    dentist_name = get_jwt_identity()
    dentist = Dentist.query.filter_by(username=dentist_name).first()
    if not dentist:
        return abort(400, description="Invalid dentist account")
    
    booking = Booking.query.filter_by(id=booking_id).first()
    if not booking:
        return abort(400, description="booking not exist")
    if booking.dentist_id != dentist.id:
        return abort(400, description="That's not your patient")
    
    
    treatment = Treatment.query.filter_by(id=treatment_id).first()
    if not treatment:
        return abort(400, description="This treatment is not exist")

    db.session.delete(treatment)
    db.session.commit()

    return jsonify(treatment_schema.dump(treatment))