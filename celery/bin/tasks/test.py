# -*- coding: utf-8 -*-

import time

from bin.tasks import app
from bin.tasks.base import BaseTask

from celery import group
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)



@app.task(name='rd.group.test.add', base=BaseTask, bind=True)
def add(self, x, y):
    logger.info('{} + {}'.format(x, y))
    return x + y


@app.task(base=BaseTask, bind=True)
def get_args(self, *args):
    logger.info('args=%s', args)
    return True
