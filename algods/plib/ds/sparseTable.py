import operator

class SparseTable:
    """
    range extreme query, without modify

    find the index with min values, if multiple indices, select leftmost
    """
    def __init__(self, A, merge):
        """ immutable 
        preprocess O(nlgn)
        interval max/min query in O(1), return index
        """
        n = len(A)
        maxj = n.bit_length() - 1
        M = [[None]*(n) for _ in range(maxj+1)] 

        for i in range(n): M[0][i] = i
        for j in range(1, maxj+1):
            pow2j1 = 1<<(j-1)
            for i in range(n-(1<<j)+1):
                M[j][i] = merge(M[j-1][i], M[j-1][i+pow2j1])
        self.M, self.merge, self.A = M, merge, A
        
    def query(self,l,r):
        """ret: min(A[l:r+1])
        assert: l<=r
        """
        A, M, merge = self.A, self.M, self.merge
        k = (r-l+1).bit_length() - 1
        can1 = M[k][l]
        can2 = M[k][r-(1<<k)+1]
        return merge(A[can1],A[can2])

if __name__ == '__main__':
    from random import *
    for _ in range(100):
        n = 100
        A = [randrange(-1e9, 1e9) for _ in range(n)]
        st = SparseTable(A)
        
        for l in range(n):
            for r in range(l, n):
                assert min(range(l,r+1),key=lambda i:A[i]) == st.query(l, r)