# -*- coding: utf-8 -*-

from kombu import Queue, Exchange
from celery.schedules import crontab


# Broker 地址
BROKER_URL = 'amqp://admin:123456@192.168.0.5:5672/'
# broker连接池大小，可选，默认为10。可根据worker并发数调整
# BROKER_POOL_LIMIT = 20

# 任务结果存储地址，可选
CELERY_RESULT_BACKEND = 'redis://192.168.0.7:6379/1'
# 任务结果存储的超期时间设置(s)，设置以防止结果堆积。可选
CELERY_TASK_RESULT_EXPIRES = 60 * 60

# 消息序列化格式
CELERY_TASK_SERIALIZER = 'json'
# broker允许接收的消息格式
CELERY_ACCEPT_CONTENT = ['json']
# 启用client调用任务时发送task-sent事件开关,便于监控
CELERY_SEND_TASK_SENT_EVENT = True


# 任务队列声明
# 将任务队列与相应的exchange和相应的routing_key绑定
CELERY_QUEUES = (
    Queue('rd.group.test', exchange=Exchange('rd.group.ex.test', type='direct'), routing_key='test'),
    Queue('rd.group.args', exchange=Exchange('rd.group.ex.args', type='direct'), routing_key='args'),
)

# 任务路由规则
CELERY_ROUTES = ([
    ('rd.group.test.add', {'exchange': 'rd.group.ex.test', 'routing_key': 'test'}),
    ('rd.group.test.get_args', {'exchange': 'rd.group.ex.args', 'routing_key': 'args'}),
],)


# celery 周期任务

# 指定时区, 默认UTC时间
CELERY_TIMEZONE = 'Asia/Chongqing'

 # 目前允许配置两种形式, 否则监控无法识别:
 # 1.每天固定时间点: crontab(hour=12, minute=0)
 # 2.间隔时间点: crontab(hour='*/2', minute=0) 0点开始，每2h执行一次

# 周期任务
CELERYBEAT_SCHEDULE = {
    'test-schedule-add': {
        'task': 'rd.group.test.add',
        #'schedule': crontab(hour='*/1', minute=9),
        'schedule': crontab(),
        'args': (1, 1),
        'options': {'queue': 'rd.group.test', 'routing_key': 'test'}  # 需显式指定
    },
}
