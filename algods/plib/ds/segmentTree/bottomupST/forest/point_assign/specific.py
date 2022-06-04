""" 
TOC:
    ST_add
    ST_minval
    ST_maxval
    ST_minidx

"""
class ST_add:
    """ the merge func is operator.add """
    __slots__ = 'n', 'nodes'
    def __init__(self, A):
        self.n = n = len(A)
        self.nodes = nodes = [0]*n + A
        for inode in reversed(range(1, n)):
            nodes[inode] = nodes[inode*2] + nodes[inode*2+1]

    def addition(self, Ai, v):
        nodes = self.nodes
        inode = self.n + Ai
        self.nodes[inode] += v
        while inode:
            inode //= 2
            nodes[inode] = nodes[inode*2] + nodes[inode*2+1]
    
    def addition(self, Ai, v):
        nodes = self.nodes
        inode = self.n + Ai
        self.nodes[inode] += v
        while inode:
            inode //= 2
            nodes[inode] = nodes[inode*2] + nodes[inode*2+1]

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
    
    def point_query(self, Ai):
        return self.nodes[self.n + Ai]


from math import inf
class ST_minval:
    """ the merge func is operator.min 
    the node store the value
    """
    __slots__ = 'n', 'nodes'
    def __init__(self, A):
        self.n = n = len(A)
        self.nodes = [0]*n + A
        for inode_id in reversed(range(1, n)):
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
    
    def range_query(self, l, r):
        ret = inf
        l += self.n
        r += self.n
        while l<=r:
            if l&1: ret = min(ret, self.nodes[l])
            if r&1==0: ret = min(self.nodes[r], ret)
            l=(l+1)//2
            r=(r-1)//2
        return ret
    
    def point_query(self, Ai):
        return self.nodes[Ai+self.n]


class ST_maxval:
    __slots__ = 'n', 'nodes'
    def __init__(self, A):
        self.n = n = len(A)
        self.nodes = [0]*n + A
        for inode_id in reversed(range(1, n)):
            self.pull(inode_id)

    def pull(self, paridx):
        nodes = self.nodes
        lchi, rchi = nodes[paridx*2], nodes[paridx*2+1]
        nodes[paridx] = lchi if lchi > rchi else rchi

    def assign(self, Ai, v):
        cur = self.n + Ai
        self.nodes[cur] = v
        while cur:
            cur //= 2
            self.pull(cur)
    
    def range_min(self, l, r):
        ret = -inf
        l += self.n
        r += self.n
        while l<=r:
            if l&1: ret = max(ret, self.nodes[l])
            if r&1==0: ret = max(self.nodes[r], ret)
            l=(l+1)//2
            r=(r-1)//2
        return ret

    def binary_search_first(self, Al, Ar, v):
        # find MIN{Ai; Al<=Ai<=Ar; A[Ai]>=v}
        n, nodes= self.n, self.nodes            

        l, r = Al+n, Ar+n
        seg_l, seg_r = [], []

        while l<=r:
            if l&1: seg_l.append(l)
            if 0==r&1: seg_r.append(r)
            l=(l+1)//2
            r=(r-1)//2

        for inode in seg_l + seg_r[::-1]:
            if nodes[inode] >= v:
                while inode < n:
                    if nodes[inode*2] >= v:
                        inode = inode*2
                    else:
                        inode = inode*2 + 1
                return inode - n

        return
    
    def point_query(self, Ai):
        return self.nodes[self.n+Ai]



class ST_minidx:
    """ the opeartor is `lambda lAid, rAid: lAid if A[lAid]<A[rAid] or(A[lAid]==A[rAid] and lAid<rAid) else rAid`
    the node store the arraylist_index with minvalue
    if multiple, use the leftmost one
    """
    __slots__ = 'n', 'nodes', 'A'
    def __init__(self, A):
        self.n = n = len(A)
        self.nodes = [None]*n + list(range(n)) 
        self.A = A
        for inode_id in reversed(range(1, self.n)):
            self.pull(inode_id)

    def pull(self, paridx):
        nodes, A = self.nodes, self.A
        lchi, rchi = nodes[paridx*2], nodes[paridx*2+1]
        nodes[paridx] = lchi if A[lchi] <= A[rchi] else rchi
    
    def assign(self, Ai, v):
        cur = self.n + Ai
        self.A[cur] = v
        while cur:
            cur //= 2
            self.pull(cur)
    
    def range_min(self, l, r):
        """ try to write without sentry """
        A = self.A
        nodes, n = self.nodes, self.n
        seg_l, seg_r, l, r = [], [], l+n, r+n
        
        while l<=r:
            if l&1: seg_l.append(l)
            if r&1==0: seg_r.append(r)
            l=(l+1)//2
            r=(r-1)//2
        
        iseg = iter(seg_l + seg_r[::-1])
        cAid = nodes[next(iseg)]
        
        for inode in iseg:
            othAid = nodes[inode] 
            if A[cAid] > A[othAid]:
                cAid = othAid
            
        return cAid