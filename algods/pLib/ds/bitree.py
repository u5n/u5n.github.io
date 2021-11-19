lowbit = lambda x: x&-x
# index start from 0
class BIT:
    __slots__='n','bit'	
    def __init__(self, n):
        self.n = n
        self.bit = [0] * n

    def add(self, idx, delta):
        """ A[idx]+=delta """
        while idx < self.n:
            self.bit[idx] += delta
            # add (only rightmost 0 set 1)
            idx += lowbit(idx+1)

    def sum(self, idx, idx2):
        """ sum(A[slice(idx[,idx2])]) """
        if idx2!=None: return self.sum(idx2)-self.sum(idx)
        ret = 0
        while idx >= 1:
            ret += self.bit[idx-1]
            # sub (only rightmost 1 set 1)
            idx -= lowbit(idx)
        return ret

# index start from 0, and 2 dimension
class BIT2:
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
                y += lowbit(y+1)
            x+=lowbit(x+1)
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
                y -= lowbit(y)
            x -= lowbit(x)
        return ret