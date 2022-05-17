"""
des:
    this create a segment forest, 
        the tree is built bottom up layer by layer
            ```
            def build(n):
                nodes = [Node()]*(2*n)
                l = n 
                r = n*2 -1 
                while r-l+1 >1:
                    l, r = (l+1)//2, (r-1)//2
                    for inode in range(l, r+1):
                        nodes[inode].left = nodes[inode*2]
                        nodes[inode].right = nodes[inode*2+1]
            ```
        a node numbered i 
            has two child i*2 and i*2+1
            if i&1:
                it's right child(if has parent)
            else:
                it's left child(if has parent)
        
        
convention: 
    node number start from 1
    use closed interval

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
        cur = self.n + Ai
        while cur>1:
            cur//=2
            yield cur

    def subsegment(self, l, r):
        n, nodes = self.n, self.nodes

        l += n
        r += n
        while l<=r:
            if l&1: yield nodes[l]
            if r&1==0: yield nodes[r]
            l=(l+1)//2
            r=(r-1)//2

    def binary_search_first(self, Al, Ar, f):
        """ find min i(Al<=i<=Ar) that f(i), if f is monotonic increased bool function"""
        n = nodes = self.n, self.nodes
        g = ___ # inode -> EXIST{;f(j); j in inode correspond interval}
        def binary_search_node(inode):
            while inode<n: 
                if g[inode*2]:
                    inode = inode*2
                else:
                    inode = inode*2+1
            return inode-n
        
        l, r = Al+n, Ar+n
        subitv = []
        while l<=r:
            if l&1: subitv.append(l)
            if 0==r&1: subitv.append(r)
            l=(l+1)//2
            r=(r-1)//2
        for inode in subitv:
            if g[inode]:
                return binary_search_node(inode)
        raise Exception("not found")


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


    def addition(self, Ai, v):
        cur = self.n + Ai
        self.nodes[cur] += v
        while cur:
            cur //= 2
            self.pull(cur)

    def range_query(self, l, r):
        ret = 0
        l += self.n
        r += self.n
        while l<=r:
            if l&1: ret += self.nodes[l]
            if r&1==0: ret += self.nodes[r]
            l=(l+1)//2
            r=(r-1)//2
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
        lchi, rchi = nodes[paridx*2], nodes[paridx*2+1]
        nodes[paridx] = lchi if lchi < rchi else rchi

    def assign(self, Ai, v):
        cur = self.n + Ai
        self.nodes[cur] = v
        while cur:
            cur //= 2
            self.pull(cur)
    
    def range_min(self, l, r):
        ret = inf
        l += self.n
        r += self.n
        while l<=r:
            if l&1: ret = min(ret, self.nodes[l])
            if r&1==0: ret = min(self.nodes[r], ret)
            l=(l+1)//2
            r=(r-1)//2
        return ret


class ST_minidx:
    """ the opeartor is operator.min 
    the node store the index with minvalue
    if multiple, use leftmost one
    """
    __slots__ = 'n', 'nodes', 'leaves'
    def __init__(self, n):
        self.n = n
        self.nodes = [0]*(2*n)

    def buildfrom(self, A):
        n = self.n 
        for Ai in range(n):
            self.nodes[Ai+n] = Ai
        self.leaves = list(A)
        for inode_id in reversed(range(1, self.n)):
            self.pull(inode_id)

    def pull(self, paridx):
        n, nodes = self.n, self.nodes
        lchi, rchi = nodes[paridx*2], nodes[paridx*2+1]
        if nodes[n+lchi] <= nodes[n+rchi]:
            nodes[paridx] = lchi
        else:
            nodes[paridx] = rchi
    
    def assign(self, Ai, v):
        cur = self.n + Ai
        self.leaves[cur] = v
        while cur:
            cur //= 2
            self.pull(cur)
    
    def range_min(self, l, r):
        nodes, n = self.nodes, self.n
        seg_l, seg_r, l, r = [], [], l+n, r+n
        while l<=r:
            if l&1: seg_l.append(l)
            if r&1==0: seg_r.append(r)
            l=(l+1)//2
            r=(r-1)//2
        
        iseg = iter(seg_l + seg_r[::-1])
        res = next(iseg)
        for inode in iseg:
            if nodes[n+inode] < nodes[n+res]:
                res = inode
        return res