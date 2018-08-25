from app import psqldb
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


# from app import app
# from flask_sqlalchemy import SQLAlchemy
# psqldb = SQLAlchemy(app)

@login.user_loader
def load_user(id):
    return Users.query.get(id)


class Users(psqldb.Model, UserMixin):
    __tablename__ = 'Users'

    id = psqldb.Column(psqldb.Integer, unique=True, primary_key=True, nullable=False, autoincrement=True)
    username = psqldb.Column(psqldb.String(128), unique=True, nullable=False)
    password = psqldb.Column(psqldb.String(256), nullable=False)
    email = psqldb.Column(psqldb.String(128), unique=True, nullable=False)
    first_name = psqldb.Column(psqldb.String(256), nullable=False)
    last_name = psqldb.Column(psqldb.String(256), nullable=False)

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.email = email  # .lower
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
