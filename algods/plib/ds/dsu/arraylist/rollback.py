# represent a operation that unite set of representative l into set of representative r
from collections import namedtuple, defaultdict
Dsu_operation = namedtuple("Dsu_operation", "l r sz_r")

class Dsu_rollback:
    """
    Dsu (implement by list) that support rollback, the path compression is disabled
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
