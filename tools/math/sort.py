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
    """插入排序"""
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
        # 选择最小索引
        min_index = i
        for j in range(i, length):
            if arr[j] < arr[min_index]:
                min_index = j
        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]


arr = [1, 2, 3, 123, 234, 23434, 345, 45, 234435, 566]
selectionSort(arr)
print(arr)


def mergeSort(arr):
    """归并排序，主要是采用分治法，和递归来处理"""
    if len(arr) < 2:
        return arr
    middle = len(arr) // 2
    left, right = arr[:middle], arr[middle:]

    return merge(mergeSort(left), mergeSort(right))


def merge(left, right):
    result = []
    while left and right:
        if left[0] >= right[0]:
            result.append(right.pop(0))
        else:
            result.append(left.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result


arr = [12, 234, 1, 23, 5, 67, 76, 878]
a = mergeSort(arr)
print(a)


def quickSort(arr, left, right):
    """快速排序"""
    if left >= right:
        return
    low = left
    high = right
    key = arr[low]
    while left < right:
        while left < right and arr[right] > key:
            right -= 1
        arr[left] = arr[right]
        while left < right and arr[left] <= key:
            left += 1
        arr[right] = arr[left]
    arr[right] = key
    quickSort(arr, low, left - 1)
    quickSort(arr, left + 1, high)


arr = [123, 12, 4, 34234, 345, 65, 934, 23]
quickSort(arr, 0, len(arr)-1)
print(arr)
