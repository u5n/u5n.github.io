"""
des:
    this create a segment forest, 
                       2
                     /   \
              3     4     5
             / \   / \   / \
            6   7 8   9 10 11
            
        Ai: 0   1 2   3 4  5 
            
        the forest can be built bottom up layer by layer
            ```
            def build(n):
                nodes = [Node() for _ in range(2*n)]
                l = n 
                r = n*2 - 1
                l, r = (l+1)//2, (r-1)//2
                while l<=r:
                    for inode in range(l, r+1):
                        nodes[inode].left = nodes[inode*2].left
                        nodes[inode].right = nodes[inode*2+1].right
                    l, r = (l+1)//2, (r-1)//2   
            ```
        
time complexity:
    init: O(n)
    range query: O(lgn)
    point query: O(1)
    assign: O(lgn)

convention: 
    the segment tree implement use arraylist and node number start from 1
    range_query use closed interval

"""

class ST_single:
    """ 
    des:
        point modify, range query 
        the node store only one type of value
        the leaf node correspond to interval [i,i] has value `A[i]`
    merge_func: 
        any monoid operator such as max, min, xor
    test:
        @lc#2286
            https://leetcode.cn/submissions/detail/319512169/
    """
    __slots__ = 'n', 'nodes', 'merge'
    def __init__(self, A, merge_func):
        self.n = n = len(A)
        self.merge = merge_func
        self.nodes = [0]*n + A    
        for inode in reversed(range(1, self.n)):
            self.pull(inode)

    def pull(self, inode):
        merge, nodes = self.merge, self.nodes
        nodes[inode] = merge(nodes[inode*2], nodes[inode*2+1])

    def ancester(self, Ai):
        cur = self.n + Ai
        ret = []
        while cur>1:
            cur//=2
            ret.append(cur)
        return ret

    def subsegment(self, l, r):
        # use closed interval [l,r]
        seg_l, seg_r, l, r = [], [], l+self.n, r+self.n
        while l<=r:
            if l&1: seg_l.append(l)
            if r&1==0: seg_r.append(r)
            l=(l+1)//2
            r=(r-1)//2
        return seg_l + seg_r[::-1]

    def assign(self, Ai, v):
        self.nodes[Ai+self.n] = v
        for par in self.ancester(Ai):
            self.pull(par)

    def range_query(self, Al, Ar):
        nodes, merge = self.nodes, self.merge
        segs = iter(self.subsegment(Al, Ar))
        ret = nodes[next(segs)]
        for inode in segs:
            ret = merge(ret, nodes[inode])
        return ret

    def binary_search_first(self, Al, Ar, g):
        """ find min Ai(Al<=Ai<=Ar) that g(A[Ai]) """
        n, nodes = self.n, self.nodes        
        for inode in self.subsegment(Al, Ar):
            if ___(nodes[inode]):
                while inode<n: 
                    if ___(nodes[inode*2]):
                        inode = inode*2
                    else:
                        inode = inode*2+1
                return inode-n
        return

    def point_query(self, Ai):
        return self.nodes[self.n + Ai]

class ST_multi:
    """ an example 
    test:
        @lc#2286
            https://leetcode.cn/submissions/detail/319511689/
    """
    __slots__ = 'n', 'nodes'
    class ST_node:
        __slots__ = 'sum', 'max', 'Al', 'Ar'
        def __init__(self, sum, max, Al, Ar):
            self.sum, self.max, self.Al, self.Ar = sum, max, Al, Ar
        def leaf_assign(self, v):
            self.sum = self.max = v
    
    def __init__(self, A):
        self.n = n = len(A)
        self.nodes = nodes = [None]*n + [self.ST_node(v, v, i, i) for i,v in enumerate(A)]
        for inode in reversed(range(1, self.n)):
            nodes[inode] = self.ST_node(None, None, nodes[inode*2].Al,nodes[inode*2+1].Ar)
            self.pull(inode)

    def pull(self, inode):
        nodes = self.nodes
        par, lchi, rchi = nodes[inode], nodes[inode*2], nodes[inode*2+1]
        
        par.sum = lchi.sum + rchi.sum
        par.max = max(lchi.max, rchi.max)

    def ancester(self, Ai):
        cur = self.n + Ai
        ret = []
        while cur>1:
            cur//=2
            ret.append(cur)
        return ret

    def subsegment(self, l, r):
        # use closed interval [l,r]
        seg_l, seg_r, l, r = [], [], l+self.n, r+self.n
        while l<=r:
            if l&1: seg_l.append(l)
            if r&1==0: seg_r.append(r)
            l=(l+1)//2
            r=(r-1)//2
        return seg_l + seg_r[::-1]

    def assign(self, Ai, v):
        self.nodes[Ai+self.n].leaf_assign(v)
        for par in self.ancester(Ai):
            self.pull(par)
    
    def range_sum_query(self, Al, Ar):
        nodes = self.nodes
        segs = iter(self.subsegment(Al, Ar))
        ret = nodes[next(segs)].sum
        for inode in segs:
            ret = ret + nodes[inode].sum
        return ret

    def binary_search_first(self, Al, Ar, v):
        """ find min Ai(Al<=Ai<=Ar) that A[Ai]>=v """
        n, nodes = self.n, self.nodes        
        for inode in self.subsegment(Al, Ar):
            if nodes[inode].max>=v:
                while inode<n: 
                    if nodes[inode*2].max>=v:
                        inode = inode*2
                    else:
                        inode = inode*2+1
                return inode-n
        return

    def A_point_query(self, Ai):
        return self.nodes[self.n + Ai].sum