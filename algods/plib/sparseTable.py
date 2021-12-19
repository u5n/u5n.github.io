"""
immutable 
preprocess O(nlgn)
range max/min query in O(1)
"""
import operator

# _ilog2_cache
maxn = 1000000
ilog2 = [0]*(maxn+1)
for i in range(1, maxn+1):
    ilog2[i] = ilog2[i-1] + (i%2==0)
class ST:
    def __init__(self, A, opt):
        n = len(A)
        maxj = ilog2[n]
        M = [[None]*(n) for _ in range(maxj+1)] # M[0][i]=i
        for i in range(n): M[0][i] = i
        for j in range(1, maxj+1):
            pow2j1 = 1<<(j-1)
            for i in range(n-(1<<j)+1):
                can1 = M[j-1][i]
                can2 = M[j-1][i+pow2j1]
                M[j][i]=can1 if opt(A[can1],A[can2]) else can2
        self.M = M
        self.opt = opt
        self.A = A
    def query(self,l,r):
        """query min(A[l:r+1])"""
        A, M, opt = self.A, self.M, self.opt
        k = ilog2[r-l+1]
        can1 = M[k][l]
        can2 = M[k][r-(1<<k)+1]
        return can1 if opt(A[can1],A[can2]) else can2