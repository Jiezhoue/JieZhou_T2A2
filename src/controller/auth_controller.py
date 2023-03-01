from flask import jsonify, Blueprint, request, abort
from main import db
from models.users import User
from schema.user_schema import user_schema, users_schema
from main import bcrypt
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.get("/users")
def get_user():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

@auth.post("/login")
def user_login():
    try:
        user_field = user_schema.load(request.json)
        user = User.query.filter_by(username=user_field["username"]).first()
        if not user:
            return abort(401, description="username is not exist")
        elif not bcrypt.check_password_hash(user.password, user_field["password"]):
            return abort(401, description="password is not right")
        access_token = create_access_token(identity=str(user.username))
        return jsonify({"user": user.username, "token": access_token})
    except ValidationError:
        return abort(401, description="minimun password length is 8")









    

