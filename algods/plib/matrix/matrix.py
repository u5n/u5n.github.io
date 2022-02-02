from typing import *
from collections import *
"""  
des:
    this file also contain graph content
TOC:
    IntsumQuery
    adj_cells
    spiral_traverse
    matpow_mod
convention:
    use m to represent row number 
    use n to represent col number
"""

class IntsumQuery:
    """ static and immutable 2d array, interval sum query use prefix sum """
    def __init__(self, A):
        m, n = len(A), len(A[0])
        # pre[r][c] == sum(A[:r, :c])
        pre = [ [0]*(n+1) for _ in range(m+1)]
        for r in range(m):
            for c in range(n):
                pre[r+1][c+1] = A[r][c] + pre[r][c+1] + pre[r+1][c] - pre[r][c]
        self.pre = pre

    def query(self, r0, c0, r1, c1):
        """ return sum(A[r0:r1, c0:c1]) """
        # assert 0<=r0<=r1<=m, 0<=c0<=c1<=n
        return self.pre[r1][c1] - self.pre[r1][c0] - self.pre[r0][c1] + self.pre[r0][c0]

def bfs(A, start: Iterable):
    """ multi source bfs start at `start`, on `A` """
    m,n=len(A), len(A[0])
    # matrix explore
    def adj_cells(ux, uy):
        """ yield adjacent cells that in bounds """
        # top tr right rd down dl left lt
        # (-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)
        # top right down left 
        for dx,dy in (-1,0),(0,1),(1,0),(0,-1):
            x,y = ux+dx,uy+dy
            if 0<=x<m and 0<=y<n: # and A[x][y]
                yield x,y
    
    q = list(start)
    vis = set(q)
    d = 0
    while q:
        pq = q
        q = []
        for x, y in pq:
            for nxt in adj_cells(x, y):
                if nxt not in vis:
                    q.append(nxt)
                    vis.add(nxt)
        d += 1


Mod = int(1e9+7)
# if numpy is not available, use c++
import numpy as np
def matpow_mod(mat, b):
    # np.power(mat, b)
    n = len(mat)
    ret = np.eye(n, n, dtype=np.uint64) 
    while b:
        if b&1:
            ret = (ret@mat)%Mod
        b >>= 1
        mat = (mat@mat)%Mod
    return ret

def spiral_traverse(mat):
    """
    spiral matrix generator
    start at topleft
    clockwise
    """
    m,n=len(mat),len(mat[0])
    maxl = (min(m,n)+1)//2
    for l in range(maxl):
        h = m - l*2
        w = n - l*2
        if w==1:
            # right
            for i in range(h):
                yield l+i,l
        elif h==1:
            # down
            for i in range(w):
                yield l,l+i
        else:
            # topleft: l,l
            # topright: l,l+w-1
            # bottomright: l+h-1,l+w-1
            # bottomleft: l+h-1,l
            x = y = l
            # go right
            for _ in range(w-1):
                yield x,y
                y+=1
            # go down
            for _ in range(h-1):
                yield x,y
                x+=1
            # go left
            for _ in range(w-1):
                yield x,y
                y-=1
            # go up
            for _ in range(h-1):
                yield x,y
                x-=1