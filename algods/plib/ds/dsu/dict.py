from collections import defaultdict
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