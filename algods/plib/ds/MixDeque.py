"""
tutorial: https://cp-algorithms.com/data_structures/stack_queue_modification.html#queue-modification-method-3
"""
from math import *

class MixStack:
    """ deque support find `reduce(monoid_opt, list(self))` in armotized O(1) """
    __slots__ = 'arr', 'monoid'
    def __init__(self, monoid): 
        self.arr, self.monoid = [], monoid
    def pop(self): return self.arr.pop()[0]
    def append(self, v):
        if len(self.arr)==0:
            self.arr.append((v,v))
        else:
            self.arr.append((v, self.monoid(self.arr[-1][1], v)))
    def top(self): return self.arr[-1][0]
    def getmix(self): return self.arr[-1][1]
    def __len__(self): return len(self.arr)
    def __str__(self): return f"MixStack({[v for v,m in self.arr]}, monoid={self.monoid})"

class MixDeque:
    """ 
    des:
        deque support find `reduce(monoid_opt, list(self))` in armotized O(1) 
    test:
        @lc#
    """
    __slots__ = 'lsta', 'rsta', 'monoid'
    def __init__(self, monoid):
        self.lsta, self.rsta, self.monoid = MixStack(monoid), MixStack(monoid), monoid
    def append(self, v):
        self.rsta.append(v)
    def pop(self):
        if not self.rsta: self.split(0)
        return self.rsta.pop()
        
    def appendleft(self, v):
        self.lsta.append(v)

    def popleft(self):
        if not self.lsta: self.split(1)
        return self.lsta.pop()

    def getmix(self):
        if not self.lsta or not self.rsta:
            return self.rsta.getmix() if not self.lsta else self.lsta.getmix()
        return self.monoid(self.lsta.getmix(), self.rsta.getmix()) 

    def split(self, right):
        """ right==1 means split self.rsta """
        tmp = self.rsta.arr if right else self.lsta.arr
        n = len(tmp)
        if n==0: raise IndexError("pop/query an empty deque")
        self.lsta = MixStack(self.monoid)
        self.rsta = MixStack(self.monoid)
        if right:            
            for i in range(n//2+1,n): self.rsta.append(tmp[i][0])
            for i in range(n//2,0-1,-1): self.lsta.append(tmp[i][0])
        else:
            for i in range(ceil(n/2),n): self.lsta.append(tmp[i][0])
            for i in range(ceil(n/2)-1,0-1,-1): self.rsta.append(tmp[i][0])
    
    def __repr__(self):
        return f"MixQueue({ [v for v,m in self.lsta.arr], [v for v,m in self.rsta.arr] }, monoid={self.monoid})"
