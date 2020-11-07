from app import ma, db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    # Defining the table name 
    __tablename__ = "users"

    # Defining the table structure
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.SmallInteger, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    

    @property
    def password(self):
        raise AttributeError("Cannot read the password")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    userid = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    user_role = ma.auto_field()
