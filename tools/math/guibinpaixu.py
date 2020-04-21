# -*- coding: utf-8 -*-

#  单链表排序，要求时间复杂度O(nlogn), 空间复杂度O(1)
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def sortList(self, head):
        if head is None:
            return head
        return self.mergeSort(head)

    def mergeSort(self, head):
        if head.next is None:
            return head
        slow = head  # 慢指针
        fast = head  # 快指针
        pre = None
        while fast is not None and fast.next is not None:
            pre = slow
            slow = slow.next
            fast = fast.next.next
        pre.next = None
        l = self.mergeSort(head)
        r = self.mergeSort(slow)
        return self.merge(l, r)

    def merge(self, l, r):
        dummyhead = ListNode(0)
        node = dummyhead
        while l is not None and r is not None:
            if l.val <= r.val:
                node.next = l
                l = l.next
            else:
                node.next = r
                r = r.next
            node = node.next
        if l is not None:
            node.next = l
        if r is not None:
            node.next = r
        return dummyhead.next


a = ListNode(4)
a.next = ListNode(1)
a.next.next = ListNode(2)
a.next.next.next = ListNode(3)

'''
test = Solution()
b = test.sortList(a)
while b:
    print(b.val)
    b = b.next
'''
