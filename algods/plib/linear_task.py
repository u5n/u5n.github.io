"""
collection of some O(n) patterns, instead of copy from those code, recite and dictate is faster
TOC
    groupby
"""
from typing import *
from math import *

def groupby(A:Iterable):
    """ group A by its value
    can also be used to split string
    """
    n = len(A)
    i = 0
    for j in range(1, n+1):
        if j==n or A[i]!=A[j]:
            yield i,j
            i = j

def template_discretization(A):
    SA = sorted(A)
    # map A[i] to its rank in SA
    v_rk = {}; v_rk_i = 0
    for v in SA:
        if v not in v_rk:
            v_rk[v] = v_rk_i; v_rk_i += 1
    

def template_unique(A: list): 
    # unique use hashtable(require element hashable)
    list(Counter(A))

class InarrayQueue:
    """ abstract of one usage of monotonic pointers"""
    def __init__(self, A): self.p, self.n, self.A = 0,len(A), A
    def __len__(self): return self.n - self.p
    def popleft(self): self.p += 1; return self.A[self.p-1]
    
if __name__ == "__main__":
    pass