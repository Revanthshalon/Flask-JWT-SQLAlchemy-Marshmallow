import os
from datetime import timedelta

class BaseConfig(object):
    # Common Configurations for all Environments
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(BaseConfig):
    # Production Configurations
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_ALGORITHM = "HS512"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=180)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(BaseConfig):
    # Development Configurations
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///temp.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username@password@localhost:port/databasename' Uncomment this for the using the mysql database
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=180)
    JWT_ALGORITHM = 'HS512'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


app_config = {
    "production": "config.ProductionConfig",
    "development": "config.DevelopmentConfig",
}


def init_app(app):
    config_name = os.environ.get('FLASK_ENV')
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('app.cfg')
