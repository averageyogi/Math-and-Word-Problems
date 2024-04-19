from collections import deque
from typing import Optional

# Definition for singly-linked list.
# class LinkedList:
#     def __init__(self, head=None) -> None:
#         self.head = head

# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


def middleNode(self, head):
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


if __name__ == '__main__':
    llist = deque(["a", "b", "c", "d", "e"])
    print(type(llist.head))
    llist