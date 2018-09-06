from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from arango import ArangoClient
from app.airlines.handler import Handler
from flask_mail import Mail

# from app.flights_updater import FlightsUpdater

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)


# Initialize PostgreSql database
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
from app import routes
flights_updater = routes.FlightsUpdater("Flights Updater")
flights_updater.start()



if __name__ == '__main__':
    app.run(debug=True)