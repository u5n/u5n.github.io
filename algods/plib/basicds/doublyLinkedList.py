"""
test at @luogu#P7912 
    https://www.luogu.com.cn/record/66813662
        ctor
        popleft
        append
        extend
        

"""
from typing import Iterable

class ListNode:
    __slots__ = 'val','next','prev'
    def __init__(self, val=None, prev=None, next=None):
        self.val,self.next,self.prev = val,next,prev
    def __str__(self): return f'DListNode({self.val})'
    def asHead(self):
        """ transfrom linkedlist start from `self` to list, """
        ret = []
        cur = self
        while cur:
            ret.append(cur.val)
            cur=cur.next
        return ret[:-1] # no sentail

# senhead <-> L[0] <-> L[1] <-> ... L[n-1] <-> sentail
# senhead -> ( <-> L[0] <-> L[1] <-> ... L[n-1] <-> L[0] <->) <- sentail
class LinkedList:
    """ there won't be any cycle 
    """
    __slots__ = 'senhead', 'sentail', 'sz'
    def __init__(self, A:Iterable = None):
        self.senhead = ListNode("senhead") # L[-1]
        self.sentail = ListNode("sentail") # L[n]
        self.senhead.next = self.sentail
        self.sentail.prev = self.senhead
        self.sz = 0
        if A: self.extend(A)

    def begin(self): return self.senhead.next
    def end(self): return self.sentail
    # queue like function
    def append(self, val): self.insert_between(self.sentail.prev, self.sentail, val)
    def appendleft(self, val): self.insert_between(self.senhead, self.senhead.next, val)
    def pop(self): 
        tormv = self.sentail.prev
        self.erase(tormv)
        return tormv.val
    def popleft(self): 
        tormv = self.senhead.next 
        self.erase(tormv)
        return tormv.val

    def insert_before(self, node, val):
        if node is self.senhead: raise IndexError("insert before senhead")
        self.insert_between(node.prev, node, val)
    
    def insert_after(self, node, val):
        if node is self.sentail: raise IndexError("insert after sentail")
        self.insert_between(node, node.next, val)

    def insert_between(self, prv, nxt, val):
        new = ListNode(val, prev=prv, next= nxt)
        prv.next = new
        nxt.prev = new
        self.sz+=1
    
    def erase(self, node):
        """ remove a ListNode from its LinkedList
        not sure if it's in `self`
        """
        if self.sz==0: raise IndexError("erase from empty list")
        prv, nxt = node.prev, node.next
        prv.next = nxt
        nxt.prev = prv
        self.sz -= 1

    def index(self, i):
        """ get ListNode by rank
        `i=-1` return `senhead`, `i=n` return `sentail` """
        if i<0 or i>=self.sz:
            if i==-1: return self.senhead
            elif i==self.sz: return self.sentail
            else: raise IndexError
        
        if i<=self.sz-1-i:
            cur = self.senhead.next
            for _ in range(i):
                cur=cur.next
        else:
            cur = self.sentail.prev
            for _ in range(self.sz-1-i):
                cur=cur.prev
        return cur
    def extend(self, iterable):
        if isinstance(iterable, LinkedList):
            lastnode = self.sentail.prev
            lastnode.next = iterable.senhead.next
            iterable.senhead.prev = lastnode
            self.sentail = iterable.sentail
            self.sz += iterable.sz
        else:
            for v in iterable:
                self.insert_after(self.sentail.prev, v)
    def __getitem__(self, i): return self.index(i).val
    def __len__(self): return self.sz
    def __str__(self): return f"LL{list(node.val for node in self)}"
    def __iter__(self):
        cur = self.senhead.next
        for _ in range(self.sz):
            yield cur
            cur = cur.next

def cyclic_dlinkedlist_tolist(head, gonext=True):
    """ assume it's cyclic
        direction: "clockwise
    """
    cur = head
    ret = []
    while cur:
        ret.append(cur.val)
        cur = cur.next if gonext else cur.prev
        if cur is head: break
    return ret


if __name__ == "__main__":
    L = LinkedList([[1,2], 3,4])
    L[0][0] += 10
    print(L.pop())
    print(L)
