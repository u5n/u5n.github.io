"""
Dsu: Disjoint set inion data structure implement parent relation use dict
this file stores data structure dsu that implement use a parent relationship

both use path compression with unite by size
"""
from collections import defaultdict, namedtuple


class DsuList:
    """ 
    the parent relationship is maintain by a list
    the element is numbered in [0,n)
    """

    def __init__(self, n):
        # make_set 0,1,...,n-1
        # parent relation
        self.p = [i for i in range(n)]
        # size of each resentative
        self.sz = [1] * n
        self.cnt = n

    def find(self, u):
        p = self.p
        if p[u] != u:
            p[u] = self.find(p[u])
        return p[u]

    def unite(self, l, r, bysize=True):
        p, sz = self.p, self.sz
        l, r = self.find(l), self.find(r)
        if l == r: return False
        if bysize and sz[l] > sz[r]: l, r = r, l
        p[l] = r
        sz[r] += sz[l]
        self.cnt -= 1
        return True

    def to_lists(self):
        """
        key is resentative
        value is element in the set
        """
        ret = defaultdict(list)
        for k in range(len(self.p)):
            ret[self.find(k)].append(k)
        return ret

    def __str__(self):
        return str(self.to_lists().items())


class Dsu:
    """ the parent relationship is maintain by a hashmap
    """
    def __init__(self):
        self.p = {}
        self.sz = {}
        self.cnt = 0

    def make_set(self, i, sz=1):
        """ add a new set (with single element `i`)  into `self` if `i` not in"""
        if i in self.p: return
        self.p[i] = i
        self.sz[i] = sz
        self.cnt += 1

    def find(self, u):
        p = self.p
        if p[u] != u: p[u] = self.find(p[u])
        return p[u]

    def unite(self, l, r, bysize=True):
        p, sz = self.p, self.sz
        l, r = self.find(l), self.find(r)
        if l == r: return False
        if bysize and sz[l] > sz[r]: l, r = r, l
        p[l] = r
        sz[r] += sz[l]
        self.cnt -= 1
        return True

    def to_lists(self, withkey=False):
        """
        key is resentative
        value is element in the set
        """
        ret = defaultdict(list)
        for k in self.p:
            ret[self.find(k)].append(k)
        if withkey:
            return ret
        return [e for e in ret.values()]

    def __str__(self):
        return str(self.to_lists().items())


# represent a operation that unite set of representative l into set of representative r
Dsu_operation = namedtuple("Dsu_operation", "l r sz_r")


class DsuList_rollback:
    """
    Dsu that support rollback, the path compression is disabled
    time: without rollback, amortized O(log(n)) per operation
    """

    def __init__(self, n):
        self.p = [i for i in range(n)]
        self.sz = [1] * n
        self.opts = []
        self.cnt = n

    def find(self, u):
        return u if self.p[u] == u else self.find(self.p[u])

    def unite(self, l, r):
        p, sz, opts = self.p, self.sz, self.opts
        l, r = p[l], p[r]
        if l == r: return False
        self.cnt -= 1
        if sz[l] > sz[r]: l, r = r, l
        p[l] = r
        opts.append(Dsu_operation(l, r, sz[r]))
        sz[r] += sz[l]
        return True

    def rollback(self):
        p, sz, opts = self.p, self.sz, self.opts
        last_union = opts.pop()
        self.cnt += 1
        p[last_union.l] = last_union.l
        sz[last_union.r] = last_union.sz_r

    def to_lists(self):
        """
        key is resentative
        value is element in the set
        """
        ret = defaultdict(list)
        for k in range(len(self.p)):
            ret[self.find(k)].append(k)
        return ret

    def __str__(self):
        return str(self.to_lists().items())
