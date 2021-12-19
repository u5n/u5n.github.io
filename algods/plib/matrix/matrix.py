from typing import *
from collections import *
"""  
des:
    this file also contain graph content
todo 
    quick matrix powmod 
    quick matrix powmod use numpy operator
    consider in function parameter, using pair or two paras
TOC:
    prefixsum
    adj
convention:
    use m to represent row number 
    use n to represent col number
"""
class PrefixsumQuery:
    def __init__(self, A):
        m,n = len(A), len(A[0])
        # pre[r][c] == sum(A[:r, :c])
        pre = [ [0]*(n+1) for _ in range(m+1)]
        for r in range(m):
            for c in range(n):
                pre[r+1][c+1] = A[r][c] + pre[r][c+1] + pre[r+1][c] - pre[r][c]
        self.pre = pre

    def query(self, r0, c0, r1, c1):
        """ return sum(A[r0:r1, c0:c1]) """
        # assert 0<=r0<=r1<m, 0<=c0<=c1<n
        return self.pre[r1+1][c1+1] - self.pre[r1+1][c0] - self.pre[r0][c1+1] + self.pre[r0][c0]

# matrix explore
# m,n = len(A),len(A[0])
def adj(ux, uy, m, n):
    """ yield adjacent cells that in bounds
    """
    # top tr right rd down dl left lt
    # (-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)
    # top right down left 
    for dx,dy in (-1,0),(0,1),(1,0),(0,-1):
        x,y = ux+dx,uy+dy
        if 0<=x<m and 0<=y<n:
            yield x,y

def topo_sort(M, f):
    """ topological sort """
    m,n = len(M),len(M[0])
    ind = [[0]*n for _ in range(m)]
    for ux in range(m):
        for uy in range(n):
            for v in adj(ux, uy, m, n):
                if f((ux, uy), v):

    for u in range(n):
        for v in G[u]:
            ind[v]+=1
    
    q = deque()
    for u in range(n):
        if ind[u]==0:
            q.append(u)
    
    ret = []
    while q:
        u = q.pop()
        ret.append(u)
        for v in G[u]:
            ind[v]-=1
            if ind[v]==0:
                q.append(v)
    
    if len(ret)==n:
        return ret
    raise Exception("not DAG")