# -*- coding: utf-8 -*-

from celery import Celery

app = Celery('tasks', broker='amqp://admin:123456@192.168.0.5:5672/')

@app.task
def add(x, y):
    return x + y
