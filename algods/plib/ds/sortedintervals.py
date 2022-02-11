"""
convention: 
    every method use left closed and right closed interval
    `Interval` class represent closed interval

"""
from collections import Counter, namedtuple
from random import *
from sortedcontainers import SortedList, SortedDict

class Interval:
    __slots__ = 'l', 'r', 'val'
    def __init__(self, l, r, val=None):
        self.l, self.r, self.val = l, r, val
    def __repr__(s): return f"Interval({s.l},{s.r},{s.val})"


class SortedIntervals:
    """ des: a collection of ordered and disjoint closed intervals ( endpoint is integers )
    app: the online algorithm of [meeting rooms](https://leetcode.com/problems/meeting-rooms)
    """
    def __init__(self):
        self.ints = SortedList(key=lambda x: x.l)

    def get_sub(self, l, r):
        """ find all intervals in `self` that fully contained in [l,r] 
        return two indices on `self.ints`, `self.ints[lfind:rfind+1]` are fully contained in [l,r]
        if no such interval, return the original `lfind` and `rfind`, (`rfind-lfind<0`)
        """
        ints = self.ints 
        # find all intervals that left endpoint in [l,r]
        lfind = ints.bisect_key_left(l)
        rfind = ints.bisect_key_right(r) - 1
        if rfind >= lfind:
            if ints[rfind].r > r:
                return lfind, rfind - 1
        return lfind, rfind

    def get_overlap(self, l, r):
        """  similar to `self.get_sub` """
        ints = self.ints 
        # find all intervals that left endpoint in [l,r]
        lfind = ints.bisect_key_left(l)
        rfind = ints.bisect_key_right(r) - 1
        # add a lefter interval
        if lfind > 0:
            if ints[lfind - 1].r >= l:
                lfind -= 1
        return lfind, rfind

    def get_super(self, l, r):
        """ return index of interval on `self` in which the [l,r] fully contained"""
        ints = self.ints 
        lfind = ints.bisect_key_right(l) - 1
        if ints[lfind].r >= r:
            return lfind
        return -1

    def add(self, l, r):
        """ add interval [l,r],
        automatically merge exactly adjacent interval
            eg. interval_union `[1,2],[4,10]`, add `[3,3]` it becomes `[1,10]`
        then return the merged interval
        """
        ints = self.ints 
        lfind, rfind = self.get_overlap(l, r)
        # if a righter interval can merge with [l,r]
        if rfind < len(ints) - 1:
            rr = ints[rfind + 1]
            if rr.l == r + 1:
                r = rr.r
                ints.pop(rfind + 1)

        # if `self` exist overlaping intervals, merge into [l,r]
        if lfind <= rfind:
            l = min(l, ints[lfind].l)
            r = max(r, ints[rfind].r)
            for _ in range(rfind - lfind + 1):
                ints.pop(lfind)
                # rfind is invalid then

        # if a lefter interval can merge with [l,r]
        if lfind > 0:
            ll = ints[lfind - 1]
            if ll.r == l - 1:
                l = ll.l
                ints.pop(lfind - 1)

        new = Interval(l, r)
        ints.add(new)
        return new

    def remove_point(self, x):
        """ remove_point `x` and break interval into less than 2 intervals at point x """
        # the rightmost interval with left endpoint <= x
        ints = self.ints 
        find = ints.bisect_key_right(x) - 1
        if find == -1: return
        tar = ints[find]
        if tar.r >= x:
            ints.pop(find)
            if tar.l != tar.r:
                if tar.l != x:
                    ints.add(Interval(tar.l, x - 1))
                if tar.r != x:
                    ints.add(Interval(x + 1, tar.r))

    def remove(self, l, r):
        """ remove all intervals fully contained in [l,r], split intervals overlap only
        """
        ints = self.ints 
        # find all intervals that left endpoint in [l,r]
        lfind = ints.bisect_key_left(l)
        rfind = ints.bisect_key_right(r) - 1
        # shorten the interval at rfind
        if rfind < len(ints):
            right = ints[rfind]
            if right.r > r:
                right.l = r+1
                rfind -= 1
        # shorten a lefter interval
        if lfind > 0:
            ll = ints[lfind-1]
            if ll.r >= l:
                ll.r = l-1
        # now ints[lfind : rfind+1] is fully contained in [l:r]
        if lfind <= rfind:
            for _ in range(rfind-lfind+1):
                ints.pop(lfind)

    def __len__(self): return len(self.ints)


class ChthollyTree:
    """ 
        des: 
            flattened segment tree(similar to 1d quadtree, dynamically open and delete point), every node stored in a sortedlist 
            base idea: after rather small times of assign function on random interval, the size of `self.A` become lg(n)
        example: ChthollyTree([10,20,30]), then self.nodes is {0:10, 1:20, 2:30}, only store left endpoints, it's enough to represent all the three intervals
        app: huge of random assign operations
        time complexity: O(nlg(lg(n))) on random data
        testOJ: @cf#896C(TLE) https://codeforces.com/contest/896/submission/142823477
    """
    def __init__(self, A): 
        self.lpts = SortedDict(enumerate(A))
        # add a sentry
        self.lpts[len(A)] = 0
    
    def split(self, x):
        """ split the interval@[l,r] contains x into two part, [l,x-1](if not empty), [x,r]
        return index of interval [x,r]
        """
        # assert 0<=x<=n
        lpts = self.lpts
        find = lpts.bisect_right(x)-1
        int_l, int_v = lpts.peekitem(find)
        if int_l != x:
            lpts[x] = int_v
            find += 1
        return find

    def addition(self, l, r, v):
        """ des: increase all points in [l,r] by value v """
        # assert 0<=l<=r<n
        lpts = self.lpts
        lfind = self.split(l)
        rfind = self.split(r+1)
        for k in lpts.keys()[lfind:rfind]:
            lpts[k] += v
        
    def assign(self, l, r, v):
        """ des: assign all points in [l,r] by value v, then merge the interval included in [l,r] """
        # assert 0<=l<=r<n
        lpts = self.lpts
        lfind = self.split(l)
        rfind = self.split(r+1)
        for _ in range(rfind-lfind-1):
            lpts.popitem(lfind+1)
        lpts[l] = v

    def traverse(self, l, r):
        """ yield all values in [l,r] in format: (value, numberofvalue) """
        # assert 0<=l<=r<n
        lpts = self.lpts
        # find all intervals that left endpoint in [l,r]
        lfind = lpts.bisect_left(l)
        rfind = lpts.bisect_right(r) 
        if lfind >= rfind:
            yield lpts.peekitem(lfind-1)[1], r-l+1
            return
        ints =  lpts.items()[lfind:rfind]
        if lfind>0:
            _, ll_val = lpts.peekitem(lfind-1)
            yield ll_val, ints[0][0]-l
        
        for i_ints in range(len(ints)-1):
            int_l, int_v = ints[i_ints]
            yield int_v, ints[i_ints+1][0]-int_l
        yield ints[-1][1], r-ints[-1][0]+1


class ChthollyTreeList:
    """ 
        des: 
            flattened segment tree(similar to 1d quadtree, dynamically open and delete point), every node stored in an arraylist without order
            base idea: after rather small times of assign function on random interval, the size of `self.A` become lg(n)
        example: ChthollyTree([10,20,30]), then self.nodes is {0:10, 1:20, 2:30}, only store left endpoints, it's enough to represent all the three intervals
        app: huge of random assign operations
        time complexity: 
            O(nlgn) on random data
        compare: slightly faster than ChthollyTree which is far complex than list impl
        testOJ: @cf#896C(TLE) https://codeforces.com/contest/896/submission/145106218
    """
    def __init__(self, A): 
        self.A = [Interval(i,i,v) for i,v in enumerate(A)]
    
    def split(self, l, r):
        """ ensure there is an interval start at l and an interval end at r
        i.e. there won't be partially overlap relationship between intervals in A and [l,r]
        """
        # assert 0<=x<=n
        A = self.A
        l_flg = r_flg = 1
        
        for intvl in A:
            # for(int i=0;i<len(A);i++)
            if intvl.l == l: l_flg = 0
            if intvl.r == r: r_flg = 0
            if l_flg + r_flg == 0: break
            
            if l_flg and intvl.l < l  and l <= intvl.r:
                A.append(Interval(l, intvl.r, intvl.val))
                intvl.r = l-1
                l_flg = 0
            
            if r_flg and intvl.l <= r and r < intvl.r:
                A.append(Interval(intvl.l, r, intvl.val))
                intvl.l = r+1
                r_flg = 0  

    def addition(self, l, r, v):
        """ des: increase all points in [l,r] by value v """
        # assert 0<=l<=r<n
        self.split(l,r)
        for intvl in self.A:
            if l<=intvl.l and intvl.r <= r:
                intvl.val += v
        
        
    def assign(self, l, r, v):
        """ des: assign all points in [l,r] by value v, then merge the interval included in [l,r] """
        # assert 0<=l<=r<n
        self.split(l,r)
        # print(self.A,'bef',l,r,v)
        newA = [Interval(l,r,v)]
        for intvl in self.A:
            if intvl.l<l or intvl.r>r:
                newA.append(intvl)
        self.A = newA
        # print(newA,'aft')

    def traverse(self, l, r):
        """ 
        the traverse is unordered
        yield all values in [l,r] in format: (value, numberofvalue) """
        # assert 0<=l<=r<n
        A = self.A
        ret = []
        for intvl in A:
            # if overlap
            if l<=intvl.r and intvl.l <= r:
                # if intvl contained in [l,r]
                if l<=intvl.l and intvl.r<=r:
                    ret.append((intvl.val, intvl.r-intvl.l+1))
                # overlap on the intvl right
                elif l<intvl.l:
                    ret.append((intvl.val, r-intvl.l+1))
                # overlap on the intvl left
                elif intvl.r<r:
                    ret.append((intvl.val, intvl.r-l+1))
                # if [l,r] contained in intvl
                else:
                    ret.append((intvl.val, r-l+1))
                    break
        return ret
            

if __name__ == "__main__":
    def test_SortedIntervals_1():
        tree = SortedIntervals()
        tree.add(1, 1)
        tree.remove_point(0)
        tree.remove_point(1)
        tree.add(-100, 100)
        tree.remove_point(23)
        tree.remove_point(24)
        tree.remove_point(25)
        tree.remove_point(100)
        tree.remove_point(1022)
        tree.add(239, 10000)
        tree.add(24, 30)
        tree.add(24, 3000)
        assert [(x.l, x.r) for x in tree.ints] == [(-100,22), (24,10000)]
    
    n = 10000
    A = [randint(-100000, 100000) for _ in range(n)]
    def test_ChthollyTree_1():
        tree = ChthollyTree(A)
        for _ in range(1000):
            op = randrange(3)
            l, r = sorted([randrange(n), randrange(n)])
            v = randint(-100000, 100000)
            if op == 0:
                iA = l
                for v,c in tree.traverse(l, r):
                    # pass
                    for _ in range(c):
                        assert iA<len(A), "traverse yield wrong value number"
                        assert A[iA] == v, "traverse yield wrong value"
                        iA += 1
            elif op == 1:
                tree.assign(l, r, v)
                for i in range(l, r+1): A[i]=v
            else:
                tree.addition(l, r, v)
                for i in range(l, r+1): A[i]+=v
        print("final interval number",len(tree.lpts))

    
    def test_ChthollyTreeList_2():
        tree = ChthollyTreeList(A)
        for _ in range(1000):
            op = choice([0,1,2])
            l, r = sorted([randrange(n), randrange(n)])
            v = randint(-100000, 100000)
            if op == 0:
                C = Counter()
                for v,c in tree.traverse(l, r):
                    C[v] += c
                
                for i in range(l,r+1):
                    C[A[i]]-=1
                assert all(v==0 for v in C.values()), (A,C,l,r,tree.A)
            elif op == 1:
                tree.assign(l, r, v)
                for i in range(l, r+1): A[i]=v
            else:
                tree.addition(l, r, v)
                for i in range(l, r+1): A[i]+=v
        print("final interval number",len(tree.A))

    test_SortedIntervals_1()
    from timeit import default_timer as time
    sta = time()
    test_ChthollyTree_1()
    # test_ChthollyTreeList_1()
    test_ChthollyTreeList_2()
    print(time()-sta)