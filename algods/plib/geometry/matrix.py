from typing import *
from collections import *
"""  
des:
    this file also contain graph content
TOC:
    interval_sum_query0
    interval_sum_query
    prefix_sum
    prefix_sum_np0
    prefix_sum_np
    DiffArray
    adj_cells
    spiral_traverse
    matpow_mod
convention:
    use m to represent row number 
    use n to represent col number
"""

def interval_sum_query0(pre, r0, c0, r1, c1):
    """ pre is 0-indexed
    return sum(A[r0:r1, c0:c1]) """
    # assert 0<=r0<=r1<=m, 0<=c0<=c1<=n
    return pre[r1][c1] - pre[r1][c0] - pre[r0][c1] + pre[r0][c0]

def interval_sum_query(pre, r0, c0, r1, c1):
    """ pre is 1-indexed
    return sum(A[r0:r1+1, c0:c1+1]) """
    ret = pre[r1][c1]
    if r0!=0:
        ret -= pre[r0-1][c1]
        if c0!=0: 
            ret += pre[r0-1][c0-1]
    if c0!=0:
        ret -= pre[r1][c0-1]
    return ret

def prefix_sum(A):
    """ O(mn) 
    pre is 1-indexed, i.e. pre[r][c] == sum(A[:r, :c])
    """
    m, n = len(A), len(A[0])
    pre = [ [0]*(n+1) for _ in range(m+1)]
    for r in range(m):
        for c in range(n):
            pre[r+1][c+1] = A[r][c] + pre[r][c+1] + pre[r+1][c] - pre[r][c]
    return pre

import numpy as np
def prefix_sum_np(A):
    """ pre[r][c] == sum(A[:r, :c) 
    performance: 10x faster than native python
    """
    m, n = len(A), len(A[0])
    A_ = np.zeros((m+1, n+1), int)
    A_[1:,1:] = A
    np.cumsum(A_, axis=0, out=A_)
    np.cumsum(A_, axis=1, out=A_)
    return A_.tolist()
def prefix_sum_np0(A):
    """ pre[r][c] == sum(A[:r+1, :c+1) 
    performance: 10x faster than native python
    """
    pre = np.cumsum(A, axis=0)
    np.cumsum(pre, axis=1, out=pre)
    return pre.tolist()

class DiffArray:
    """ des: 
        for static and 2d array@M, this class maintain difference_array of M
        able to get the M in O(mn)
    test: @lc#2132
    """
    def __init__(self, m, n):
        self.diff = [[0]*n for _ in range(m)]
        self.m, self.n = m, n
    def add_interval(self, lx, ly, rx, ry, d):
        """ M[lx:ly, rx:ry] += d 
        assert 0<=lx<=rx, lx<m, 0<=ly<=ry, ly<n
        """
        diff = self.diff
        diff[lx][ly] += d
        if rx<self.m:
            diff[rx][ly] -= d
            if ry<self.n:
                diff[rx][ry] += d
        if ry<self.n:
            diff[lx][ry] -= d

    def get_M(self): return prefix_sum_np(self.diff)


Mod = int(1e9+7)
# if numpy is not available, use c++
import numpy as np
def matpow_mod(mat, b):
    """ np.power(mat, b)%Mod """
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