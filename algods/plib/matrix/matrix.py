from typing import *
from collections import *
"""  
des:
    this file shouldn't contain graph content
TOC:
    interval_sum_query
    prefix_sum
    prefix_sum_np
    {zero indexed prefix sum}
        interval_sum_query0
        prefix_sum_np0
    DiffArray
    spiral_traverse
    matpow_mod
convention:
    use m to represent row number 
    use n to represent col number
"""


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
    """ pre[r][c] == sum(A[:r, :c])
    performance: 10x faster than native python
    """
    m, n = len(A), len(A[0])
    A_ = np.zeros((m+1, n+1), int)
    A_[1:, 1:] = A
    np.cumsum(A_, axis=0, out=A_)
    np.cumsum(A_, axis=1, out=A_)
    return A_.tolist()

def interval_sum_query(pre, r0, c0, r1, c1):
    """ pre is 1-indexed
    return sum(A[r0:r1, c0:c1]) """
    return pre[r1][c1] - pre[r1][c0] - pre[r0][c1] + pre[r0][c0]


def zero_indexed_prefix():
    def prefix_sum_np0(A):
        """ pre[r][c] == sum(A[:r+1, :c+1])
        performance: 10x faster than native python
        """
        pre = np.cumsum(A, axis=0)
        np.cumsum(pre, axis=1, out=pre)
        return pre.tolist()

    def interval_sum_query0(pre, r0, c0, r1, c1):
        """ pre is 0-indexed
        return sum(A[r0:r1+1, c0:c1+1])
        assert: 0<=r0<=r1<=m, 0<=c0<=c1<=n
        """
        ret = pre[r1][c1]
        if c0 == 0 and r0 == 0:
            return ret 
        elif c0 == 0:
            return ret - pre[r0-1][c1]
        elif r0 == 0:
            return ret - pre[r1][c0-1]
        else:
            return ret - pre[r1][c0-1] - pre[r0-1][c1]

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


