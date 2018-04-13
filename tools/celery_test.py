# -*- coding: utf-8 -*-
from celery import Celery
import settings


app = Celery('stats')
app.config_from_object(settings)


@app.task
def hello(x, y):
    print(x+y)
    return x+y
