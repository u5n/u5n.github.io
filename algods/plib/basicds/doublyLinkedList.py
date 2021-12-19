from typing import Iterable


class ListNode:
    __slots__ = 'val','next','prev'
    def __init__(self, val=None, prev=None, next=None):
        self.val,self.next,self.prev = val,next,prev
    def __str__(self): return f'DListNode({self.val})'
    def asHead(self):
        ret = []
        cur = self
        while cur:
            ret.append(cur.val)
            cur=cur.next
        return ret[:-1] # no sentail

# senhead <-> L[0] <-> L[1] <-> ... L[n-1] <-> sentail
# senhead -> ( <-> L[0] <-> L[1] <-> ... L[n-1] <-> L[0] <->) <- sentail
class DoublyLinkedList:
    """ there won't be any cycle """
    def __init__(self, A:Iterable):
        self.senhead = ListNode("senhead") # L[-1]
        self.sentail = ListNode("sentail") # L[n]
        self.senhead.next = self.sentail
        self.sentail.prev = self.senhead
        self.sz = 0
        if A: 
            for e in A: self.append(e)

    def begin(self): return self.senhead.next
    def end(self): return self.sentail
    def append(self, val): self.insert_after(self.sentail.prev, val)
    def appendleft(self, val): self.insert_before(self.senhead.next, val)
    def popleft(self): return self.erase(self.senhead.next).val
    def pop(self): return self.erase(self.sentail.prev).val

    def insert_before(self, iter, val):
        if iter is self.senhead: raise IndexError("insert before senhead")
        self.insert_between(iter.prev, iter, val)
    
    def insert_after(self, iter, val):
        if iter is self.sentail: raise IndexError("insert after sentail")
        self.insert_between(iter, iter.next, val)

    def insert_between(self, prv, nxt, val):
        new = ListNode(val, prev=prv, next= nxt)
        prv.next = new
        nxt.prev = new
        self.sz+=1
    def pop(self, i):
        """ remove a ListNode by its rank """
        if self.i<0 or self.i>=self.sz: raise IndexError(f"can't pop with rank {i}")
        self.erase(self.index(i))
    def erase(self, iter):
        """ remove a ListNode from its LinkedList
        not sure if it's in `self`
        """
        if self.sz==0: raise IndexError("erase from empty list")
        prv, nxt = iter.prev, iter.next
        prv.next = nxt
        nxt.prev = prv
        self.sz -= 1

    def index(self, i):
        """ `i=-1` return `senhead`, `i=n` return `sentail` """
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

    def __len__(self): return self.sz
    def __str__(self): return f"LL({list(self)})"
    def __iter__(self):
        cur = self.senhead.next
        for _ in range(self.sz):
            yield cur
            cur = cur.next

if __name__ == "__main__":
    L = DoublyLinkedList([1,2,3])
    print(L)