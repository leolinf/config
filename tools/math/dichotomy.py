# -*- coding: utf-8 -*-
import time


def dichotomy(_list, n):
    """二分查找 该数字在列表中的位置"""
    low = 0
    high = len(_list) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = _list[mid]
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
result = dichotomy(array, 3.4)
print("result: %s" % result)
