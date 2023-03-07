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

from controller.auth_controller import admin_authentication
from controller.auth_controller import user_authentication

patient = Blueprint('patient', __name__, url_prefix='/patient')

@patient.get("/info")
@jwt_required()
@user_authentication
def patient_info(user, **kwargs):
    # user_name = get_jwt_identity()
    # user = User.query.filter_by(username=user_name).first()
    # if not user:
    #     return abort(401, description="Invaild user")
    
    result = user_schema.dump(user)
    return jsonify(result)


@patient.delete("/cancel")
@jwt_required()
@user_authentication
def cancel_booking(user, **kwargs):
    # user_name = get_jwt_identity()
    # user = User.query.filter_by(username=user_name).first()
    # if not user:
    #     return abort(401, description="Invaild user")
    
    booking = Booking.query.filter_by(user_id=user.id, status="Open").first()
    if not booking:
        return abort(400, description="no open booking in the system")
    db.session.delete(booking)
    db.session.commit()

    return jsonify(user_schema.dump(user))
    


@patient.get("/treatment")
@jwt_required()
@admin_authentication
def treatment():
    treatment = Treatment.query.all()

    return jsonify(treatments_schema.dump(treatment))



@patient.get("/bookings")
@jwt_required()
@admin_authentication
def bookings():
    # user_username = get_jwt_identity()
    # user = User.query.filter_by(username=user_username).first()
    # if not user:
    #     return abort(400, description="Invalid User")
    
    # if not user.admin:
    #     return abort(400, description="You don't have permission to access system")
    
    bookings = Booking.query.all()

    return jsonify(bookings_schema.dump(bookings))



#each user can update their own personal info
@patient.put("/update")
@jwt_required()
@user_authentication
def update_info(user, **kwargs):
    # user_name = get_jwt_identity()
    # user = User.query.filter_by(username=user_name).first()
    # if not user:
    #     return abort(401, description="Invaild user")
    
    #update info only based on what's in the json file, could be one or many arributes
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
    except:
        return jsonify({"message": "Invalid Input"})
    

