"""
 index start from 0
each method use Left-closed, right-open interval
"""

from collections import defaultdict


class BIT:
    """ des:
        bit[i] = sum(A[i+1-lowbit(i+1):i+1])
        for an static array `A`, it support single point addition and range query on `A`
    """
    __slots__='n','bit'	
    def __init__(self, n):
        self.n = n
        self.bit = [0] * n

    def add(self, idx, delta):
        
        while idx < self.n:
            self.bit[idx] += delta
            idx |= idx+1 # idx += lowbit(idx+1)

    def sum(self, idx, idx2=None):
        """ sum(A[slice(idx[,idx2])]) """
        if idx2!=None: return self.sum(idx2)-self.sum(idx)
        ret = 0
        while idx >= 1:
            ret += self.bit[idx-1]
            idx &= idx-1 # idx -= lowbit(idx)
        return ret
        
    def findA(self):
        # todo: this can be optimized
        return [ self.sum(i,i+1) for i in range(self.n)]

class BIT_diff(BIT):
    """ des: for an static array `A`, it support range addition & point query on `A`
    impl: use a `BIT` to maintain `diff(A)`
    """
    def range_add(self, l, r, delta):
        """ A[l:r] += v """
        self.add(l, delta)
        if r != self.n: self.add(r, -delta)
    def point_query(self, i):
        """ return A[i] """
        return self.sum(i+1)
    

class BIT_range:
    """ des: for an static array `A`, it support range addition & range query `A`
    impl: 
        A0 := diff_rev(A)
        A0(x) = x*B0(x) - B1(x)
        use `BIT_diff` to maintain `B0` and `B1`
    """
    __slots__ = 'bit0', 'bit1', 'n'
    def __init__(self, n):
        self.bit0 = BIT(n)
        self.bit1 = BIT(n)
        self.n = n
    def range_add(self, l, r, v):
        """ assert 0<=l<=r; l<n; r can exceed n """
        self.bit0.add(l, v)
        self.bit1.add(l, (l-1)*v)
        if r<self.n:
            self.bit0.add(r , -v)
            self.bit1.add(r, -(r-1)*v)
    def sum(self, idx, idx2=None):
        if idx2 != None: return self.sum(idx2) - self.sum(idx)
        return (idx-1)*self.bit0.sum(idx) - self.bit1.sum(idx)

# index start from 0, and 2 dimension
class BIT2d:
    """ des: for an static 2darray `A`, it support point addition and rectangle query on `A` """
    __slots__='m', 'n', 'bit'
    def __init__(self, m, n):
        self.m, self.n = m, n
        self.bit = [[0]*n for _ in range(m)]

    def add(self, idx, delta):
        """ A[idx] += delta """
        x = idx[0]
        while x < self.m:
            y = idx[1]
            while y < self.n:
                self.bit[x,y] += delta
                y |= y+1
            x|=x+1

    def sum(self, idx, idx2=None):
        """ sum(A[:idx[0],:idx[1]]) or sum(A[idx[0]:idx2[0], idx[1]:idx2[1]]) """
        if idx2!=None:
            return self.sum(idx2) + self.sum(idx) - self.sum((idx[0],idx2[1])) - self.sum((idx2[0],idx[1]))
        ret=0
        x = idx[0]
        while x>=1:
            y = idx[1]
            while y>=1:
                ret += self.bit[x-1, y-1]
                y &= y-1
            x &= x-1
        return ret

class BIT2d_diff(BIT2d):
    """ des: for an static 2darray `A`, it support rectangle addition and single point query on `A` 
    time: each O(lg(m)*lg(n))
    """
    def interval_add(self, idx, idx2, delta):
        """ A[idx[0]:idx2[0], idx[1]:idx2[1]] += delta 
        this is designed to allow idx2[0]>=m and idx2[1]>=n; add a sentry line and column to avoid lots of `if` 
        """
        add = self.add
        add(idx, delta)
        if idx2[1]<self.n:
            add((idx[0], idx2[1]), -delta)
            if idx2[0] < self.m:
                add(idx2, delta)
        if idx2[0]<self.m:
            add((idx2[0], idx[1]), -delta)
    def query(self, idx):
        """ return A[idx] """
        return self.sum((idx[0]+1, idx[1]+1))

if __name__ == '__main__':
    """ test BIT class """
    from random import *
    def test_BIT():
        n = 100
        A = [random() for i in range(n)]
        B = BIT(n)
        for i,e in enumerate(A):
            B.add(i, e)
        lowbit = lambda x:x&-x
        for i in range(n):
            assert B.bit[i] == sum(A[i+1-lowbit(i+1):i+1])
        
        atol=1e-08
        for i in range(n):
            assert abs(B.sum(i+1) - sum(A[:i+1])) <= atol

    """ test BIT_diff class """
    def test_BIT_diff():
        n = 100
        A = [0]*n
        B = BIT_diff(n)
        for _ in range(50):
            l = randrange(n)
            r = randrange(l,n)
            v = choice([-32,-16,-8,-4,-2,-1,1,2,4,8,16,32])
            B.range_add(l, r, v)
            for i in range(l,r): A[i]+=v
        assert A == [B.query(i) for i in range(n)]