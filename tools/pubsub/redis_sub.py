# -*- coding: utf-8 -*-

from redis_pusb import RedisHelper


def hehe():
    obj = RedisHelper('today')
    redis_sub = obj.subscribe()
    #while True:
        # listen()函数封装了parse_response()函数
    msg = redis_sub.listen()
    for i in msg:
        if i['type'] == 'message':
            return i['data']

print(hehe())
