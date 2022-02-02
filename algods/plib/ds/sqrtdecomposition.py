from math import *
from itertools import islice
import operator

class Sqrtdecomposition:
    def __init__(self, n, opt=max, id_ele=-inf, A=None):
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
    def query(self, l, r):
        # query on A[l:r]
        A = self.A 

        lend = l + (-l % self.block_sz)
        rend = r - (r % self.block_sz)
        ret = self.id_ele
        if lend >= rend:
            for Ai in islice(A, l, r):
                ret=self.opt(ret, Ai)
        else:
            for Ai in islice(A, l, lend):
                ret=self.opt(ret, Ai)
            for block in islice(self.blocks, lend//self.block_sz, rend//self.block_sz):
                ret=self.opt(ret, block)
            for Ai in islice(A, rend, r):
                ret=self.opt(ret, Ai)
        return ret
    def assign_monoid(self, i, v):
        """ des: assign also recalculate the whole block, apply to monoid opeartor
        time: O(n) """
        p_blocks = i//self.block_sz
        # # when self.opt is max
        # if self.A[i] < v:
        #     self.blocks[p_blocks] = max(self.blocks[p_blocks], v)
        #     return
        # elif self.A[i] == v: 
        #     return
        self.A[i] = v
        lend = p_blocks * self.block_sz
        for Ai in islice(self.A, lend, min(self.n, lend + self.block_sz)):
            self.blocks[p_blocks] = self.opt(self.blocks[p_blocks], Ai)
    def assign(self, i, v):
        """ des: assign A[i] to v, assume the operator is a group 
        time: O(1) """
        p_blocks = i//self.block_sz
        reverse_opt = operator.__sub__ # inverse self.opt
        assert reverse_opt != None
        self.blocks[p_blocks] = operator.__sub__(self.blocks[p_blocks], self.A[i])
        self.A[i] = v
        self.blocks[p_blocks] = self.opt(self.blocks[p_blocks], v)

if __name__ == "__main__":
    # testcase1 RMQ and RSQ
    n = 100
    sq_ext = Sqrtdecomposition(n)
    sq_sum = Sqrtdecomposition(n, operator.add, 0)
    import random
    A = [random.randrange(-100, 100) for _ in range(n)]
    for i,e in enumerate(A):
        sq_ext.assign_monoid(i, e)
        sq_sum.assign(i, e)
    for l in range(n):
        for r in range(l+1, n+1):
            assert max(A[l:r]) == sq_ext.query(l,r)
            assert sum(A[l:r]) == sq_sum.query(l,r)
                