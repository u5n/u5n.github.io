"""
_:
    name: binary indexed tree
convention:
    tree node number start from 1
    the target array `A` index start from 0
adv/dis compare to other bottomup segment tree:
    adv: faster
    dis: 
        can't break interval into smaller intervals(there is a node correspond to)
            don't support opeartor without inverse element
            don't support binary search on interval

each method use Left-closed, right-open interval
"""

class BIT:
    """ 
    des:
        for a static array `A`, it support a group operator on `A`:
            1. single element change
            2. range accumulative operation on `A`
        the operator shoule be a group
    default: 
        use `operator.add` and `math.sum`
        tarr[i] = sum(A[i+1-lowbit(i+1):i+1])
    """
    __slots__='n','tarr'	
    def __init__(self, n):
        self.n = n
        self.tarr = [0] * (n+1)

    def buildfrom(self, A):
        tarr = self.tarr
        n = len(A)
        pre = [0]*(n+1)
        for i in range(n):
            pre[i+1] = pre[i] + A[i]
        for inode in range(1, 1+n):
            tarr[inode] = pre[inode] - pre[inode&(inode-1)]
        
    def add(self, idx, delta):
        n, tarr = self.n, self.tarr
        idx += 1
        while idx <= n:
            tarr[idx] += delta
            idx += idx&-idx

    def sum(self, idx, idx2=None):
        """ sum(A[slice(idx[,idx2])]) """
        tarr = self.tarr
        if idx2!=None: return self.sum(idx2)-self.sum(idx)
        ret = 0
        while idx:
            ret += tarr[idx]
            idx &= idx-1 # idx -= lowbit(idx)
        return ret
        
    def point_query(self, i):
        """ calculate A[i], by find all children of a tree node """
        tarr = self.tarr
        res = tarr[i]
        bound = i&(i-1)
        i -= 1
        while i>bound:
            res -= tarr[i]
            i&=i-1
        return res

    def kth(self, k):
        """ des: 
            return min i that sum(i+1)>k
            if BIT is a Counter, it find the kth(start from 0) smallest element
        time: O(lg(n))
        exec example:
            ```
            maxv = 100
            B = BIT(maxv)
            A=[1,1,1,2,3,3,3,3,4]
            for v in A:
                B.add(v, 1)
            for k in range(len(A)):
                assert B.kth(k) == A[k]
            assert B.kth(len(A)+1) == maxv
            ```
        """
        n, tarr = self.n, self.tarr
        
        bit = 1<<(n.bit_length()-1)
        pre = 0 # prefix 
        while bit:
            cur = pre + bit
            if cur <= n and k >= tarr[cur]:
                # go to next right sibling (shrink the interval by half)
                k -= tarr[cur]
                pre = cur
            # if cur > self.n or k < self.tarr[cur-1]:
            #     go to leftmost child ( shrink the interval by half )
            bit >>= 1
        return pre

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
        bit0, bit1 = self.bit0, self.bit1
        """ assert 0<=l<=r; l<n; r can exceed n """
        bit0.add(l, v)
        bit1.add(l, (l-1)*v)
        if r<self.n:
            bit0.add(r , -v)
            bit1.add(r, -(r-1)*v)
    def sum(self, idx, idx2=None):
        if idx2 != None: return self.sum(idx2) - self.sum(idx)
        return (idx-1)*self.bit0.sum(idx) - self.bit1.sum(idx)

# index start from 0, and 2 dimension
class BIT2d:
    """ des: for an static 2darray `A`, it support point addition and rectangle query on `A` """
    __slots__='m', 'n', 'tarr'
    def __init__(self, n, m):
        self.n, self.m = n,m
        self.tarr = [[0]*(m+1) for _ in range(n+1)]
    
    def add(self, idx, delta):
        """ A[idx] += delta """
        tarr, n, m = self.tarr, self.n, self.m
        x = idx[0]+1
        while x <= n:
            y = idx[1]+1
            while y <= m:
                tarr[x][y] += delta
                y += y&-y
            x += x&-x
    
    def sum(self, idx, idx2=None):
        """ sum(A[:idx[0],:idx[1]]) or sum(A[idx[0]:idx2[0], idx[1]:idx2[1]]) """
        if idx2!=None:
            return self.sum(idx2) + self.sum(idx) - self.sum((idx[0],idx2[1])) - self.sum((idx2[0],idx[1]))
        tarr = self.tarr
        ret, x = 0, idx[0]
        while x:
            y = idx[1]
            while y:
                ret += tarr[x][y]
                y &= y-1
            x &= x-1
        return ret

class BIT2d_diff(BIT2d):
    """ des: for an static 2darray `A`, it support rectangle addition and single point query on `A` 
    time: each O(lg(n)*lg(m))
    """
    def interval_add(self, idx, idx2, delta):
        """ A[idx[0]:idx2[0], idx[1]:idx2[1]] += delta """
        add = self.add
        add(idx, delta)
        add((idx[0], idx2[1]), -delta)
        add(idx2, delta)
        add((idx2[0], idx[1]), -delta)
    def query(self, idx):
        """ return A[idx] """
        return self.sum((idx[0]+1, idx[1]+1))



if __name__ == '__main__':
    """ test BIT class """
    from random import *
    def test_BIT():
        n = 212
        A = [random() for i in range(n)]
        B = BIT(n)
        for i,e in enumerate(A):
            B.add(i, e)
        lowbit = lambda x:x&-x
        for i in range(n):
            assert B.tarr[i+1] == sum(A[i+1-lowbit(i+1):i+1])
        
        atol=1e-08
        for i in range(n):
            assert abs(B.sum(0, i+1) - sum(A[:i+1])) <= atol

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
        assert A == [B.point_query(i) for i in range(n)]
    
    test_BIT()
    test_BIT_diff()