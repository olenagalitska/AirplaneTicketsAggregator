from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel

from arango import ArangoClient

import logging.config
import yaml

from app.conf.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize PostgreSql database
psqldb = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

# logging initialization (should be after psqldb init and login init, because they are used by logger)
with open('app/conf/logging.yml', 'r') as stream:
    logging_config = yaml.load(stream)
logging.config.dictConfig(logging_config)

# create logger
logger = logging.getLogger('logger')

logger.info('logger started')
logger.info('psqldb has already started (before logger)')
logger.info('login_manager has already started (before logger)')

try:
    logger.info('try to init Migrate(app, psql)')
    migrate = Migrate(app, psqldb)
    logger.info('succeeded')

    # example of using logger
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')

    # example of using logger with exceptions
    # try:
    #     open('/path/to/does/not/exist', 'rb')
    # except (SystemExit, KeyboardInterrupt):
    #     raise
    # except Exception as e:
    #     logger.error('Failed to open file', exc_info=True)

    logger.info('try to init Mail()')
    mail = Mail(app)
    logger.info('succeeded')

    logger.info('try to init Babel()')
    babel = Babel(app)
    logger.info('succeeded')

    # python-arango

    # Initialize the client for ArangoDB.
    logger.info('try to init ArangoClient(...)')
    arangodb_client = ArangoClient(protocol='http', host='localhost', port=8529)
    logger.info('succeeded')

    logger.info('try to connect to arango _system')
    sys_db = arangodb_client.db('_system', username='root', password='')
    logger.info('succeeded')

    if not sys_db.has_database('whatafly'):
        logger.info('_system does not have whatafly db. try to create it')
        sys_db.create_database('whatafly')
        logger.info('succeeded')

    logger.info('try to connect to whatafly')
    arangodb = arangodb_client.db('whatafly', username='arango_user', password='mkh8JTbE793kNtXr')
    logger.info('succeeded')

    logger.info('try to get airlines_data collection from whatafly')
    airlines_data_collection = arangodb.collection('airlines_data')
    logger.info('succeeded')
    # history_collection = arangodb.collection('history')
    # user_activity_collectino = arangodb.collection('user_activity')
    # saved_flights_collection = arangodb.collection('saved_flights')

    list_of_airlines = []

    cursor_list_of_airlines = airlines_data_collection.keys()

    for airline in cursor_list_of_airlines:
        list_of_airlines.append(airline)

    logger.info('airlines from arango: ' + str(list_of_airlines))

    logger.info('try to import and init search Handler()')
    from app.airlines.handler import Handler
    search_handler = Handler()
    logger.info('succeeded')

    logger.info('try to import routes')
    # DO NOT REMOVE IT!
    from app import routes
    logger.info('succeeded')

    logger.info('try to import, init and start ThreadStarter()')
    from app.threads.threads_starter import ThreadsStarter
    threads_starter = ThreadsStarter("Updater Starter")
    threads_starter.start()
    logger.info('succeeded')

    logger.info('starting app...')
    if __name__ == '__main__':
        app.run(debug=True)

except Exception as e:
    logger.error('Exception:  ', exc_info=True)
    exit(-4)
