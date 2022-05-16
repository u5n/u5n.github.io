import operator

ilog2 = lambda i: i.bit_length() - 1
class SparseTable:
    """
    range extreme query, without modify

    find the index with min values, if multiple indices, select leftmost
    """
    def __init__(self, A, opt=operator.lt):
        """ immutable 
        preprocess O(nlgn)
        interval max/min query in O(1), return index
        """
        n = len(A)
        maxj = ilog2(n)
        # j,i -> extreme on A[i:i+2**j]
        M = [[None]*(n) for _ in range(maxj+1)] 
        # M[0][i]=i
        for i in range(n): M[0][i] = i
        for j in range(1, maxj+1):
            pow2j1 = 1<<(j-1)
            for i in range(n-(1<<j)+1):
                can1 = M[j-1][i]
                can2 = M[j-1][i+pow2j1]
                M[j][i] = can1 if opt(A[can1],A[can2]) else can2
        self.M, self.opt, self.A = M, opt, A
        
    def query(self,l,r):
        """ret: min(A[l:r+1])
        assert: l<=r
        """
        A, M, opt = self.A, self.M, self.opt
        k = ilog2(r-l+1)
        can1 = M[k][l]
        can2 = M[k][r-(1<<k)+1]
        return can1 if opt(A[can1],A[can2]) else can2

if __name__ == '__main__':
    from random import *
    for _ in range(100):
        n = 100
        A = [randrange(-1e9, 1e9) for _ in range(n)]
        st = SparseTable(A)
        
        for l in range(n):
            for r in range(l, n):
                assert min(range(l,r+1),key=lambda i:A[i]) == st.query(l, r)