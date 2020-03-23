# -*- coding: utf-8 -*-


def Bubble(arr):
    """冒泡排序"""
    for i in range(len(arr)):
        for j in range(0, len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]


arr = [10, 121, 5, 6, 9, 3, 2]
Bubble(arr)
print(arr)


def insertSort(arr):
    """快速排序"""
    for i in range(len(arr)):
        for j in range(i, 0, -1):
            # 最后一个数字肯定最大
            if arr[j] < arr[j-1]:
                arr[j-1], arr[j] = arr[j], arr[j-1]


arr = [1, 2, 3, 123, 123, 234, 23434, 345, 45, 234435, 566]
insertSort(arr)
print(arr)


def selectionSort(arr):
    """选择排序"""
    length = len(arr)
    for i in range(length):
        #  选择最小索引
        min_index = i
        for j in range(i, length):
            if arr[j] < arr[min_index]:
                min_index = j
        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]


arr = [1, 2, 3, 123, 234, 23434, 345, 45, 234435, 566]
selectionSort(arr)
print(arr)
