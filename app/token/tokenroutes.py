from flask import request
from . import token
from app import db, jwt

@token.route("/")
def index():
    return "Success"