"""
convention: 
    every method use left closed and right closed interval
    `Interval` class represent closed interval

"""
from sortedcontainers import SortedDict
import math

class ChthollyTree:
    """ 
        des: 
            flattened segment tree(similar to 1d quadtree, dynamically open and delete point), 
                every node stored in a SortedDict, with left endpoint of SegmentTree node corresponding interval as key, node attribute as value
            
        time complexity: 
            ctor: O(nlgn)
            per operation: O(lg(n)) 
        test: 
            @cf#896C
                previous version(TLE): https://codeforces.com/contest/896/submission/148760838
                an unordered list https://codeforces.com/contest/896/submission/148760320
            @lc#2213
                single point assign only
            @lccn#LCP52
    """
    def __init__(self, A): 
        """ example:
                A=enumerate("abaab")
                A=[(10, 1), (100, 2), (1000, 3)]
                    [-inf, 10) value is None
                    [10, 100) value is 1
                    [100, 1000) value is 2
                    [1000, +inf) value is 3
        """
        self.itvs = SortedDict({-math.inf: None})
        prv = 0
        n = len(A)
        for cur in range(1+n):
            if cur==n or A[prv][1] != A[cur][1]:
                self.itvs[A[prv][0]] = A[prv][1]
                prv = cur
    
    def split_at(self, x):
        """ split at gap between x-1 and x
        return rank of interval start at x
        """
        itvs = self.itvs
        
        itv_rk = itvs.bisect_right(x)-1
        itv_l, itvattr = itvs.peekitem(itv_rk)
        # if x is already a leftendpoint
        if itv_l == x:
            return itv_rk
        

        # strictly, this shoule be copy.copy(itvattr), even deepcopy, but slower
        itvs[x] = itvattr
        return itv_rk + 1
    
    def union_at(self, itv_l):
        """ union at gap between itv_l-1 and itv_l
        return rank of the interval contains itv_l
        assert: there is an interval whose leftendpoint is itv_l
        """
        itvs = self.itvs

        itv_rk = itvs.index(itv_l)
        cur_itvattr = itvs[itv_l]
        
        # compare left interval with current interval
        lft_itvattr = itvs.values()[itv_rk-1]
        
        if lft_itvattr == cur_itvattr:
            itvs.popitem(itv_rk)
            return itv_rk-1
        return itv_rk
        
    def assign(self, l, r, v):
        """ des: assign all points in [l,r] by value v, then merge the interval included in [l,r] """
        # assert 0<=l<=r<n
        itvs = self.itvs

        lrk = self.split_at(l)
        rrk = self.split_at(r+1)
        
        itvs[l] = v
        del itvs.iloc[lrk+1:rrk]
        
        self.union_at(l) 
        self.union_at(r+1)

    def point_query(self, x):
        return self.itvs.values()[ self.itvs.bisect_right(x)-1 ]

import bisect
class ChthollyTreeList:
    """ the ChthollyTree implemented by arraylist
    python>=3.10
    """
    def __init__(self, A): 
        self.itvs = [[-math.inf, None]]
        prv = 0
        n = len(A)
        for cur in range(1, n+1):
            if cur==n or A[prv][1] != A[cur][1]:
                self.itvs.append(list(A[prv]))
                prv = cur
    
    def split_at(self, x):
        """ split at gap between x-1 and x
        return rank of interval start at x
        """
        itvs = self.itvs
        
        itv_rk = bisect.bisect_right(itvs, x, key=lambda x:x[0])-1
        itv_l, itvattr = itvs[itv_rk]
        # if x is already a leftendpoint
        if itv_l == x:
            return itv_rk
        
        # strictly, this shoule be `[x, copy.copy(itvattr)]`, even deepcopy, but slower
        itvs[itv_rk+1:itv_rk+1] = [x, itvattr]
        return itv_rk + 1
    
    def union_at(self, itv_l):
        """ union at gap between itv_l-1 and itv_l
        return rank of the interval contains itv_l
        assert: there is an interval whose leftendpoint is itv_l
        """
        itvs = self.itvs

        itv_rk = bisect.bisect_right(itvs, itv_l, key=lambda x:x[0])-1
        cur_itvattr = itvs[itv_l]
        
        # compare left interval with current interval
        lft_itvattr = itvs[itv_rk-1][1]
        
        if lft_itvattr == cur_itvattr:
            itvs[itv_rk:itv_rk+1] = []
            return itv_rk-1
        return itv_rk
        
    def assign(self, l, r, v):
        """ des: assign all points in [l,r] by value v, then merge the interval included in [l,r] """
        # assert 0<=l<=r<n
        itvs = self.itvs

        lrk = self.split_at(l)
        rrk = self.split_at(r+1)
        
        itvs[lrk][1] = v
        itvs[lrk+1:rrk] = []
        
        self.union_at(l) 
        self.union_at(r+1)

    def point_query(self, x):
        itvs = self.itvs
        return itvs[ bisect.bisect_right(itvs, x, key=lambda x:x[0])-1 ][1]