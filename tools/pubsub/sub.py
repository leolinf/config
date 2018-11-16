# -*- coding: utf-8 -*-


from rabbitmq import PikaQueue

a = PikaQueue('orders')
c = a.get()
print(c)

