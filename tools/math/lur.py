# -*- coding: utf-8 -*-

from collections import OrderedDict


class LurCache(object):
    """lur缓存算法"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
        else:
            value = -1
        return value

    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
            self.cache[key] = value
        else:
            if len(self.cache) == self.capacity:
                self.cache.popitem(last=False)
                self.cache[key] = value
            else:
                self.cache[key] = value


if __name__ == "__main__":
    lur = LurCache(2)
    print(lur.get(5))
    lur.put(5, 2)
    print(lur.get(5))
    lur.put(3, 1)
    lur.put(2, 1)
    print(lur.get(5))
