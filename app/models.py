from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return Users.query.get(id)

class Users(db.Model, UserMixin):
    id = db.Column(db.String(265), primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    birth = db.Column(db.Date)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def chech_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)