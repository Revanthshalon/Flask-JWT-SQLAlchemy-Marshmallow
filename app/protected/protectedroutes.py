from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from . import protected


@protected.route("/")
@jwt_required
def protectedindex():
    current_user = get_jwt_identity()
    user_claims = get_jwt_claims()
    resp = jsonify({
        'current user':current_user,
        'claims': user_claims,
    })
    return resp, 200