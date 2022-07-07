"""
Dsu: Disjoint set inion data structure implement parent relation use dict
this file stores data structure dsu that implement use a parent relationship

both use path compression with unite by size
"""
from collections import defaultdict


class Dsu:
    """ 
    the parent relationship is maintain by a list A
        of a representative r, `-A[r]` is size of set correspond r
        of a non-representative x, `A[x]` is parent of x
    the element is numbered in [0,n)
    """
    __slots__ = 'p', 'cnt'
    def __init__(self, n):
        # make_set 0,1,...,n-1
        # parent relation
        self.p = [-1]*n
        self.cnt = n

    def find(self, u):
        p = self.p
        if p[u] >= 0:
            p[u] = self.find(p[u])
            return p[u]
        else:
            return u

    def unite(self, l, r, bysize=True):
        p = self.p
        l, r = self.find(l), self.find(r)
        if l == r: return False
        if bysize and p[l] < p[r]: l, r = r, l
        p[r] += p[l]
        p[l] = r
        self.cnt -= 1
        return True

    def to_sets(self):
        """
        key is resentative
        value is the set
        """
        ret = defaultdict(list)
        for k in range(len(self.p)):
            ret[self.find(k)].append(k)
        return ret

    def is_repr(self, u): return self.find(u) < 0
    def __len__(self): return self.cnt
    def __repr__(self): return str(self.to_sets().items()).replace("dict_items", "Dsu")


class DsuChain:
    """
    des:
        use dsu to implement a chain similar to singly linkedlist
        the chain node numbered from 0 to n-1, with a node numbered n as a sentry
        diff with singly linkedlist:
            can't have loop
            linkedlist(chain) node is a set
            can only delete
            delete a node by unite into its next node
            can get node by node number in O(1)
    time:
        the dsu is amortized O(lg(q)), where q number of operations
    """
    def __init__(self, n):
        self.dsu = Dsu(n+1)
        self.n = self.sz = n

    def remove(self, i):
        if not 0<=i<self.n: raise IndexError("remove index error")
        self.dsu.unite(i, self.next(i), bysize=False)
        self.sz -= 1

    def next(self, i): return self.dsu.find(i+1)
    def front(self): return self.dsu.find(0)
    def test(self, i): return self.dsu.is_repr(i)

    def __iter__(self):
        start = self.front()
        while start < self.n:
            yield start
            start = self.next(start)

    def __repr__(self):     
        return f"DsuChain({'->'.join(map(str, self.__iter__()))}, cap={self.n})"

    def __len__(self): return self.sz

class DsuDChain:
    """
    des:
        use dsu to implement a chain similar to doubly linkedlist
        the chain node numbered from 1 to n, with node numbered 0 and n+1 as a sentry
        refer to DsuChain
    time:
        the dsu is amortized O(lg(q)), where q number of operations
    """
    def __init__(self, n):
        self.dsu_r = Dsu(n+2) # use [1,n+1]
        self.dsu_l = Dsu(n+1) # use [0,n]
        self.n = self.sz = n

    def remove(self, i):
        if not 1<=i<=self.n: raise IndexError("remove index error")
        self.dsu_r.unite(i, self.next(i), bysize=False)
        self.dsu_l.unite(i, self.prev(i), bysize=False)
        self.sz -= 1

    def prev(self, i): return self.dsu_l.find(i-1)
    def next(self, i): return self.dsu_r.find(i+1)
    def test(self, i): return self.dsu_l.is_repr(i)
    def front(self): return self.dsu_r.find(1)
    def back(self): return self.dsu_l.find(self.n)

    def __iter__(self):
        start = self.front()
        while start <= self.n:
            yield start
            start = self.next(start)
    
    def __reversed__(self):
        start = self.back()
        while start > 0:
            yield start
            start = self.prev(start)

    def __repr__(self): return f"DsuDChain({' - '.join(map(str, self.__iter__())),}, cap={self.n})"
    def __len__(self): return self.sz