from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from arango import ArangoClient

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

client = ArangoClient(protocol='http', host='localhost', port=8529)
sys_db = client.db('_system', username='root', password='')
if not sys_db.has_database('whatafly'):
    sys_db.create_database('whatafly')

arangodb = client.db('whatafly', username='root', password='')

from app import routes

if __name__ == '__main__':
    app.run(debug=True)
