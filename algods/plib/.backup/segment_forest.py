"""
create a segment forest size 6 , get the node corresponding interval
            2
          /   \
     3   4     5
    / \ / \   / \
    6 7 8  9 10 11
    0 1 2  3 4  5 
application: ?
"""
class ST_template_running:
    """ 
    get the node correspond interval in the running time
    point modify, range query 
    """
    __slots__ = 'n', 'nodes'
    def __init__(self, n):
        self.n = n
        self.nodes = [None]*(2*n)
    
    def buildfrom(self, A):
        n, nodes = self.n, self.nodes
        nodes[self.n:] = A
        l, r = n, n*2-1
        Almin, itv_sz = 0, 1
        while l<r:
            if l&1: Almin += itv_sz
            l, r, itv_sz = (l+1)//2, (r-1)//2, itv_sz*2
            for inode in range(l,r+1):
                self.pull(inode, Almin+(inode-l)*itv_sz, itv_sz)
    
    def pull(self, paridx, Al, itv_sz):
        nodes = self.nodes
        lchi = nodes[paridx*2]
        rchi = nodes[paridx*2+1]
        nodes[paridx].val = lchi.val + rchi.val

    def assign(self, Ai, v):
        n, nodes = self.n, self.nodes
        
        cur = n + Ai
        nodes[cur] = v
        itv_sz = 1
        while cur:
            if cur&1:
                Ai -= itv_sz
                if Ai < 0: break
            cur>>=1
            itv_sz<<=1
            if Ai+itv_sz > n: break
            self.pull(cur, Ai, itv_sz)

    def subsegment(self, l, r):
        n, nodes = self.n, self.nodes

        l += n
        r += n
        while l<=r:
            if l&1: yield nodes[l]
            if r&1==0: yield nodes[r]
            l=(l+1)//2
            r=(r-1)//2

        
class ST_template_cache:
    """ point modify, range query 
    preprocess the node correspond interval 
    the node.Al, node.Ar information is wrong on some unused(subsegment function won't yield) nodes
    """
    __slots__ = 'n', 'nodes'
    class Node:
        # repr use closed interval [Al, Ar]
        __slots__ = 'val Al Ar'
        def __init__(self, val, Al, Ar):
            self.val,self.Al,self.Ar= val,Al,Ar

    def __init__(self, A):
        Node = self.Node
        nodes = [None]*(2*n)
        for Ai in range(n):
            nodes[Ai+n] = Node(A[Ai], Ai, Ai)
        for inode in reversed(range(1,n)):
            nodes[inode] = Node(None, nodes[inode*2].Al, nodes[inode*2+1].Ar)
            self.pull(inode)
        nodes, n = self.nodes, self.n

    def pull(self, paridx):
        nodes = self.nodes
        par, lchi, rchi = nodes[paridx], nodes[paridx*2], nodes[paridx*2+1]
        nodes[paridx].val = lchi.val + rchi.val

    def assign(self, Ai, v):
        n, nodes = self.n, self.nodes

        cur = n + Ai
        nodes[cur] = v
        while cur>1:
            cur//=2
            self.pull(cur)
    
    def subsegment(self, l, r):
        n, nodes = self.n, self.nodes

        l += n
        r += n
        while l<=r:
            if l&1: yield nodes[l]
            if r&1==0: yield nodes[r]
            l=(l+1)//2
            r=(r-1)//2