class ST_diff_add:
    """  range addition, point query
    consider derivative  of the `A`
    operator: any commutative-monoid operator such as max, min, xor
    """
    def __init__(self, n):
        self.n = n
        self.nodes = [0]*(2*n)
    
    def buildfrom(self, A):
        self.nodes[self.n:] = A
    
    def restore(self):
        # topdown push increment into child
        nodes = self.nodes
        for inode in range(1, self.n):
            nodes[inode//2] += nodes[inode]
            nodes[inode//2+1] += nodes[inode]
            nodes[inode] = 0

    def ancester(self, Ai):
        nodes = self.nodes

        ret = 0
        cur = (self.n + Ai)//2
        while cur:
            ret += nodes[cur]
            cur//=2
        
        return ret
    def range_addition(self, l, r, v):
        nodes = self.nodes

        l += self.n
        r += self.n
        while l<r:
            if l&1: nodes[l]+=v; l+=1
            if r&1: r-=1; nodes[r]+=v
            l//=2
            r//=2
