from collections import defaultdict
from dataclasses import dataclass

@dataclass(slots=True)
class Attr:
    sz: int


class Dsu:
    """ the parent relationship is maintain by a hashmap
    """
    __slots__ = 'p', 'repr_attr', 'cnt'
    def __init__(self):
        self.p = {}
        self.repr_attr = {} # repr -> attr of set(default only store size)
        self.cnt = 0

    def make_set(self, i, sz=1):
        """ add a new set (with single element `i`)  into `self` if `i` not in"""
        if i in self.p: return
        self.p[i] = i
        self.repr_attr[i] = Attr(sz)
        self.cnt += 1

    def find(self, u):
        p = self.p
        if p[u] != u: p[u] = self.find(p[u])
        return p[u]

    def unite(self, l, r, bysize=True):
        p, repr_attr = self.p, self.repr_attr
        l, r = self.find(l), self.find(r)
        if l == r: return False
        if bysize and repr_attr[l].sz > repr_attr[r].sz: l, r = r, l
        p[l] = r
        repr_attr[r].sz += repr_attr[l].sz
        # del repr_attr[l]
        self.cnt -= 1
        return True

    def to_sets(self):
        """
        key is resentative
        value is the set
        """
        ret = defaultdict(list)
        for k in self.p:
            ret[self.find(k)].append(k)
        return ret

    def __repr__(self): return str(self.to_sets().items()).replace("dict_items", "Dsu")
