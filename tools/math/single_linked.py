# -*- coding: utf-8 -*-


class ListNode:

    def __init__(self, val):
        self.val = val
        self.next = None


# 初始化链表
head = ListNode(1)
# 将节点指向链表的头
node = head
# 用来排序的链表头
node1 = head

for i in range(2, 5):
    head.next = ListNode(i)
    head = head.next

# 输出链表
while True:
    if node is None:
        break
    print(node.val)
    node = node.next


# 单链表反转
def reverseList(head):
    if head is None or head.next is None:
        return head
    # 递归反转子链表
    newHead = reverseList(head.next)
    # 反正 1,2 节点
    # 通过head.next 获得节点2
    t1 = head.next
    # 让2的节点指向 1
    t1.next = head
    # 节点1 指向空
    head.next = None
    return newHead


def reverseList2(head):
    curr = head
    node = None
    while curr:
        tmpHead = curr.next
        curr.next = node
        node = curr
        curr = tmpHead
    return node


a = reverseList2(node1)
while a:
    print(a.val)
    a = a.next
