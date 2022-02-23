from math import *
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