from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_arangodb import ArangoDB
from app.airlines.handler import Handler

app = Flask(__name__)
app.config.from_object(Config)

psqldb = SQLAlchemy(app)

migrate = Migrate(app, psqldb)

login = LoginManager(app)
login.login_view = 'login'

arangodb = ArangoDB(app)

search_handler = Handler()

from app import routes

if __name__ == '__main__':
    app.run(debug=True)
