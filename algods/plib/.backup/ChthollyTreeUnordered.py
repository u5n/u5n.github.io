"""
seems that this is useless
"""
from collections import Counter
class Interval:
    __slots__ = 'l', 'r', 'val'
    def __init__(self, l, r, val=None):
        self.l, self.r, self.val = l, r, val
    def __repr__(s): return f"Interval({s.l},{s.r},{s.val})"
class ChthollyTreeUnordered:
    """ 
        des: 
            flattened segment tree(similar to 1d quadtree, dynamically open and delete point)
            base idea: after rather small times of assign function on random interval, the size of `self.A` become $lg(n)$
            impl: every node stored in an arraylist without order; because of unordered, need to store right endpoint of each interval
        app: huge of random assign operations
        time complexity: 
            O(nlgn) with n random opeartions
        compare: slightly faster than ChthollyTree which is far complex than list impl
        testOJ: @cf#896C https://codeforces.com/contest/896/submission/148760320
    """
    def __init__(self, A): 
        self.A = [Interval(i,i,v) for i,v in enumerate(A)]
    
    def split(self, l, r):
        """ this function ensure there is an interval start at l and an interval end at r
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
        
    def get_point(self, x):
        A = self.A
        for intvl in A:
            if intvl.l <= x <=intvl.r:
                return intvl.val
        return None


if __name__ == "__main__":
    from random import *
    n = 10000
    A = [randint(-100000, 100000) for _ in range(n)]
    def test_ChthollyTreeList():
        tree = ChthollyTreeUnordered(A)
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

    from timeit import default_timer as time
    sta = time()
    test_ChthollyTreeList()
    print(time()-sta)