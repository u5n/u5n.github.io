from typing import *
from collections import *
"""  
des:
    this file shouldn't contain graph content
convention:
    use n to represent row number 
    use m to represent col number
"""

class prefix_sum:
    """ pre[r][c] == sum(A[:r, :c]) """
    def __init__(self, A):
        n, m = len(A), len(A[0])
        pre = [ [0]*(m+1) for _ in range(n+1)]
        for r in range(n):
            for c in range(m):
                pre[r+1][c+1] = A[r][c] + pre[r][c+1] + pre[r+1][c] - pre[r][c]
        return pre
    
    def itv_sum(self, r0, c0, r1, c1):
        """ return sum(A[r0:r1, c0:c1]) """
        if not( r0<r1 and c0<c1) : return 0
        pre = self.pre
        return pre[r1][c1] - pre[r1][c0] - pre[r0][c1] + pre[r0][c0]
        
import numpy as np
class np_prefix_sum:
    """ pre[r][c] == sum(A[:r, :c])
    performance: 10x faster than native python
    """
    def __init__(self, A):
        n, m = len(A), len(A[0])
        pre = np.zeros((n+1, m+1), int)
        pre[1:, 1:] = A
        np.cumsum(pre, axis=0, out=pre)
        np.cumsum(pre, axis=1, out=pre)
        self.pre = pre.tolist()
    
    def itv_sum(self, r0, c0, r1, c1):
        """ return sum(A[r0:r1, c0:c1]) """
        if not( r0<r1 and c0<c1) : return 0
        pre = self.pre
        return pre[r1][c1] - pre[r1][c0] - pre[r0][c1] + pre[r0][c0]


class DiffMatrix:
    """ des: 
        for static and 2d array@M, this class maintain difference_array of M
        can get the M in O(mn)
    test: @lc#2132
    """
    def __init__(self, n, m):
        self.diff = [[0]*m for _ in range(n)]
        self.n, self.m = n, m
    
    def add_itv(self, lx, ly, rx, ry, d):
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
    
    def get_native_M(self):
        M = np.cumsum(self.diff, axis=0)
        np.cumsum(M, axis=1, out=M)
        return M.tolist()
