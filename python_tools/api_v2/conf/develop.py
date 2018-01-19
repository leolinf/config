# -*- coding: utf-8 -*-


class Config:

    PROJECT = "api_v2"

    # 默认mongodb
    MONGO_DATABASE_URI = "mongodb://127.0.0.1/data_market"
    MONGO_DATABASE_NAME = 'data_market'

    CELERY_BROKER_URL = "amqp://root:root@127.0.0.1/api_v2"
    RABBITMQ_NAME = "api_v2"

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = None

    # 记录
    FAIL_PECORED = 0
    SUCCESS_RECORED = 1

    CACHE_REDIS_URL = 'redis://127.0.0.1/11'
    CACHE_KEY_PREFIX = 'api_v2'
    ENABLE_SENTRY = False
