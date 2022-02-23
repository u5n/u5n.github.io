"""
TOC
    des: queue support extract min/max, impl by a element asc/desc stack
    code:
        nearest_leftandright
        nearest
        MonoQueue
        MonoQueueVal    
"""
import operator
from collections import deque
from math import *

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
    return left, right

def nearest_larger(A, opt=operator.gt):
    """ 
    paras: opt: example: `[opeartor.lt, opeartor.gt, opeartor.ge, operator.le]`
    des:
        yield i0, i1, i2 for index i1 in `A`
            def cmp(i, j):
                if 0!=opt(A[i], A[j]): opt(A[i], A[j])
                if opt(0, 0):
                    return i-j # if A[j], A[i] equal, smaller index's cmp is larger
                return j-i # if A[i] A[j] equal, larger index's cmp is larger
                
            i0 is largest index(i0<i1) that cmp(i0, i1)==1
            i2 is smallest index(i2>i1) that cmp(i2, i1)==1
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
    des: monoqueue on an streaming, additionaly store the value
    appliation:
        max queue: opt=operator.le
        min queue: opt=operator.ge
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