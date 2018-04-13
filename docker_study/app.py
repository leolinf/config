# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig

logging_config = dict(
    version = 1,
    formatters = {
        'f': {
                'format':'%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
            }
        },
    handlers = {
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': 'DEBUG'
            },
        'f': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'log/2.app.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'f'
            }
        },
    root = {
        'handlers': ['f', 'h'],
        'level': logging.DEBUG,
        'propagate': True
        },
)
# 方式1
dictConfig(logging_config)
logger = logging.getLogger()

from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


Session = sessionmaker(autoflush=False)


@contextmanager
def session_scope(session=None):
    """Provide a transactional scope around a series of operations."""
    if not session:
        session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise

    try:
        session.close()
    except:
        session.remove()


class MarkValueSort(Resource):

    def get(self):

        session = scoped_session(Session)
        logger.info('session id = %s', str(id(session)))
        sql = 'SELECT id, name FROM jinse_sort where id=250'
        result = session.execute(sql).fetchall()
        session.close()
        _list = [dict(i) for i in result]
        logger.info('result : %s', _list)
        return _list


def create_app():
    app = Flask(__name__)
    api = Api(app)
    engine = create_engine('mysql+mysqlconnector://root:123456@172.16.4.218:3306/weibit_spider', pool_size=2, max_overflow=0, pool_recycle=50)
    Session.configure(bind=engine)
    api.add_resource(MarkValueSort, '/')
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
