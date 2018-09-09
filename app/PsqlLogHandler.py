import logging.handlers

from app import psqldb
from app.models import Log


class PsqlLogHandler(logging.Handler):
    """
    Logging handler for PostgreSQL.

    """

    # A very basic logger that commits a LogRecord to the PSQL Db
    def emit(self, record):
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            msg=record.__dict__['msg'], )
        psqldb.session.add(log)
        psqldb.session.commit()
