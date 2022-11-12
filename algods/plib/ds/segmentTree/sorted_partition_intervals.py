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
            flattened segment tree(dynamically open and delete point), 
                every node stored in a SortedDict, with left endpoint of SegmentTree node corresponding interval as key, node attribute as value
            
        time complexity: 
            ctor: O(nlgn)
            per operation: O(lg(n)) 
        test: 
            @lc#2276: https://leetcode.cn/submissions/detail/323946479/
            @lc#2213
                single point assign only
            @lc#352: https://leetcode.cn/submissions/detail/323963103/
            
            @lccn#LCP52
    """
    __slots__ = 'itvs'
    def __init__(self, A=None):
        """ example:
                A=enumerate("abaab")
                A=[(10, 1), (100, 2), (1000, 3)]
                    [-inf, 10) value is None
                    [10, 100) value is 1
                    [100, 1000) value is 2
                    [1000, +inf) value is 3
        """
        self.itvs = SortedDict({-math.inf: None})
        if A:
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
        if itvs[itv_l] == itvs.values()[itv_rk-1]:
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
        del itvs.keys()[lrk+1:rrk]
        
        self.union_at(l) 
        self.union_at(r+1)
    
    def point_query(self, x): return self.itvs.values()[ self.itvs.bisect_right(x)-1 ]
    def itv_sz(self, rk): 
        """ if store interval size into interval values, then it maybe slower """
        return self.itvs.peekitem(rk+1)[0] - self.itvs.peekitem(rk)[0]
    
    def get_super(self, l, r):
        """ find interval that completely contain [l,r], include sentry intervals [..., +inf) or [-inf, ...) """
        itvs = self.itvs
        lrk = itvs.bisect_right(l)-1
        if lrk+1==len(itvs):
            if itvs.keys()[lrk+1] > r:
                return lrk
        
        return None

    def __repr__(self):
        ret = ""
        for k,v in self.itvs.items():
            if k!=-math.inf:
                ret += f"[{k} -> {v}]"
        return 'ChthollyTree(' + ret + ')'

    def __len__(self): return len(self.itvs)-1



import bisect
class ChthollyTreeArray:
    """ the ChthollyTree implemented by arraylist
    only for len(A)<=100000
    python>=3.10
    performance:
        don't know how to measure
        and `self.itvs` can use `ds.sqrtArray`
    test:
        @lc#2276
            https://leetcode.cn/submissions/detail/323970243/
    """
    __slots__ = 'itvs'
    def __init__(self, A=None): 
        self.itvs = [[-math.inf, None]]
        if A:
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
        # itv_rk = itvs.bisect_key_right(x, key=lambda x:x[0])-1
        itv_l, itvattr = itvs[itv_rk]
        # if x is already a leftendpoint
        if itv_l == x:
            return itv_rk
        
        # strictly, this shoule be `[x, copy.copy(itvattr)]`, even deepcopy, but slower
        itvs[itv_rk+1:itv_rk+1] = [[x, itvattr]]
        return itv_rk + 1
    
    def union_at(self, itv_l):
        """ union at gap between itv_l-1 and itv_l
        return rank of the interval contains itv_l
        assert: there is an interval whose leftendpoint is itv_l
        """
        itvs = self.itvs
        itv_rk = bisect.bisect_left(itvs, itv_l, key=lambda x:x[0])
        # itv_rk = itvs.bisect_key_left(itv_l, key=lambda x:x[0])
        if itvs[itv_rk-1][1] == itvs[itv_rk][1]:
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
        return itvs[ bisect.bisect_right(itvs, x, key=lambda y:y[0])-1 ][1]
    
    def itv_sz(self, rk):
        return self.itvs[rk+1][0] - self.itvs[rk][0]

    def get_super(self, l, r):
        """ find interval that completely contain [l,r], include sentry intervals [..., +inf) or [-inf, ...) """
        itvs = self.itvs
        lrk = bisect.bisect_right(itvs, l, key=lambda x:x[0])-1
        # lrk = itvs.bisect_right(l, key=lambda x:x[0])-1
        if lrk+1==len(itvs):
            if itvs[lrk+1][0] > r:
                return lrk
        
        return None

    def __repr__(self):
        ret = ""
        for k,v in self.itvs:
            if k!=-math.inf:
                ret += f"[{k} -> {v}]"
        return 'ChthollyTreeArray(' + ret + ')'

    def __len__(self): return len(self.itvs)-1