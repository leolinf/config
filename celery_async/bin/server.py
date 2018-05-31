# -*- coding: utf-8 -*-

import logging
import sys
import os
from logging.config import dictConfig

HOME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(HOME))


logging_config = dict(
    version=1,
    formatters={
        'f': {
            'format': '%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
        }
    },
    handlers={
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.DEBUG
        }
    },
    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)

dictConfig(logging_config)
logger = logging.getLogger()

from bin.tasks import app


def load_tasks():
    logger.info("<<<< loading tasks >>>>")
    from bin.tasks import test


load_tasks()
