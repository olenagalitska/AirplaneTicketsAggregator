import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gWfMjs2uXjUd7EeG'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://psql_user:cUgjfhjMuVX4Ydvg@localhost:5432/whatafly'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'whatafly2018@gmail.com'
    MAIL_PASSWORD = 'xKygnnDmQRTkKq3h'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
