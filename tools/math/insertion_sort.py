# -*- coding: utf-8 -*-


def insertSort(data):
    for i in range(0, len(data)):
        for j in range(i, 0, -1):
            # 最后一个数据肯定是最大的
            if data[j] < data[j-1]:
                data[j-1], data[j] = data[j], data[j-1]
            else:
                break
    print(data)
    return data


if __name__ == '__main__':
    insertSort([10, 12, 2, 3, 14, 11, 10])
