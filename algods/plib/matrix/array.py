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
    use n to represent row number 
    use m to represent col number
"""
import copy
from itertools import product

def prefix_sum1(A):
    """ pre is 1-indexed, i.e. pre[r][c] == sum(A[:r, :c]) """
    n, m = len(A), len(A[0])
    pre = [ [0]*(m+1) for _ in range(n+1)]
    for r in range(n):
        for c in range(m):
            pre[r+1][c+1] = A[r][c] + pre[r][c+1] + pre[r+1][c] - pre[r][c]
    return pre

import numpy as np
def prefix_sum1_np(A):
    """ pre[r][c] == sum(A[:r, :c])
    performance: 10x faster than native python
    """
    n, m = len(A), len(A[0])
    A_ = np.zeros((n+1, m+1), int)
    A_[1:, 1:] = A
    np.cumsum(A_, axis=0, out=A_)
    np.cumsum(A_, axis=1, out=A_)
    return A_.tolist()

def interval_sum1_query(pre, r0, c0, r1, c1):
    """ pre is 1-indexed
    return sum(A[r0:r1, c0:c1]) """
    return pre[r1][c1] - pre[r1][c0] - pre[r0][c1] + pre[r0][c0]


# zero_indexed_prefix
def prefix_sum0(A):
    """ pre[r][c] == sum(A[:r+1, :c+1])
    performance: 10x faster than native python
    """
    n, m = len(A), len(A[0])
    pre = [row[:] for row in A]
    for r,c in product(range(n), range(1, m)):
        pre[r][c] += pre[r][c-1]
    for r,c in product(range(1, n), range(m)):
        pre[r][c] += pre[r-1][c]
    return pre

def prefix_sum0_np(A):
    """ pre[r][c] == sum(A[:r+1, :c+1])
    performance: 10x faster than native python
    """
    pre = np.cumsum(A, axis=0)
    np.cumsum(pre, axis=1, out=pre)
    return pre.tolist()

def interval_sum0_query(pre, r0, c0, r1, c1):
    """ pre is 0-indexed
    return sum(A[r0:r1+1, c0:c1+1])
    assert: 0<=r0<=r1<=n, 0<=c0<=c1<=m
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

class DiffMatrix:
    """ des: 
        for static and 2d array@M, this class maintain difference_array of M
        able to get the M in O(mn)
    test: @lc#2132
    """
    def __init__(self, n, m):
        self.diff = [[0]*m for _ in range(n)]
        self.n, self.m = n, m
    def add_interval(self, lx, ly, rx, ry, d):
        """ M[lx:ly, rx:ry] += d 
        assert 0<=lx<=rx, lx<n, 0<=ly<=ry, ly<m
        """
        diff = self.diff
        diff[lx][ly] += d
        if rx<self.n:
            diff[rx][ly] -= d
            if ry<self.m:
                diff[rx][ry] += d
        if ry<self.m:
            diff[lx][ry] -= d

    def get_M(self): return prefix_sum0_np(self.diff)


