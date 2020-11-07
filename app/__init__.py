from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import config as Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    
    app = Flask(__name__, instance_relative_config=True)
    # Initializing the configurations for 
    Config.init_app(app)
    # the pluggable dependancies
    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    from app.models.UserModel import User

    # Importing Blueprints
    from app.token import token
    from app.protected import protected

    # Registring Blueprints
    app.register_blueprint(token, url_prefix="/token")
    app.register_blueprint(protected, url_prefix='/protected')

    return app