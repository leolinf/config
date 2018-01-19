# -*- coding: utf-8 -*-

from mongoengine import connect
from flask import Flask, g, redirect, request, url_for
from celery import Celery
from celery.task.schedules import crontab

from .config import Config
from .extensions import sentry, cache, zipkin


celery = Celery(
    __name__,
    broker=Config.CELERY_BROKER_URL,
    include=['task.tasks'],
)


def create_app(config=None):

    app = Flask(
        Config.PROJECT,
    )

    config_app(app, config)
    config_database(app)
    config_extension(app)
    config_blueprints(app)
    config_celery(app)

    return app


def config_app(app, config):

    app.config.from_object(Config)
    if config:
        app.config.from_object(config)


def config_blueprints(app):
    """蓝图注入"""

    from app.test import test

    app.register_blueprint(test)


def config_extension(app):


    cache.init_app(app, config={'CACHE_TYPE': 'redis'})
    zipkin.init_app(app)
    if Config.ENABLE_SENTRY:
        sentry.init_app(app, dsn=Config.SENTRY_DSN)


def config_database(app):

    connect(
        db=app.config['MONGO_DATABASE_NAME'],
        host=app.config['MONGO_DATABASE_URI'],
        connect=False,
    )


def config_celery(app):

    celery.config_from_object(app.config)

    celery.conf.update(
        CELERY_TIMEZONE='Asia/Chongqing',
        CELERYBEAT_SCHEDULE={
            'delete': {
                'task': 'task.tasks.delete_today',
                'schedule': crontab(hour=0, minute=0),
                'options': {
                    'queue': 'delete'
                }
            },
    #        'update_token': {
    #            'task': 'task.tasks.update_token',
    #            'schedule': crontab(minute='*/30'),
    #            'options': {
    #                'queue': 'update_token'
    #            }
    #        },
        },
    )
