# -*- coding: utf-8 -*-

from redis_pusb import RedisHelper


obj = RedisHelper('today')
obj.public("hello_world")
