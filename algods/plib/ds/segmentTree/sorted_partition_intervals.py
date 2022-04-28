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
        self.itvs = SortedDict()
        A_keys = sorted(A.keys())
        A_Keys_iter = iter(A_keys)
        prv = next(A_Keys_iter)
        for cur in A_Keys_iter:
            if A[prv] != A[cur]:
                self.itvs[prv] = A[prv]
                prv = cur
        self.itvs[prv] = A[prv]
        # add a sentry
        self.itvs[-math.inf] = None 
    
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