from flask import jsonify, Blueprint, request, abort
from main import db
from models.users import User
from schema.user_schema import user_schema, users_schema
from main import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.bookings import Booking
from schema.booking_schema import booking_schema, bookings_schema
from models.treatments import Treatment
from schema.treatment_schema import treatment_schema, treatments_schema

from controller.auth_controller import admin_authentication
from controller.auth_controller import user_authentication


patient = Blueprint('patient', __name__, url_prefix='/patient')

#User(Admin/Patient) can get their own personal info with the booking records
@patient.get("/info")
@jwt_required()
@user_authentication
def patient_info(user):

    result = user_schema.dump(user)
    return jsonify(result)


#User can cancel the booking if the status is "Open"
@patient.delete("/cancel")
@jwt_required()
@user_authentication
def cancel_booking(user):
   
    booking = Booking.query.filter_by(user_id=user.id, status="Open").first()
    if not booking:
        return abort(404, description="There is no open booking in the system")
    db.session.delete(booking)
    db.session.commit()

    return jsonify(user_schema.dump(user))
    

#Admin can check all the booking details.
@patient.get("/bookings")
@jwt_required()
@admin_authentication
def bookings():
 
    bookings = Booking.query.all()

    return jsonify(bookings_schema.dump(bookings))



#each user can update their own personal info
@patient.put("/update")
@jwt_required()
@user_authentication
def update_info(user):
  
    # update info only based on what's in the json file, could be one or many arributes
    try:
        user_fields = user_schema.load(request.json)

        if "f_name" in user_fields:
            user.f_name = user_fields["f_name"]
        if "l_name" in user_fields:
            user.l_name = user_fields["l_name"]
        if "mobile" in user_fields:
            user.mobile = user_fields["mobile"]
        
        db.session.commit()
        return jsonify(user_schema.dump(user))
    #return an error if anything wrong with the json file
    except:
        return jsonify({"message": "You can only update your f_name, l_name or mobile"})
    


#User can get one of their booking total fees
@patient.get("/<int:id>/fees")
@jwt_required()
@user_authentication
def treatment_fee(user,id):
    #check if the booking exist or not, belongs to this user or not.
    booking = Booking.query.filter_by(id=id).first()
    if not booking:
        return abort(404, description="Booking is not exist")
    if booking.user_id != user.id:
        return abort(403, description="this booking is not yours")

    # use for loop to get all fees under single booking and add them together
    total_amount = 0
    for x in booking.treatment:
        total_amount += x.fee
    
    return jsonify({"Booking ID: ": booking.id, "Total amount:": total_amount})

