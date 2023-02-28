from flask import Blueprint, jsonify, request, abort

from models.dentists import Dentist
from schema.dentist_schema import dentist_schema, dentists_schema

dentist = Blueprint('dentist', __name__, url_prefix="/dentists")

@dentist.get("/")
def get_dentist():
    dentist = Dentist.query.all()
    result = dentists_schema.dump(dentist)

    return jsonify(result)
