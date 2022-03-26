"""
convention: node number start from 1
test: there is no need to test, I decide to follow up https://codeforces.com/blog/entry/18051
TOC:
    ST_template
    ST_template_perfectbinarytree
    ST_add
    ST_minval
    ST_minidx
"""

class ST_template:
    """ point modify, range query 
    operator: 
        any monoid operator such as max, min, xor
        if the opeartor is commutative, the class need a little change, refer to https://codeforces.com/blog/entry/18051
    """
    __slots__ = 'n', 'nodes'
    def __init__(self, n):
        self.n = n
        self.nodes = [0]*(2*n)
    
    def buildfrom(self, A):
        self.nodes[self.n:] = A
        for inode_id in reversed(range(1, self.n)):
            self.pull(inode_id)
    
    def pull(self, paridx):
        nodes = self.nodes
        nodes[paridx] = nodes[paridx*2] + nodes[paridx*2+1]

    def ancester(self, Ai):
        par = (self.n + Ai)//2
        while par:
            yield par
            par//=2
        
    def subsegment(self, l, r):
        nodes = self.nodes

        l += self.n
        r += self.n
        while l<r:
            if l&1: yield nodes[l]; l+=1
            if r&1: r-=1; yield nodes[r]
            l//=2
            r//=2


class ST_add:
    """ the opeartor is operator.add """
    __slots__ = 'n', 'nodes'
    def __init__(self, n):
        self.n = n
        self.nodes = [0]*(2*n)
    def buildfrom(self, A):
        self.nodes[self.n:] = A
        for inode_id in reversed(range(1, self.n)):
            self.pull(inode_id)

    def pull(self, paridx):
        nodes = self.nodes
        nodes[paridx] = nodes[paridx*2] + nodes[paridx*2+1]


    def add(self, Ai, v):
        curidx = self.n + Ai
        self.nodes[curidx] += v
        paridx = curidx // 2
        while paridx:
            self.pull(paridx)
            paridx //= 2

    def range_query(self, l, r):
        ret = 0
        l += self.n
        r += self.n
        while l<r:
            if l&1: ret += self.nodes[l]; l+=1
            if r&1: r-=1; ret += self.nodes[r]
            l//=2
            r//=2
        return ret

from math import inf
class ST_minval:
    """ the opeartor is operator.min 
    the node store the value
    """
    __slots__ = 'n', 'nodes'
    def __init__(self, n):
        self.n = n
        self.nodes = [0]*(2*n)
    def buildfrom(self, A):
        self.nodes[self.n:] = A
        for inode_id in reversed(range(1, self.n)):
            self.pull(inode_id)

    def pull(self, paridx):
        nodes = self.nodes
        nodes[paridx] = min(nodes[paridx*2], nodes[paridx*2+1])

    def assign(self, Ai, v):
        curidx = self.n + Ai
        self.nodes[curidx] = v
        paridx = curidx // 2
        while paridx:
            self.pull(paridx)
            paridx //= 2
    
    def range_min(self, l, r):
        ret = inf
        l += self.n
        r += self.n
        while l<r:
            if l&1: ret = min(ret, self.nodes[l]); l+=1
            if r&1: r-=1; ret = min(self.nodes[r], ret)
            l//=2
            r//=2
        return ret


class ST_minidx:
    """ the opeartor is operator.min 
    the node store the index with minvalue
    if multiple, use leftmost one
    """
    __slots__ = 'n', 'nodes'
    def __init__(self, n):
        self.n = n
        self.nodes = [0]*(2*n)
    def buildfrom(self, A):
        self.nodes[self.n:] = A
        for inode_id in reversed(range(1, self.n)):
            self.pull(inode_id)

    def pull(self, paridx):
        nodes = self.nodes
        lchi = nodes[paridx*2]
        rchi = nodes[paridx*2+1]
        if nodes[self.n+lchi] <= nodes[self.n+nodes[rchi]]:
            nodes[paridx] = lchi
        else:
            nodes[paridx] = rchi
    
    def assign(self, Ai, v):
        curidx = self.n + Ai
        self.nodes[curidx] = v
        paridx = curidx // 2
        while paridx:
            self.pull(paridx)
            paridx //= 2
    
    def range_min(self, l, r):
        n,nodes = self.nself.nodes
        retl = retr = None
        
        l += n
        r += n
        while l<r:
            if l&1: 
                if retl is None or nodes[n+retl] > nodes[n+nodes[l]]:
                    retl = nodes[l] 
                l+=1

            if r&1: 
                r-=1
                if retr is None or nodes[n+nodes[r]] <= nodes[n+retr]:
                    retr = nodes[r]
            l//=2
            r//=2

        if retl is None: 
            return retr 
        elif retr is None:
            return retl
        return retl if nodes[n+retl] <= nodes[n+retr] else retr
