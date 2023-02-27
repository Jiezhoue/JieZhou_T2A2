from flask import Blueprint, jsonify, request, abort



home = Blueprint('home', __name__, url_prefix="/home")

@home.get("/")
def home_page():
  return jsonify({"message" : "Welcome to Dental System!"})