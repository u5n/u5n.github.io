# template for some tricky interviewer problem
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __repr__(self):
        return str(self.val)
    def tolistAsHead(self):
        ret = []
        cur = self
        while cur!=None:
            ret.append(cur.val)
            cur = cur.next
        return ret

def toLinkedlist(A):
    sen = ListNode()
    cur = sen
    for e in A:
        cur.next = ListNode(e)
        cur = cur.next
    return sen.next

"""
TOC
    reverse
    getMedium
    size
    merge two sorted list
    remove
"""

def reverse(pre, end=None):
    """ reverse linkedlist begin at pre.next, end before end """
    head = pre.next
    while head.next!=end:
        tomove = head.next
        nxttomoved = tomove.next
        tomove.next = pre.next
        pre.next = tomove
        head.next = nxttomoved

# pre -> sta -> sta2 -> ... -> last -> end
# pre -> sta
# pre -> sta2 -> sta
def getMedium(sta, end=None,left=True):
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

def mergeTwoLists(l1: ListNode, l2: ListNode):
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

head = toLinkedlist([1])
# print(getMedium(head))
pre=ListNode(0,head)
reverse(pre)
print(pre.next.tolistAsHead())
# print(isPalindrome(head))