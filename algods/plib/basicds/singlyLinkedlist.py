# template for some tricky interview problem
# especially for leetcode problems 
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __str__(self):
        return f'ListNode({self.val})'
    def __iter__(self):
        cur = self
        while cur!=None:
            yield cur.val
            cur = cur.next

def toLinkedlist(A: list):
    sen = ListNode()
    cur = sen
    for e in A:
        cur.next = ListNode(e)
        cur = cur.next
    return sen.next

"""
TOC
    reverse
    reverse_n
    getMedium
    size
    merge two sorted list
    remove
"""

def reverse(pre, end=None):
    """ reverse linkedlist begin at `pre.next`, end before (exclude)`end` """
    head = pre.next
    if head is None: return # reverse empty linkedlist
    while head.next!=end:
        cur = head.next
        nxt = cur.next 

        cur.next = pre.next 
        pre.next = cur
        head.next = nxt

def reverse_n(pre, n):
    """ reverse size `n` linkedlist begin at pre.next
        return #reversed
    """
    head = pre.next
    if head is None: return 0
    for n_rev in range(1, n):
        if head.next == None:
            return n_rev
        cur = head.next # L[head + n_rev]
        nxt = cur.next

        cur.next = pre.next
        pre.next = cur
        head.next = nxt
    return n

def getMedium(sta, end=None, left=True):
    """ 
    if left: return L[(n-1)//2]
    else: return L[n//2] 
    """
    slow = sta
    faster = sta
    while faster!=end and faster.next!=end and faster.next.next!=end:
        slow = slow.next
        faster = faster.next.next
    if not left and faster.next!=end:
        return slow.next
    return slow

def size(sta, end=None):
    ans = 0
    while sta!=end:
        ans+=1
        sta = sta.next
    return ans

def mergeTwoSortedLists(l1: ListNode, l2: ListNode):

    pre = ListNode()
    cur = pre
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = ListNode(l1.val)
            l1=l1.next
        else:
            cur.next = ListNode(l2.val)
            l2=l2.next
        cur = cur.next
    cur.next = l1 or l2
    return pre.next

def remove(prv):
    prv.next = prv.next.next

if __name__ == "__main__":
    head = toLinkedlist([1,2,3,4,5])
    # print(getMedium(head))
    pre=ListNode(0,head)
    reverse_n(pre.next,3)
    print(list(pre.next))
    # print(isPalindrome(head))