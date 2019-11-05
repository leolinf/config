# -*- coding: utf-8 -*-
# 一个链表，假设第一个节点我们定为下标为1，第二个为2，
# 那么下标为奇数的结点是升序排序，偶数的结点是降序排序，
# 如何让整个链表有序？（分离链表，合并两个有序链表）


class ListNode(object):

    def __init__(self, x):
        self.val = x
        self.next = None


# 初始化链表
head = ListNode(1)
node = head
nums = 10
a = 2
b = 10
while nums > 0:
    if nums % 2 == 1:
        head.next = ListNode(a)
        a += 1
        head = head.next
    else:
        head.next = ListNode(b)
        b -= 1
        head = head.next
    nums -= 1


class Solution(object):

    def twoList(self, node):
        l1 = ListNode(0)
        l1Node = l1
        l2 = None

        count = 1
        while node:
            if count%2 == 1:
                l1.next = node
                l1 = l1.next
                node = node.next
            else:
                temp = node.next  # 记录当前节点的下一个节点的位置
                node.next = l2
                l2 = node
                node = temp
            count += 1

        return self.merget(l1Node.next, l2)

    def merget(self, l1, l2):
        head = ListNode(0)
        first = head
        while l1 is not None and l2 is not None:
            if l1.val < l2.val:
                head.next = l1
                l1 = l1.next
            else:
                head.next = l2
                l2 = l2.next
            head = head.next
        if l1 is None:
            head.next = l2
        if l2 is None:
            head.next = l1
        return first.next


test = Solution()
a = test.twoList(node)
while a:
    print(a.val)
    a = a.next

