from flask import Flask
from app.updaters.airlines_news_updater import AirlinesNewsUpdater
from app.updaters.airlines_info_updater import AirlinesInfoUpdater
from app.conf.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from arango import ArangoClient
from app.airlines.handler import Handler

from flask_mail import Mail

# from app.flights_updater import FlightsUpdater

import logging.config
import yaml

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


# logging initialization (should be after psqldb init, because it used by logger
with open('app/conf/logging.yml', 'r') as stream:
    logging_config = yaml.load(stream)
logging.config.dictConfig(logging_config)

# create logger
logger = logging.getLogger('logger')

# example of using logger
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')
start_urls = []

print('list of airlines: ')
for airline in list_of_airlines:
    print(airline)
    airline_news = airlines_data_collection.get(airline)
    print('link:')
    link = airline_news.get('news_link')
    print(link)
    print()
    start_urls.append(link)



print('urls:')
for url in start_urls:
    print(url)

airline_data = airlines_data_collection.get(airline)
airline_news_data = airline_data['news']
# self.start_urls.append((airline_news_data['links'])['news_link'])




airline_data = airlines_data_collection.get('uia')

airline_news_data = airline_data['news']

print('airline_news_data: ')
print(airline_news_data)
print()

print('airline_news_data["latest_version"]: ')
print(airline_news_data['latest_version'])
print()

print('airline_news_data["selectors"]: ')
print(airline_news_data['selectors'])
print()


print('news: ')
news = airline_news_data['v.' + str(airline_news_data['latest_version'])]
print(news)
print()

print('links:')
print(airline_data['links'])
print()

search_handler = Handler()

# airlines_news_updater = AirlinesNewsUpdater("Airlines News Updater")
# airlines_news_updater.start()
#
# airlines_info_updater = AirlinesInfoUpdater("Airlines Info Updater")
# airlines_info_updater.start()

from app import routes
# flights_updater = routes.FlightsUpdater("Flights Updater")
# flights_updater.start()



if __name__ == '__main__':
    app.run(debug=True)