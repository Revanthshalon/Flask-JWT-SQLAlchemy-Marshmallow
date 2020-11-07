from app import db, ma

class UploadModel(db.Model):

    __tablename__ = "Uploads"

    uploadid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    filename = db.Column(db.String(100), unique=True, index=True, nullable=False)
    filelocation = db.Column(db.String(255),nullable=False)
    