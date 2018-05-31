# -*- coding: utf-8 -*-

import logging
import traceback
from celery import Celery
from conf import celeryconfig
from conf.config import SERVER_NAMESPACE

log = logging.getLogger()


class NewCelery(Celery):

    def gen_task_name(self, name, module):
        try:
            module = SERVER_NAMESPACE + module.split('.')[-1]
            return super(NewCelery, self).gen_task_name(name, module)
        except Exception as e:
            log.warn(traceback.format_exc())


app = NewCelery('stats')
app.config_from_object(celeryconfig)
