from flask import Flask

from app.airlines_news_updater import AirlinesNewsUpdater
from app.airlines_info_updater import AirlinesInfoUpdater
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from arango import ArangoClient
from app.airlines.handler import Handler

app = Flask(__name__)
app.config.from_object(Config)

psqldb = SQLAlchemy(app)

migrate = Migrate(app, psqldb)

login = LoginManager(app)
login.login_view = 'login'

# python-arango

# Initialize the client for ArangoDB.
arangodb_client = ArangoClient(protocol='http', host='localhost', port=8529)

sys_db = arangodb_client.db('_system', username='root', password='')
if not sys_db.has_database('whatafly'):
    sys_db.create_database('whatafly')

arangodb = arangodb_client.db('whatafly', username='arango_user', password='mkh8JTbE793kNtXr')

airlines_data_collection = arangodb.collection('airlines_data')

list_of_airlines = []

cursor_list_of_airlines = airlines_data_collection.keys()

for airline in cursor_list_of_airlines:
    list_of_airlines.append(airline)

search_handler = Handler()

airlines_news_updater = AirlinesNewsUpdater("Airlines News Updater")
airlines_news_updater.start()

airlines_info_updater = AirlinesInfoUpdater("Airlines Info Updater")
airlines_info_updater.start()

from app import routes

if __name__ == '__main__':
    app.run(debug=True)
