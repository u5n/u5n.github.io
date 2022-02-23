from math import *
from itertools import islice
import operator

class SqrtDecomposition:
    """
    preprocess in O(n), space O(n)
    maintain an arraylist
    method
        interval query O(√n)
        point change O(√n)
        point query O(1)
    """
    def __init__(self, n, opt=max, id_ele=-inf, A=None):
        if opt in (max, min):
            self.assign = self.assign_monoidopt
        elif opt in (operator.add, operator.xor):
            self.assign = self.assign_groupopt
        else:
            raise Exception("unknown binary operator")
        block_sz = isqrt(n)
        n_blocks = ceil(n/block_sz)
        blocks = [id_ele]*n_blocks
        if A:
            self.A = A
            for i,e in enumerate(A):
                p_blocks = i// block_sz
                blocks[p_blocks] = opt(blocks[p_blocks], e)
        else:
            self.A = [id_ele]*n
        self.n, self.blocks, self.opt, self.block_sz = n, blocks, opt, block_sz    
        self.id_ele = id_ele
    def query_interval(self, l, r):
        """ query on A[l:r] 
        time: O(√n)
        """
        A, opt, block, block_sz = self.A , self.opt, self.block, self.block_sz

        lend = l + (-l % block_sz)
        rend = r - (r % block_sz)
        ret = self.id_ele
        if lend >= rend:
            for i in range(l, r):
                ret=opt(ret, A[i])
        else:
            for i in range(l, lend):
                ret=opt(ret, A[i])
            for i_block in range(lend//block_sz, rend//block_sz):
                ret=opt(ret, block[i_block])
            for i in range(rend ,r):
                ret=opt(ret, A[i])
        return ret
    def assign_monoidopt(self, i, v):
        """ des: assign also recalculate the whole block, apply to monoid opeartor
        time: O(n) """
        A, blocks, opt = self.A, self.blocks, self.opt
        p_blocks = i//self.block_sz
        
        # when self.opt is max
        if v==opt(A[i], v): # if A[i] < v:
            blocks[p_blocks] = max(blocks[p_blocks], v)
            return
        elif A[i] == v: 
            return
        
        # recalculate blocks[p_blocks]
        A[i] = v
        lend = p_blocks * self.block_sz
        for Ai in range(lend, min(self.n, lend + self.block_sz)):
            Av = A[Ai]
            blocks[p_blocks] = self.opt(blocks[p_blocks], Av)
    def assign_groupopt(self, i, v):
        """ des: assign A[i] to v, assume the operator is a group 
        time: O(1) """
        p_blocks = i//self.block_sz
        reverse_opt = operator.__sub__ # inverse self.opt
        assert reverse_opt != None
        self.blocks[p_blocks] = operator.__sub__(self.blocks[p_blocks], self.A[i])
        self.A[i] = v
        self.blocks[p_blocks] = self.opt(self.blocks[p_blocks], v)

def mosalgorithm(A, queries):
    """ process offline queries where the queriese contains some inclusive intervals 
    time: O( Q√Q + (N+Q)F√N + QG)
        where G is time of `get_answer`
        F is time of `ds.add`
    """
    ___ = print("Code Template, need finish"), 1/0
    n = len(A)
    block_sz = isqrt(n)
    def query_opt(q):
        l,r,i = q
        i_block = l//block_sz
        return i_block, r if i_block%2==0 else -r
    sq = sorted([(l,r,i) for i,(l,r) in enumerate(queries)], key=query_opt)
    ds = ___
    ret = [None]*len(queries)
    l , r = 0,-1 # represent an inclusive interval
    for ql,qr,qi in sq:
        while l>ql: l-=1; ds.add(A[l])
        while l<ql: ds.remove(A[l]); l+=1
        while r<qr: r+=1; ds.add(A[r])
        while r>qr: ds.remove(A[r]); r-=1
        ret[qi] = ___
        
    return ret
if __name__ == "__main__":
    # testcase1 RMQ and RSQ
    n = 100
    import random
    A = [random.randrange(-100, 100) for _ in range(n)]
    sq_max = SqrtDecomposition(n, A=A)
    sq_sum = SqrtDecomposition(n, operator.add, 0, A=A)
    # for i,e in enumerate(A):
    #     sq_max.assign(i, e)
    #     sq_sum.assign(i, e)
    for l in range(n):
        for r in range(l+1, n+1):
            assert max(A[l:r]) == sq_max.query_interval(l,r)
            assert sum(A[l:r]) == sq_sum.query_interval(l,r)
                