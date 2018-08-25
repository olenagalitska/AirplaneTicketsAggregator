from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.airlines.handler import Handler


app = Flask(__name__)
app.config.from_object(Config)

psqldb = SQLAlchemy(app)

migrate = Migrate(app, psqldb)

login = LoginManager(app)
login.login_view = 'login'


# python-arango

from arango import ArangoClient

# Initialize the client for ArangoDB.
arango_client = ArangoClient(protocol='http', host='localhost', port=8529)

# Connect to "test" database as root user.
arangodb = arango_client.db('whataflyDB', username='dj', password='passwordTheChosenOne')



# pyArango
#
# from pyArango.connection import *
# arangodb_connection = Connection(username="dj", password="passwordTheChosenOne")
# arangodb = arangodb_connection.databases["whataflyDB"]




# ArangoPy
#
# from arangodb.api import Client
#
# client = Client(hostname='localhost')





search_handler = Handler()

from app import routes

if __name__ == '__main__':
    app.run(debug=True)
