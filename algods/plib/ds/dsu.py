"""
Dsu: Disjoint set inion data structure implement parent relation use dict
DsuList: Dsu implement parent relation use arraylist

both use path compression with union by size
"""
from collections import defaultdict

class DsuList:
    """ sets are numbered from `0` to `n-1` """
    def __init__(self, n):
        # make_set 0,1,...,n-1
        # parent relation
        self.p = [i for i in range(n)]
        # size of each representative
        self.sz = [1]*n
        self.cnt = n
    def find(self,u):
        p = self.p
        if p[u]!=u:
            p[u]=self.find(p[u])
        return p[u]
    def union(self,l,r,bysize=True):
        p,sz = self.p, self.sz
        repl,repr = self.find(l), self.find(r)
        if repl==repr: return False
        if bysize and sz[repl]>sz[repr]: repl,repr = repr,repl
        p[repl] = repr
        sz[repr]+=sz[repl]
        self.cnt -= 1
        return True

    def to_lists(self, withkey=False):
        """
        key is representative
        value is element in the set
        """
        ret = defaultdict(list)
        for k in range(len(self.p)):
            ret[self.find(k)].append(k)
        if withkey:
            return ret
        return [e for e in ret.values()]
    def __str__(self):
        return str(self.to_lists())
        
class Dsu:
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
    def find(self,u):
        p = self.p
        if p[u]!=u: p[u]=self.find(p[u])
        return p[u]
    def union(self,l,r,bysize=True):
        p,sz = self.p, self.sz
        repl,repr = self.find(l), self.find(r)
        if repl==repr: return False
        if bysize and sz[repl]>sz[repr]: repl,repr = repr,repl
        p[repl] = repr
        sz[repr]+=sz[repl]
        self.cnt -= 1
        return True
    def to_lists(self, withkey=False):
        """
        key is representative
        value is element in the set
        """
        ret = defaultdict(list)
        for k in self.p:
            ret[self.find(k)].append(k)
        if withkey:
            return ret
        return [e for e in ret.values()]
    def __str__(self):
        return str(self.to_lists())

