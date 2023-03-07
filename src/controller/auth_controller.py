from flask import jsonify, Blueprint, request, abort
from main import db
from models.users import User
from schema.user_schema import user_schema, users_schema
from main import bcrypt
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.dentists import Dentist
from schema.dentist_schema import dentist_schema, dentists_schema
from functools import wraps

auth = Blueprint('auth', __name__, url_prefix='/auth')

def admin_authentication(func):
    @wraps(func)
    def wrapper():
        user_username = get_jwt_identity()
        user = User.query.filter_by(username=user_username).first()
        if not user:
            return abort(400, description="Invalid User")
    
        if not user.admin:
            return abort(400, description="You don't have permission to access system")

        return func()      
    return wrapper

def user_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_username = get_jwt_identity()
        user = User.query.filter_by(username=user_username).first()
        if not user:
            return abort(400, description="Invalid User")

        return func(*args, **kwargs)      
    return wrapper

#Only admin account can retrieve all user's information 
@auth.get("/users")
@jwt_required()
@admin_authentication
def get_user():
    # user_name = get_jwt_identity()
    # user = User.query.filter_by(username=user_name).first()
    # if not user:
    #     return abort(401, description="Invaild user")
    # if not user.admin:
    #     return abort(401, description="Unauthorized User")

    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)


#Admin account can retrieve specific user information based on user ID
@auth.get("/user/<int:id>")
@jwt_required()
@admin_authentication
def patient_info(id):
    # user_name = get_jwt_identity()
    # user = User.query.filter_by(username=user_name).first()
    # if not user:
    #     return abort(401, description="Invaild user")
    # if not user.admin:
    #     return abort(401, description="Unauthorized User")
    
    patient = User.query.filter_by(id=id).first()
    if not patient:
        return abort(401, description="Patient not exist")
    
    result = user_schema.dump(patient)
    return jsonify(result)


#User login the dental system
@auth.post("/login")
def user_login():
    try:
        user_fields = user_schema.load(request.json)
        user = User.query.filter_by(username=user_fields["username"]).first()
        #Verifiy the username and password, let user know which one is not correct.
        if not user:
            return abort(401, description="username is not exist")
        elif not bcrypt.check_password_hash(user.password, user_fields["password"]):
            return abort(401, description="password is not right")
        access_token = create_access_token(identity=str(user.username))
        return jsonify({"user": user.username, "token": access_token})
    except ValidationError:
        return abort(401, description="minimun password length is 8")


#User can register an account
@auth.post("/signup")
def signup():
    try:
        user_fields = user_schema.load(request.json)
        user = User.query.filter_by(username=user_fields["username"]).first()

        #can't have same username in the system, check the duplication
        if user:
            return abort(401, description="Username is already registered. Please choose another username.")

        user = User()
        user.f_name = user_fields["f_name"]
        user.l_name = user_fields["l_name"]

        #Cause the mobile field is not compulsory, will check the user_fields in case it's not there and avoid throw error
        if "mobile" in user_fields:
            user.mobile = user_fields["mobile"]
        user.username = user_fields["username"]
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=str(user.username))
        return jsonify({"user": user.username, "token":access_token})
    #the password length has to be more than 8 digit
    except ValidationError:
        return abort(401, description="minimun password length is 8")


#Admin delete patient's account
@auth.delete("/user/delete/<int:id>")
@jwt_required()
@admin_authentication
def delete_user(id):
    # user_name = get_jwt_identity()
    # user = User.query.filter_by(username=user_name).first()
    # if not user:
    #     return abort(401, description="Invaild user")
    # if not user.admin:
    #     return abort(401, description="Unauthorized user")
    
    patient = User.query.filter_by(id=id).first()
    if not patient:
        return abort(400, description="Can't find that user")
    if patient.admin:
        return abort(400, description="Can't delelte admin account")
    
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"Patient {x} {y}".format(x=patient.f_name, y=patient.l_name): "has been deleted"})


    
#Admin delete dentist's account
@auth.delete("/dentist/delete/<int:id>")
@jwt_required()
@admin_authentication
def delete_dentist(id):
    # user_name = get_jwt_identity()
    # user = User.query.filter_by(username=user_name).first()
    # if not user:
    #     return abort(401, description="Invaild user")
    # if not user.admin:
    #     return abort(401, description="Unauthorized user")
    
    dentist = Dentist.query.filter_by(id=id).first()
    if not dentist:
        return abort(400, description="Can't find that dentist")
    
    db.session.delete(dentist)
    db.session.commit()
    return jsonify({"Dentist {x} {y}".format(x=dentist.f_name, y=dentist.l_name): "has been deleted"})

