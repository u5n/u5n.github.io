from collections import defaultdict
class Dsu:
    """ 
    the parent relationship is maintain by a list A
        of a representative r, `-A[r]` is size of set correspond r
        of a non-representative x, `A[x]` is parent of x
    the element is numbered in [0,n)
    the dummynode is numbered in [n,inf]
    invariant: 
        1. every set that size>=2  representative is dummynode 
        2. all parent are dummynode
    """
    __slots__ = 'p', 'n_sets', 'n'
    def __init__(self, n):
        self.p = [-1]*n
        self.n = self.n_sets = n
                    
    def find(self, u):
        p = self.p
        if p[u] >= 0:
            p[u] = self.find(p[u])
            return p[u]
        else:
            return u

    def unite(self, oril, orir):
        n,p = self.n,self.p
        l, r = self.find(oril), self.find(orir)
        if l == r: return False
        # when no dummynode as representative
        if l<n and r<n:
            dummynode = len(p)
            p[r] = dummynode
            p[l] = dummynode
            p.append(-2)
            self.n_sets -= 1        
            return True
        
        if r<n or -p[l] > -p[r]: l, r = r, l
            
        p[r] += p[l]
        p[l] = r
    
        self.n_sets -= 1
        return True
    
    def detach(self, u):
        """ make a set that only contain u """
        p = self.p
        assert(u<len(p))
        repru = self.find(u)
        if -p[repru] > 1:
            p[repru] += 1
            p[u] = -1
            self.n_sets += 1

        
    def to_sets(self):
        """
        key is resentative
        value is the set
        """
        ret = defaultdict(list)
        for k in range(self.n):
            ret[self.find(k)].append(k)
        return ret

    def __repr__(self): return str(self.to_sets().items()).replace("dict_items", "Dsu")