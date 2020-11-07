import os 
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from werkzeug.utils import secure_filename
from app.models.UploadModel import UploadModel, UploadModelSchema
from datetime import datetime
from app import db
from . import dashboard
from sqlalchemy import exc

ALLOWED_EXTENSIONS = ['csv']
UPLOADS_FOLDER = "D:/Uploads/"


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@dashboard.route("/upload", methods=['POST'])
@jwt_required
def upload():

    if 'file' not in request.files:
        resp = jsonify({
            "message":"File not in the request"
        })
        return resp, 400
    file = request.files['file']
    current_user = get_jwt_identity()
    user_claims = get_jwt_claims()

    if file and allowed_filename(file.filename):
        if os.path.exists(os.path.join(UPLOADS_FOLDER,current_user)):
            BASE_DIR = os.path.join(UPLOADS_FOLDER, current_user)
            filename = secure_filename(file.filename)
            file.save(os.path.join(BASE_DIR, filename))
            resp = {
                "message": "Upload Success",
                "filename": filename
            }
            resp['current_user'] = current_user
            resp['user_claims'] = user_claims

            uid = UploadModel(userid = user_claims['userid'], filename=filename, filelocation=os.path.join(BASE_DIR, filename), upload_date = datetime.now())
            db.session.add(uid)
            db.session.commit()

            return jsonify(resp), 201

        os.makedirs(os.path.join(UPLOADS_FOLDER,current_user))
        BASE_DIR = os.path.join(UPLOADS_FOLDER, current_user)
        filename = secure_filename(file.filename)
        file.save(os.path.join(BASE_DIR,filename))
        resp = {
            "message": "File Uploaded Successfully",
            "filename": filename
        }
        resp['current_user'] = current_user
        resp['user_claims'] = user_claims

        uid = UploadModel(userid = user_claims['userid'], filename=filename, filelocation=os.path.join(BASE_DIR, filename), upload_date = datetime.now())
        try:
            db.session.add(uid)
            db.session.commit()
        except:
            db.session.rollback()
            resp = {
                "message": "Database Error"
            }
            return jsonify(resp), 409

        return jsonify(resp),200


@dashboard.route("/files", methods=["GET"])
@jwt_required
def uploadedfiles():
    current_user = get_jwt_identity()
    user_claims = get_jwt_claims()
    upload_data = UploadModel.query.filter_by(userid=user_claims['userid']).all()
    ums = UploadModelSchema()
    upload_data = [ums.dump(i) for i in upload_data]
    resp = jsonify(upload_data)
    return resp, 200