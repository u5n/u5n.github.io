from math import *
from itertools import islice
import operator

min2 = lambda l,r: l if l<r else r
max2 = lambda l,r: l if l>r else r
class SqrtDecompositionSingle:
    """
    time:
        init: O(n)
        interval query: O(√n)
        point change with monoid merge func: O(√n)
        point change with group merge func: O(1)
        point query: O(1)
    des:
        similar to segment tree, it can divide any interval into O(√n) nodes ( complete block or single point )
        `self.merge`:
            a binary operator
            each block@A[l:r] maintain the result of `reduce(self.merge, A[l:r])`
        if the last block is not full:
            it will not be used

    """
    __slots__ = 'A', 'n', 'blocks', 'block_sz', 'id_ele', 'merge'
    def __init__(self, A, merge):
        n = len(A)
        if merge in (max, min):
            self.assign = self.assign_monoidopt
            id_ele = -inf if merge is max else inf
            merge = max2 if merge is max else min2
        elif merge in (operator.add, operator.xor):
            self.assign = self.assign_groupopt
            id_ele = 0
        else:
            raise Exception("unknown operator")

        block_sz = isqrt(n)
        n_blocks = floor(n/block_sz) # use `floor` to ignore last not full block

        blocks = [id_ele]*n_blocks
        
        for i,e in enumerate(A):
            block_id = i// block_sz
            blocks[block_id] = merge(blocks[block_id], e)

        self.A, self.n, self.blocks, self.block_sz = A, n, blocks, block_sz    
        self.id_ele, self.merge = id_ele, merge

    def range_query(self, l, r):
        """ query on A[l:r] 
        time: O(√n)
        """
        A, merge, block, block_sz = self.A , self.merge, self.blocks, self.block_sz

        # ceil to nearest left endpoint of block 
        lend = l + (-l % block_sz)
        # floor to nearest left endpoint of block
        rend = r - (r % block_sz)
        ret = self.id_ele

        # don't contain any completely block
        if lend >= rend:
            for i in range(l, r):
                ret = merge(ret, A[i])
        else:
            for i in range(l, lend):
                ret = merge(ret, A[i])
            for block_id in range(lend//block_sz, rend//block_sz):
                ret = merge(ret, block[block_id])
            for i in range(rend, r):
                ret = merge(ret, A[i])
        return ret


    def assign_monoidopt(self, i, v):
        """ des: assign also recalculate the whole block, apply to monoid opeartor
        time: O(n) """
        A, blocks, merge, block_sz, id_ele = self.A, self.blocks, self.merge, self.block_sz, self.id_ele
        block_id = i//block_sz
        
        if v==merge(A[i], v): # if A[i] < v:
            blocks[block_id] = merge(blocks[block_id], v)
            return
        elif A[i] == v: 
            return
        
        # if last block is incomplete, ignore it
        if block_id == len(blocks): return

        # recalculate blocks[block_id]
        blocks[block_id] = id_ele
        A[i] = v
        for Ai in self.block_range(block_id):
            blocks[block_id] = merge(blocks[block_id], A[Ai])

    def assign_groupopt(self, i, v):
        """ des: assign A[i] to v, assume the operator is a group 
        time: O(1) """
        A, blocks, merge = self.A, self.blocks, self.merge
        block_id = i//self.block_sz
        
        # if last block is incomplete, ignore it
        if block_id == len(blocks): return

        # inverse operation of self.merge
        blocks[block_id] = ___(blocks[block_id], A[i])
        A[i] = v
        blocks[block_id] = merge(blocks[block_id], v)

    def recalc_range(self, block_id):
        """ used when multiple value inside a block has been changed """
        A, blocks, merge, block_sz, n, id_ele = self.A, self.blocks, self.merge, self.block_sz, self.n, self.id_ele
        lend, rend = l - (l % block_sz), r + (-r % block_sz)
        for block_id in range(lend//block_sz, rend//block_sz):
            blocks[block_id] = id_ele
            for Ai in self.block_range(block_id):
                blocks[block_id] = merge(blocks[block_id], A[Ai])
            lend += block_sz

    def block_range(self, block_id):
        lend = block_id*self.block_sz
        return range(lend, min2(self.n, lend + self.block_sz))


class SqrtDecompositionMulti:
    class Node:
        __slots__ = 'max', 'sum'
        def __init__(self, max, sum):
            self.max, self.sum = max, sum
    __slots__ = 'A', 'n', 'blocks', 'block_sz'
    def __init__(self, A):
        n = len(A)
        block_sz = isqrt(n)
        n_blocks = ceil(n/block_sz)
        blocks = [ self.Node(-inf, 0) for _ in range(n_blocks)]
        
        for i,e in enumerate(A):
            block_id = i// block_sz

            blocks[block_id].max = max2(blocks[block_id].max, e)
            blocks[block_id].sum += e

        self.A, self.n, self.blocks, self.block_sz = A, n, blocks, block_sz    

    def iterate_nodes(self, l, r):
        """ 
        yield nodes in the interval [l:r]
            the node type could be a single value
            the node type could be `self.Node`

        time: O(√n)
        """
        A,  block, block_sz = self.A , self.blocks, self.block_sz

        # ceil to nearest leftendpoint of block 
        lend = l + (-l % block_sz)
        # floor to nearest rightendpoint of block
        rend = r - (r % block_sz)

        ret = []
        # don't contain any completely block
        if lend >= rend:
            for i in range(l, r):
                ret.append((i, A[i]))
        else:
            for i in range(l, lend):
                ret.append((i, A[i]))
            for block_id in range(lend//block_sz, rend//block_sz):
                ret.append((block_id*block_sz, block[block_id]))
            for i in range(rend ,r):
                ret.append((i, A[i]))
        return ret


    def range_sum_query(self, l, r):
        ret = 0
        for _, node in self.iterate_nodes(l, r):
            ret += node.sum if isinstance(node, self.Node) else node
        return ret
                
    def assign(self, i, v):
        A, blocks, block_sz = self.A, self.blocks, self.block_sz
        block_id = i//block_sz
        ov, A[i] = A[i], v
        # if last block is incomplete, ignore it
        if block_id == len(blocks): return
        blocks[block_id].sum += v - ov
        # recalculate blocks[block_id].max
        blocks[block_id].max = -inf
        if v > ov:
            blocks[block_id].max = max2(blocks[block_id].max, v)
        else:
            for Ai in self.block_range(block_id):
                blocks[block_id].max = max2(blocks[block_id].max, A[Ai])
    
    def recalc_range(self, l, r):
        """ recalculate block overlap with [l,r) """
        A, blocks, block_sz = self.A, self.blocks, self.block_sz
        lend, rend = l - (l % block_sz), r + (-r % block_sz)
        for block_id in range(lend//block_sz, rend//block_sz):
            blocks[block_id].max = -inf
            blocks[block_id].sum = 0
            for Ai in self.block_range(block_id):
                blocks[block_id].max = max2(blocks[block_id].max, A[Ai])
                blocks[block_id].sum += A[Ai]

    def block_range(self, block_id):
        lend = block_id*self.block_sz
        return range(lend, min2(self.n, lend + self.block_sz))


def mosalgorithm(A, queries):
    """ process offline queries where the queriese contains some inclusive intervals 
    time: O( Q√Q + (N+Q)F√N + QG)
        where G is time of `get_answer`
        F is time of `ds.add`
    """
    ___ = print("Code Template, need finish"), 1/0
    n = len(A)
    block_sz = isqrt(n)
    def query_cmp(q):
        l,r,i = q
        i_block = l//block_sz
        return i_block, r if i_block%2==0 else -r
    sq = sorted([(l,r,i) for i,(l,r) in enumerate(queries)], key=query_cmp)
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
    # testcase1 RMQ and RSumQ without assign
    n = 100
    import random
    A = [random.randrange(-100, 100) for _ in range(n)]
    sq_max = SqrtDecompositionSingle(A, max)
    sq_sum = SqrtDecompositionSingle(A, operator.add)
    # for i,e in enumerate(A):
    #     sq_max.assign(i, e)
    #     sq_sum.assign(i, e)
    for l in range(n):
        for r in range(l+1, n+1):
            assert max(A[l:r]) == sq_max.range_query(l,r)
            assert sum(A[l:r]) == sq_sum.range_query(l,r)
                