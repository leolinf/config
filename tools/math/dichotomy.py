# -*- coding: utf-8 -*-
import time


def dichotomy(_list, n):
    low = 0
    high = len(_list) - 1

    while low <= high:
        mid = (low + high) / 2
        guess = _list[mid]
        time.sleep(1)
        if guess > n:
            high = mid - 1
            continue
        elif guess < n:
            low = mid + 1
            continue
        elif guess == n:
            return mid
        else:
            return None
    return None


array = [1, 2, 3, 4, 5, 6]
array = []
result = dichotomy(array, 1)
print("result: %s" % result)
