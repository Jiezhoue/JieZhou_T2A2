from flask import jsonify, Blueprint, request, abort
from main import db
from models.users import User
from schema.user_schema import user_schema, users_schema
from main import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity



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








    

