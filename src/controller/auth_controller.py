from flask import jsonify, Blueprint, request, abort
from main import db
from models.users import User
from schema.user_schema import user_schema, users_schema
from main import bcrypt
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.get("/users")
@jwt_required()
def get_user():
    user_name = get_jwt_identity()
    user = User.query.filter_by(username=user_name).first()
    if not user:
        return abort(401, description="Invaild user")
    if not user.admin:
        return abort(401, description="Unauthorized User")

    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)



@auth.get("/user/<int:id>")
@jwt_required()
def patient_info(id):
    user_name = get_jwt_identity()
    user = User.query.filter_by(username=user_name).first()
    if not user:
        return abort(401, description="Invaild user")
    if not user.admin:
        return abort(401, description="Unauthorized User")
    
    patient = User.query.filter_by(id=id).first()
    if not patient:
        return abort(401, description="Patient not exist")
    
    result = user_schema.dump(patient)
    return jsonify(result)



@auth.post("/login")
def user_login():
    try:
        user_fields = user_schema.load(request.json)
        user = User.query.filter_by(username=user_fields["username"]).first()
        if not user:
            return abort(401, description="username is not exist")
        elif not bcrypt.check_password_hash(user.password, user_fields["password"]):
            return abort(401, description="password is not right")
        access_token = create_access_token(identity=str(user.username))
        return jsonify({"user": user.username, "token": access_token})
    except ValidationError:
        return abort(401, description="minimun password length is 8")


@auth.post("/signup")
def signup():
    try:
        user_fields = user_schema.load(request.json)
        user = User.query.filter_by(username=user_fields["username"]).first()
        if user:
            return abort(401, description="Username is already registered. Please choose another username.")

        user = User()
        user.f_name = user_fields["f_name"]
        user.l_name = user_fields["l_name"]

        if "mobile" in user_fields:
            user.mobile = user_fields["mobile"]
        user.username = user_fields["username"]
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=str(user.username))
        return jsonify({"user": user.username, "token":access_token})
    except ValidationError:
        return abort(401, description="minimun password length is 8")










    

