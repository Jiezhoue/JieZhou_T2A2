from flask import jsonify, Blueprint, request, abort
from main import db
from models.users import User
from schema.user_schema import user_schema, users_schema
from main import bcrypt
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.get("/users")
def get_user():
  users = User.query.all()
  result = users_schema.dump(users)
  return jsonify(result)