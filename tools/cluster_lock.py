# -*- coding: utf-8 -*-
import time
import redis


conn = redis.Redis(host='127.0.0.1', port=6379, password="123456", db=1)


class RedisLock(object):
    def __init__(self, key):
        self._lock = 0
        self.lock_key = "%s_dynamic_test" % key

    @staticmethod
    def get_lock(cls, timeout=10):
        while cls._lock != 1:
            now = time.time()
            lock_timeout = now + timeout + 1
            cls._lock = conn.setnx(cls.lock_key, lock_timeout)
            if cls._lock == 1 or (now > float(conn.get(cls.lock_key)) and now > float(conn.getset(cls.lock_key, lock_timeout))):
                print("get lock")
                break
            else:
                time.sleep(0.3)

    @staticmethod
    def release(cls):
        if time.time() < float(conn.get(cls.lock_key).decode()):
            print("release lock")
            conn.delete(cls.lock_key)


def deco(cls):
    def _deco(func):
        def __deco(*args, **kwargs):
            print("before %s called [%s]." % (func.__name__, cls))
            cls.get_lock(cls)
            try:
                return func(*args, **kwargs)
            finally:
                cls.release(cls)
        return __deco
    return _deco


@deco(RedisLock("112233"))
def myfunc():
    print("myfunc() called.")
    time.sleep(5)


if __name__ == "__main__":
    myfunc()
