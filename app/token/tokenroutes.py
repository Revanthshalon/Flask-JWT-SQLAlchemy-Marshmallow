from flask import request, jsonify
from . import token
from app import db, jwt
from sqlalchemy import exc
from app.models.UserModel import UserSchema, User
from app.models.RevokedToken import RevokedToken
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_refresh_token_required,get_jwt_identity, jwt_required, get_raw_jwt

us = UserSchema() # Importing User Schema to convert the data 


# Loading JWT user claims
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    resp = {
        'role': user['user_role'],
        'id': user['userid'],
    }
    return resp

# Loadind the jwt identity value
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['username']

# Checking if the token in blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    rt = RevokedToken.query.filter_by(jti=jti).first()
    return bool(rt)


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
        db.session.add(user)
        db.session.commit()

        resp = jsonify({"message": "User Registered Successfully"})
        return resp, 201

    except exc.IntegrityError:
        db.session.rollback()
        resp = jsonify({"message": "Database Error"})
        return resp, 409


@token.route('/login', methods=['POST'])
def login():
    
    user = User.query.filter_by(email= request.form['email']).first()

    if user is not None and user.verify_password(request.form['password']) and user.user_role==1:
        user = us.dump(user)
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        resp = jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
        })
        return resp, 200
    else:
        resp = jsonify({
            "message": "Wrong Email or Password"
        })
        return resp, 401


@token.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    resp = jsonify({
        'access_token': create_access_token(identity=current_user)
    })
    return resp, 200


@token.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()
    try:
        rt = RevokedToken(jti)
        db.session.add(rt)
        db.commit()
        resp = jsonify({
            'message':"succesfully logged out"
        })
        return resp, 200
    except exc.IntegrityError:
        resp = jsonify({
            'message': 'Database Error'
        })
        return resp, 409

@token.route('/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()
    try:
        rt = RevokedToken(jti)
        db.session.add(rt)
        db.commit()
        resp = jsonify({
            'message':"succesfully logged out"
        })
        return resp, 200
    except exc.IntegrityError:
        resp = jsonify({
            'message': 'Database Error'
        })
        return resp, 409
