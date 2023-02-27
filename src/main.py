from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.validate import Length
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


jwt = JWTManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

def create_app():
  app = Flask(__name__)
  app.config.from_object("config.app_config")

  jwt.init_app(app)
  ma.init_app(app)
  bcrypt.init_app(app)
  db.init_app(app)


  from controller import registerable_controllers

  for controller in registerable_controllers:
    app.register_blueprint(controller)

  return app

