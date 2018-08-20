import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess3836991673406236088747'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://plane:planekvastaras@localhost:5432/flights'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
