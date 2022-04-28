"""
convention: 
    every method use left closed and right closed interval
    `Interval` class represent closed interval

"""
from random import *
from sortedcontainers import SortedDict

class Itvattr:
    __slots__ = 'sz', 'val'
    def __init__(self, sz, val):
        self.sz, self.val = sz, val
    def __repr__(self):
        return f'Itvattr(sz={self.sz}, val={self.val})'

class ChthollyTree:
    """ 
        des: 
            flattened segment tree(similar to 1d quadtree, dynamically open and delete point), 
                every node stored in a SortedDict, with SegmentTree slot as key, node attribute as value
            base idea: after rather small times of assign function on random interval, the size of `self.A` become lg(n)
        
        example: 
            ChthollyTree({1: 10, 10: 20, 100: 30})
            self.nodes is {0:10, 1:20, 2:30}
        app: 
            1. huge of random assign operations
            2. single point query only 
                example: @cf#1638E

        time complexity: 
            O(nlg(lg(n))) with n random opeartions
                https://zhuanlan.zhihu.com/p/102786071
        test: 
            @cf#896C
                previous version(TLE): https://codeforces.com/contest/896/submission/148760838
                an unordered list https://codeforces.com/contest/896/submission/148760320
            @lc#2213
                single point assign only
    """
    def __init__(self, A): 
        self.itvs = SortedDict()
        n = len(A)
        prv = 0
        for cur in range(1, n+1):
            if cur==n or A[prv]!=A[cur]:
                self.itvs[prv] = Itvattr(cur-prv, A[prv])
                prv = cur
        # add two sentry
        self.itvs[-1] = Itvattr(0, None)
        self.itvs[n] = Itvattr(n, None)
    
    def split_at(self, x):
        """ split at gap between x-1 and x
        return rank of interval start at x
        assert: 0<=x<=n
        """
        itvs = self.itvs
        
        itv_rk = itvs.bisect_right(x)-1
        itv_l, itvattr = itvs.peekitem(itv_rk)
        # if x is already a leftendpoint
        if itv_l == x:
            return itv_rk
        
        totalsz = itvattr.sz
        itvattr.sz = x-itv_l
        itvs[x] = Itvattr(totalsz-itvattr.sz, itvattr.val)
        return itv_rk + 1
    
    def union_at(self, itv_l):
        """ union at gap between itv_l-1 and itv_l
        return rank of the interval contains itv_l
        assert: 0<=x<n, there is an interval whose leftendpoint is itv_l
        """
        itvs = self.itvs

        itv_rk = itvs.index(itv_l)
        c_itvattr = itvs[itv_l]
        
        # compare left interval with current interval
        _, l_itvattr = itvs.peekitem(itv_rk-1)
        
        if l_itvattr.val == c_itvattr.val:
            l_itvattr.sz += c_itvattr.sz
            itvs.popitem(itv_rk)
            return itv_rk-1
        return itv_rk


    def addition(self, l, r, v):
        """ des: increase all points in [l,r] by value v """
        # assert 0<=l<=r<n
        itvs = self.itvs
        lrk = self.split_at(l)
        rrk = self.split_at(r+1)
        for itvattr in itvs.values()[lrk:rrk]:
            itvattr.val += v
        
    def assign(self, l, r, v):
        """ des: assign all points in [l,r] by value v, then merge the interval included in [l,r] """
        # assert 0<=l<=r<n
        itvs = self.itvs

        lrk = self.split_at(l)
        rrk = self.split_at(r+1)
        
        for _ in range(rrk-lrk-1):
            itvs.popitem(lrk+1)
        itvattr = itvs[l]
        itvattr.val = v
        itvattr.sz = r-l+1
        
        # union is not necessary
        # self.union_at(l) 
        # self.union_at(r+1)

    def traverse(self, l, r):
        """ des: yield all values in [l,r] in format: (value, numberofvalue) 
        impl: instead of split operaton, discuss each situation manually
        """
        # assert 0<=l<=r<n
        itvs = self.itvs
        
        # traverse with pre_split
        """
        for itvattr in itvs.values()[self.split_at(l):self.split_at(r+1)]:
            yield itvattr.val, itvattr.sz
        """
        lrk = itvs.bisect_right(l)-1
        rrk = itvs.bisect_right(r)-1
        
        # case1: only one interval
        if lrk == rrk:
            yield itvs.peekitem(lrk)[1].val, r-l+1
            return 
        
        lmost_begin, lmost_itvattr = itvs.peekitem(lrk)
        yield lmost_itvattr.val, lmost_begin + lmost_itvattr.sz - l

        for itvattr in itvs.values()[lrk+1:rrk]:
            yield itvattr.val, itvattr.sz

        rmost_begin, rmost_itvattr = itvs.peekitem(rrk)
        yield rmost_itvattr.val, r - rmost_begin + 1



if __name__ == "__main__":
    def test_ChthollyTree_random():
        n = 40000
        A = [randint(-10, 10) for _ in range(n)]
        seed(121)
        
        tree = ChthollyTree(A)
        for _ in range(1000):
            op = randrange(3)
            l, r = sorted([randrange(n), randrange(n)])
            v = randint(-10, 10)
            if op == 0:
                iA = l
                for v,c in tree.traverse(l, r):
                    
                    for _ in range(c):
                        assert iA<len(A), "traverse yield wrong value number"
                        assert A[iA] == v, f"traverse yield wrong value, {A}, {tree.itvs}, {l,r}"
                        
                        iA += 1
            elif op == 1:
                tree.assign(l, r, v)
                for i in range(l, r+1): A[i]=v
            else:
                tree.addition(l, r, v)
                for i in range(l, r+1): A[i]+=v
        print("final interval number",len(tree.itvs))

    
    from timeit import default_timer as time
    sta = time()
    test_ChthollyTree_random()
    print(time()-sta)