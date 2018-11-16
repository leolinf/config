# -*- coding: utf-8 -*-

from rabbitmq import PikaQueue


a = PikaQueue('orders')
a.put('123123')
