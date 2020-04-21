# -*- coding: utf-8 -*-


def test(string):
    """最长回文字符串"""
    start = 0
    max_num = 0
    data_map = {}
    for i in range(0, len(string)):
        if string[i] in data_map:
            lastI = data_map[string[i]]
            if lastI > start:
                start = lastI + 1
        if i - start + 1 > max_num:
            max_num = i - start + 1
        data_map[string[i]] = i
    print(max_num)


test('abcdbaccdaac')


def test1(string):
    """
    动态规划
    note: 梅花走桩题，主要走不同的桩开始走，有几步走到最高
    """
    # 初始化定义一个数组
    dp = [1] * len(string)
    # 记录最大的桩数
    ret = 0
    for j in range(len(string)):
        for i in range(j):
            if string[j] > string[i]:
                # 记录当前桩能走到的最大步数
                dp[j] = max(dp[j], dp[i] + 1)
        # 每走一个桩记录一下最大值
        ret = max(ret, dp[j])
    return ret


print(test1('251545'))


def skip(num):
    """
    青蛙上台阶问题 一次上一个台阶和两个台阶
    params: num 台阶的数 int型
    """
    if num == 0:
        return 0
    if num == 1:
        return 1
    if num == 2:
        return 2
    dp = [0] * (num + 1)
    dp[0], dp[1], dp[2] = 0, 1, 2
    for i in range(3, num+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[num]


print(skip(4))


def uniquePath(m, n):
    """
    数组走左往右走最多多少种走法
    params: m 横坐标, n 纵坐标
    """
    if m <= 0 or n <= 0:
        return 0
    dp = [[0]*m for i in range(n)]
    for i in range(n):
        dp[i][0] = 1
    for i in range(m):
        dp[0][i] = 1
    # j 横坐标, i 纵坐标
    for j in range(1, m):
        for i in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[n-1][m-1]


print(uniquePath(2, 2))


def minPath(arr):
    """
    [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    求最小路径和
    """
    # m 表示横排多少, n 表示竖排
    m = len(arr)
    n = len(arr[0])
    for i in range(1, m):
        arr[i][0] = arr[i][0] + arr[i-1][0]
    for i in range(1, n):
        arr[0][i] = arr[0][i] + arr[0][i-1]
    for i in range(1, m):
        for j in range(1, n):
            arr[i][j] = min(arr[i-1][j], arr[i][j-1]) + arr[i][j]
    return arr[m-1][n-1]


print(minPath([
        [1,1,3],
        [4,1,6],
        [7,1,1]]
))


def wordMinChange(word1, word2):
    """
    a = 'word'
    b = 'wordx'
    b 单词最少多少次操作可以得到a
    params: word1, word2 都是字符串
    考虑到 word1或者word2 为空的时候
    """
    m = len(word1)
    n = len(word2)
    dp = [[0]*(m + 1) for i in range(n + 1)]
    for i in range(1, m+1):
        dp[0][i] = dp[0][i-1] + 1
    for j in range(1, n+1):
        dp[j][0] = dp[j-1][0] + 1
    for j in range(1, m+1):
        for i in range(1, n+1):
            # 单词的具体字符在数据下标减1
            if word1[j-1] == word2[i-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1
    return dp[n][m]


print(wordMinChange('word', 'werd123'))


def func(amount, coins):
    """
    最小次硬币的选择
    params: amount 硬币金额
            coins 硬币种类
    """
    if amount == 0:
        return 0
    if amount < 0:
        return -1
    result = 2**32
    for i in range(len(coins)):
        submin = func(amount - coins[i], coins)
        if submin == -1:
            continue
        result = min(submin+1, result)
    if result == 2**32:
        return -1
    return result


a = func(13, [1, 2, 5, 7])
print(a)

def Beibao():
    pass

