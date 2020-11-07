from flask import request, jsonify
import pandas as pd
from . import analytics
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from app.models.UploadModel import UploadModel, UploadModelSchema


@analytics.route("/view/<fileid>", methods=['GET'])
@jwt_required
def viewdf(fileid):
    current_user = get_jwt_identity()
    user_claims = get_jwt_claims()
    uploaded_file = UploadModel.query.filter_by(uploadid = int(fileid)).first()
    ums = UploadModelSchema()
    uploaded_file = ums.dump(uploaded_file)
    df = pd.read_csv(uploaded_file['filelocation'])

    return jsonify(df.head(5).to_dict(orient='records')), 200
    

# @analytics.route("/drop/<colname>", methods=['DELETE'])
# @jwt_required
# def editdf(colname):
    