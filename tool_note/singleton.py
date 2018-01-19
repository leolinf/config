# -*- coding: utf-8 -*-
from functools import wraps


# #############
#  __new__ 方法实现
# #############

class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class myclass(Singleton):
    a = 1


my = myclass()
print(id(my))
one = myclass()
print(id(one))

# ############
# 装饰器实现
##############


def singleton_new(cls):
    _instance = {}

    @wraps(cls)
    def singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return singleton


@singleton_new
class MyClass(object):
    a = 1


my = MyClass()
one = MyClass()
print(id(one), id(my))


# ###########
# 通过metaclass 实现
# ###########

class SingletonNew(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonNew, cls).__call__(*args, **kwargs)
        return cls._instance[cls]

# python2
class TestClass(object):
    __metaclass__ = SingletonNew
# python3
class Test2Class(metaclass=SingletonNew):
    pass


one = TestClass()
two = TestClass()
print(id(one), id(two))

one = Test2Class()
two = Test2Class()
print(id(one), id(two))
