"""
TOC
    {monoqueue}
        des: queue support extract min/max, impl by an asc/desc stack
        code:
            nearest_leftandright
            nearest
            MonoQueue
            MonoQueueVal
    
"""
from collections import defaultdict, deque
from math import *

class _namespace_monoqueue:
    @staticmethod
    def nearest_leftandright(A, opt):
        """ for A[r], left[r] is largest index(<r) that opt(A[left[r]], A[r])
        for A[l], right[l] is smallest index(>l) that not opt(A[l], A[right[l]])
        """
        n = len(A)
        left = [None]*n
        right = [n]*n
        sta = [-1]
        for i, e in enumerate(A):
            while len(sta)>1 and not opt(A[sta[-1]], e):
                t = sta.pop()
                right[t] = i
            left[i] = sta[-1]
            sta.append(i)
    
    @staticmethod
    def nearest_larger(A, opt):
        """ yield i0, i1, i2 
        paras: opt: examples: `[opeartor.lt, opeartor.gt, opeartor.ge, operator.le]`
        usage:
            i0 is largest i(i0<i1) that cmp(i0, i1)==1
            i2 is smallest i(i0>i1) that cmp(i2, i1)==1
            def cmp(i, j):
                if 0!=opt(A[i], A[j]): opt(A[i], A[j])
                if opt(0, 0):
                    return i-j # if A[j], A[i] equal smaller index its cmp is larger
                return j-i # if A[i] A[j] equal larger index its cmp is larger
        """
        n = len(A)
        sta = [-1]
        for i in range(n+1):
            while len(sta)>1 and (i==n or not opt(A[sta[-1]], A[i])):
                yield sta[-2], sta[-1], i
                sta.pop()
            sta.append(i)

    class MonoQueue:
        """  
        des: 
            monoqueue on an arraylist, store its indices
            use it like a sliding window
        application: 
            max queue: 
                opt=operator.le
                    if equal, select rightmost
                opt=operator.lt
                    if equal, select leftmost
            min queue: opt=operator.ge
            it's an encapsulated data structure, don't use it to find nearest left/right element that ...
        """
        def __init__(self, A, opt):
            self.q = deque()
            self.l=self.r=0
            self.A = A
            self.opt = opt
        def append(self):
            while self.q and self.opt(self.A[self.q[-1]], self.A[self.r]):
                self.q.pop()
            self.q.append(self.r)
            self.r+=1
        def popleft(self):
            if self.q[0]==self.l:
                self.q.popleft()
            self.l += 1
        def get(self):
            return self.q[0]

    class MonoQueueVal: 
        """  
        des: monoqueue on an streaming, store the value
        appliation:
            max queue: opt=operator.le
            min queue: opt=operator.ge
            it's an encapsulated data structure, don't use it to find nearest left/right element that ...
        """
        def __init__(self, opt):
            self.q = deque()
            self.l=self.r=0
            self.opt = opt
        def append(self, v):
            while self.q and self.opt(self.q[-1][0], v):
                self.q.pop()
            self.q.append((v,self.r))
            self.r+=1
        def popleft(self):
            if self.q[0][1]==self.l:
                self.q.popleft()
            self.l += 1
        def get(self):
            return self.q[0][0]

class MinDeque:
    """ deque support find min """
    def __init__(self):
        self.lsta, self.rsta = MinStack(),MinStack()
    def append(self, v):
        self.rsta.append(v)
    def pop(self):
        if not self.rsta: self.split(1)
        return self.rsta.pop()
    def appendleft(self, v):
        self.lsta.append(v)
    def popleft(self):
        if not self.lsta: self.split(0)
        return self.lsta.pop()
    def getMin(self):
        if not self.lsta or not self.rsta:
            return self.rsta.getMin() if not self.lsta else self.lsta.getMin()
        return min(self.lsta.getMin(), self.rsta.getMin()) 

    def split(self, left):
        """ left=1 means split self.lsta """
        n = len(self.lsta)
        if n==0: raise IndexError("pop/query an empty deque")
        tmp = self.lsta.arr
        self.lsta = MinStack()
        self.rsta = MinStack()
        if left:
            for i in range(ceil(n/2),n): self.lsta.append(tmp[i][0])
            for i in range(ceil(n/2)-1,0-1,-1): self.rsta.append(tmp[i][0])
        else:
            for i in range(n//2+1,n): self.rsta.append(tmp[i][0])
            for i in range(n//2,0-1,-1): self.lsta.append(tmp[i][0])        

class MinStack:
    """ stack support find min """
    def __init__(self): self.arr = []
    def pop(self): return self.arr.pop()[0]
    def append(self, v):
        if len(self.arr)==0:
            self.arr.append((v,v))
        else:
            self.arr.append((v, min(self.arr[-1][1], v)))
    def top(self): return self.arr[-1][0]
    def getMin(self): return self.arr[-1][1]
    def len(self): return len(self.arr)