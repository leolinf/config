# -*- coding: utf-8 -*-

import logging
import coloredlogs
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG')

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
    engine = create_engine('mysql+mysqlconnector://root:123456@127.0.0.1:3306/weibit_spider', pool_size=2, max_overflow=0, pool_recycle=50)
    Session.configure(bind=engine)
    api.add_resource(MarkValueSort, '/')
    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
