from app import db, ma

class UploadModel(db.Model):

    __tablename__ = "uploads"

    uploadid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    filename = db.Column(db.String(100), unique=True, index=True, nullable=False)
    filelocation = db.Column(db.String(255),nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    

class UploadModelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UploadModel

    uploadid = ma.auto_field()
    filename = ma.auto_field()
    filelocation = ma.auto_field()
    upload_date = ma.auto_field()