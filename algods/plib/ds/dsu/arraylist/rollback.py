# represent a operation that unite set of representative l into set of representative r
from collections import namedtuple, defaultdict
Dsu_operation = namedtuple("Dsu_operation", "l r p_l")

class Dsu_rollback:
    """
    Dsu (implement by list) that support rollback, the path compression is disabled
    time: without rollback, amortized O(log(n)) per operation
    """
    __slots__ = 'p', 'opts', 'cnt'
    def __init__(self, n):
        self.p = [-1]*n
        self.opts = []
        self.cnt = n

    def find(self, u): return u if self.p[u] == u else self.find(self.p[u])

    def unite(self, l, r):
        p, opts = self.p, self.opts
        l, r = self.find(l), self.find(r)
        if l == r: return False
        if p[l] < p[r]: l, r = r, l
        p[r] += p[l]
        opts.append(Dsu_operation(l, r, p[l]))
        p[l] = r
        self.cnt -= 1
        return True

    def rollback(self):
        p, opts = self.p, self.opts
        l, r, p_l = opts.pop()
        p[l] = p_l
        p[r] -= p_l
        self.cnt += 1

    def to_sets(self):
        """
        key is resentative
        value is element in the set
        """
        ret = defaultdict(list)
        for k in range(len(self.p)):
            ret[self.find(k)].append(k)
        return ret
    
    def is_repr(self, u): return self.find(u) < 0
    def __len__(self): return self.cnt
    def __repr__(self): return str(self.to_sets().items()).replace("dict_items", "Dsu")
