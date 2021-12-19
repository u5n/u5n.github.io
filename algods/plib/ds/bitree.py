# index start from 0
# use Left-closed, right-open interval
class BIT:
    """ binary indexed tree build on `A`
    bit[i] = sum(A[i+1-lowbit(i+1):i+1])
    support: point add & range query 
    """
    __slots__='n','bit'	
    def __init__(self, n):
        self.n = n
        self.bit = [0] * n

    def add(self, idx, delta):
        """ A[idx]+=delta 
        parent结点p, lowbit(p+1) > lowbit(idx+1)
        因此p右侧连续1比idx多
        等式: p&(p+1) == p + 1 - lowbit(p+1) == {p右侧连续1全变0}
        同时满足 
            p > idx
            p&(p+1) <= idx 
        因此 p 除去右侧连续1外的部分与idx相同
        因此只需要枚举p中连续1的个数
        """
        while idx < self.n:
            self.bit[idx] += delta
            idx |= idx+1

    def sum(self, idx, idx2=None):
        """ sum(A[slice(idx[,idx2])]) """
        if idx2!=None: return self.sum(idx2)-self.sum(idx)
        ret = 0
        while idx >= 1:
            ret += self.bit[idx-1]
            idx &= idx-1 # idx = idx - lowbit(idx)
        return ret
    def findA(self):
        # O(nlgn)
        return [ self.sum(i,i+1) for i in range(self.n)]

class BIT_diff(BIT):
    """ binary indexed tree build on diff(A) 
        below operation is on `A`
    support: range addition & point query
    """
    def range_add(self, l, r, v):
        self.add(l, v)
        if r != self.n: self.add(r, -v)
    def query(self, i):
        return self.sum(i+1)

class BIT_range:
    """ binary indexed tree build on A
    A = diff(A0)
    A0(x) = x*B0(x) - B1(x)
    below operation is on `A`
    support: range addition & range query
    """
    __slots__ = 'bit0', 'bit1', 'n'
    def __init__(self, n):
        self.bit0 = BIT(n)
        self.bit1 = BIT(n)
        self.n = n
    def range_add(self, l, r, v):
        self.bit0.add(l, v)
        self.bit1.add(l, (l-1)*v)
        if r!=self.n:
            self.bit0.add(r , -v)
            self.bit1.add(r, -(r-1)*v)
    def sum(self, idx, idx2=None):
        if idx2 != None: return self.sum(idx2) - self.sum(idx)
        return (idx-1)*self.bit0.sum(idx) - self.bit1.sum(idx)

# index start from 0, and 2 dimension
class BIT2d:
    __slots__='m', 'n', 'bit'
    def __init__(self, shape):
        self.m,self.n = shape
        self.bit = {}
        
    def add(self, idx, delta):
        x = idx[0]
        while x < self.m:
            y = idx[1]
            while y < self.n:
                self.bit[x,y] = self.bit.get((x,y),0)+delta
                y |= y+1
            x|=x+1
    def sum(self, idx, idx2=None):
        """ sum(A[:idx[0],:idx[1]]) or sum(A[idx[0]:idx2[0],idx[1]:idx2[1]]) """
        if idx2!=None:
            return self.sum(idx2) + self.sum(idx) - self.sum((idx[0],idx2[1])) - self.sum((idx2[0],idx[1]))
        ret=0
        x = idx[0]
        while x>=1:
            y = idx[1]
            while y>=1:
                ret += self.bit.get((x,y),0)
                y &= y-1
            x &= x-1
        return ret

if __name__ == '__main__':
    n = 100
    import random
    A = [random.random() for i in range(n)]
    B = BIT(n)
    for i,e in enumerate(A):
        B.add(i, e)
    lowbit = lambda x:x&-x
    for i in range(n):
        assert B.bit[i] == sum(A[i+1-lowbit(i+1):i+1])
    
    atol=1e-08
    for i in range(n):
        assert abs(B.sum(i+1) - sum(A[:i+1])) <= atol

