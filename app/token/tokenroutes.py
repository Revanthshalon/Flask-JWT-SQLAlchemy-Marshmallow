from flask import request, jsonify
from . import token
from app import db, jwt
from sqlalchemy import exc
from app.models.UserModel import UserSchema, User

us = UserSchema() # Importing User Schema to convert the data 


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return user


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['username']


@token.route("/register", methods=['POST'])
def register():
    
    test = User.query.filter_by(email=request.form['email']).first()

    if test:
        resp = {
            "message": "Email Already Exists"
        }
        return jsonify(resp), 409
try:
    user = User(
        username = request.form['username'],
        email = request.form['email'],
        password = request.form['password'],
        user_role = 1
    )
    db.session.add(User)
    db.session.commit()

    resp = jsonify({"message": "User Registered Successfully"})
    return resp, 201
except exc.IntegrityError:
    db.session.rollback()
    resp = jsonify({"message": "Database Error"})
    return resp, 409