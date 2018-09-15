import logging.handlers

from app import psqldb
from app.models import Log


class PsqlLogHandler(logging.Handler):
    """
    Logging handler for PostgreSQL.

    """

    # A very basic logger that commits a LogRecord to the PSQL Db
    def emit(self, record):
        msg = str(record.__dict__['msg'])
        if len(record.__dict__['args']) > 0:
            msg += '; args: ' + str(record.__dict__['args'])
        if record.__dict__['exc_info'] is not None:
            msg += str(record.__dict__['exc_info']) + str(record.__dict__['exc_text']) + str(record.__dict__['stack_info'])

        log = Log(
            pathname=record.__dict__['pathname'],
            level=record.__dict__['levelname'],
            func_name=record.__dict__['funcName'],
            line_no=record.__dict__['lineno'],
            msg=msg
        )
        psqldb.session.add(log)
        psqldb.session.commit()
