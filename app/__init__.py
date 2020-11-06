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
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Importing Blueprints
    from app.token import token

    # Registring Blueprints
    app.register_blueprint(token, url_prefix="/token")

    return app