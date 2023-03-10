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
from controller.auth_controller import user_authentication
from controller.auth_controller import dentist_authentication
from schema.booking_schema import booking_dentist_schema, bookings_dentist_schema
from controller.user_controller import admin_authentication


dentist = Blueprint('dentist', __name__, url_prefix="/dentists")


#anyone can get all dentists' info
@dentist.get("/")
def get_dentist():
    dentist = Dentist.query.all()
    result = dentists_schema.dump(dentist)

    return jsonify(result)



#Dentist login and return the JWT
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


#Only admin can create the dentist account
@dentist.post("/signup")
@jwt_required()
@admin_authentication
def dentist_signup():

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



#User make a booking with a dentist(id)
#There are couple of logic rules in this booking endpoint
#1. user can't not book twice unless he/she delete the previous one first
#2. the minimum appintment is 30min, therefore user can't make a booking if that dentist is not avaliable within that time slot
@dentist.post("/<int:id>/booking")
@jwt_required()
@user_authentication
def make_appointment(user,id):
  
    booking_fields = booking_schema.load(request.json)
    dentist = Dentist.query.filter_by(id=id).first()
    #check if the dentist is exist or not
    if not dentist:
        return abort(400, description="dentist not exist")
    
    #if user already has a booking with "Open" status in the system, he/she can not book again unless delete that one first
    exist = Booking.query.filter_by(user_id=user.id, status="Open").first()
    if exist:
        return abort(400, description="You already have a open booking in the system. Before booking a new one, please ensure to cancel any existing booking in the system.")


    data = Booking.query.filter_by(dentist_id=id, date=booking_fields["date"])
    #check the booking date, if it exists, then check the time
    if data:
        #check each booked time in system with the json "time", if it's less than 30min, this time is not available
        for book in data:
            t1 = datetime.strptime(str(book.time), '%H:%M:%S')
            print(t1)
            t2 = datetime.strptime(booking_fields["time"], '%H:%M:%S')
            print(t2)
            #check the difference between those two time. 1800 second equal to 30min
            delta = t1 - t2
            sec = delta.total_seconds()
            if abs(sec) < 1800:
                return abort(400, description="This time period is already book out, please selete another time")

    booking = Booking()
    booking.date = booking_fields["date"]
    booking.time = booking_fields["time"]
    # if "status" in booking_fields:
    #     booking.status = booking_fields["status"]
    booking.user_id = user.id
    booking.dentist_id = id
    db.session.add(booking)
    db.session.commit()

    return jsonify(booking_schema.dump(booking))



#Dentist can change the booking status from "Open" to "Close" when he finished the appointment with that user
#The reason dentist need to update that "status" because when user make a booking, the default status is "Open", that is used to avoid duplicate booking by single user
#Once the appiontment finished, dentist can close that booking and add some treatment under that booking.
@dentist.put("/<int:id>/close")
@jwt_required()
@dentist_authentication
def close_booking(dentist,id):
  
    booking = Booking.query.filter_by(id=id).first()
    if not booking:
        return abort(400, description="booking not exist")
    if booking.dentist_id != dentist.id:
        return abort(400, description="That's not your patient")
    if booking.status == "Close":
        return abort(400, description="This booking is already closed!")

    booking.status = "Close"

    db.session.add(booking)
    db.session.commit()

    return jsonify(booking_schema.dump(booking))



#Dentist add some treatment under a booking which is belongs to him
#Dentist can only add treatment after he/she change booking status from "Open" to "Close"
@dentist.post("/<int:id>/add")
@jwt_required()
@dentist_authentication
def add_treatment(dentist, id):
 
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



#Dentist can delete a treatment which he/she added under a booking which is belong to him
@dentist.delete("/<int:booking_id>/<int:treatment_id>/delete")
@jwt_required()
@dentist_authentication
def delete_treatment(dentist, booking_id, treatment_id):
 
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



#Dentist can update a treatment which he/she added under a booking which is belong to him
@dentist.put("/<int:booking_id>/<int:treatment_id>/update")
@jwt_required()
@dentist_authentication
def update_treatment(dentist,booking_id, treatment_id):
 
    booking = Booking.query.filter_by(id=booking_id).first()
    if not booking:
        return abort(400, description="booking not exist")
    if booking.dentist_id != dentist.id:
        return abort(400, description="That's not your patient")
    
    
    treatment = Treatment.query.filter_by(id=treatment_id).first()
    if not treatment:
        return abort(400, description="This treatment is not exist")
    
    treatment_fields = treatment_schema.load(request.json)

    if "service" in treatment_fields:
        treatment.service = treatment_fields["service"]
    if "fee" in treatment_fields:
        treatment.fee = treatment_fields["fee"]

    db.session.commit()

    return jsonify(treatment_schema.dump(treatment))



#Anyone can search dentist info based on their speciality
@dentist.get("/search")
def search_dentist():

    dentists = Dentist.query.filter_by(speciality = request.args.get('speciality'))
    return jsonify(dentists_schema.dump(dentists))



#Dentist can check all the bookings under his name
@dentist.get("/bookings")
@jwt_required()
@dentist_authentication
def all_bookings(dentist):
    # dentist_name = get_jwt_identity()
    # dentist = Dentist.query.filter_by(username=dentist_name).first()
    # if not dentist:
    #     return abort(400, description="Invalid dentist account")
    
    bookings = Booking.query.filter_by(dentist_id = dentist.id)
    return jsonify(bookings_dentist_schema.dump(bookings))
    
