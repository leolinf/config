# -*- coding: utf-8 -*-

import logging
import time

from bin.tasks import app
from bin.tasks.base import BaseTask
from celery import group

logger = logging.getLogger()


@app.task(base=BaseTask, bind=True)
def add(self, x, y):
    logger.info('{} + {}'.format(x, y))
    time.sleep(10)
    return x + y


@app.task(base=BaseTask, bind=True)
def adds(self):
    group(add.s(i, i) for i in xrange(10)).delay()
