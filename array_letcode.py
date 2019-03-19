# -*- coding: utf-8 -*-


array = [
    [6,5,4],
    [5,4,3],
    [3,2,1]
]


def test(a, array):
    if array is None or len(array) == 0 or len(array[0]) == 0:
        return False
    rows = len(array)
    cloumns = len(array[0])
    if a > array[0][0] or a < array[rows-1][cloumns-1] < a:
        return False
    row = 0
    cloumn =cloumns-1
    while 0<= row < rows and 0<= cloumn:
        if array[row][cloumn] == a:
            return True
        elif array[row][cloumn] > a:
            row += 1
        elif array[row][cloumn] < a:
            cloumn -= 1
    return False

print(test(2, array))
