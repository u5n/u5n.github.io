"""
rollinghash that map string into a big integer, than modulo a prime

key: 
    1. randomize parameter
    2. `mod` should be prime and as larger as possible 
        https://planetmath.org/goodhashtableprimes
        [53,97,193, 389,769,1543,3079,6151,12289,24593,49157,98317,196613,393241,786433,1572869,3145739,6291469,12582917,25165843,50331653,100663319,201326611,402653189,805306457,1610612741,]
"""

from collections import deque
import copy 
import random

# some big primes
# log2(bigprimes) ≈ *.5
bigprimes63 = [12904149405941903143, 13080048459073205527]
bigprimes127 = [237512715131811281324243117391942323623, 236918336221672442100866320173263025989]
bigprimes255 = [8*10**76-1]
# 2**520.37
bigprimes521 = [4444105497330673937223773278869842880510284203065791498504426852153219047296662648044831617912215156488271329563201131345294533853183999999999999999999999999]

class RHS:
    """ rollinghash for a deque ( also hash its size ) """
    __slots__ = 'v','n'
    mod = random.choice(bigprimes63)
    base = 26 # alphabetic
    def __init__(self, n=0, v=0):
        self.v, self.n = v,n
    def reset(self): self.v = self.n = 0
    def append(self, e: int): 
        self.v = (RHS.base*self.v + e)%RHS.mod
        self.n += 1
    def pop(self, e: int): 
        self.v = ((self.v-e)*pow(RHS.base,-1,RHS.mod))%RHS.mod
        self.n -= 1
    def popleft(self, e: int): 
        self.v = (self.v-e*pow(RHS.base,self.n-1,RHS.mod))%RHS.mod
        self.n -= 1
    def appendleft(self, e: int): 
        self.v = (self.v+e*pow(RHS.base,self.n,RHS.mod))%RHS.mod
        self.n += 1
    def __sub__(self, left): 
        """ difference of prefixes to get rollinghash of an interval """
        return (self.v - left.v*pow(RHS.base,self.n-left.n,RHS.mod))%RHS.mod
    def __eq__(self, oth): return self.v==oth.v and self.n==oth.n
    def __hash__(self): return hash((self.v, self.n))
    def __repr__(self): return f"RHS{self.n, self.v}"


def val(v): return v
# for prefixes: generate list of RHS object
def rhs_prefix(A):
    n = len(A)
    pre = [None]*(n+1)
    pre[0] = RHS(0, 0)
    for i in range(n):
        pre[i+1] = copy.copy(pre[i])
        pre[i+1].append(val(A[i]))
    return pre

"""
below is specific function to calculate rollinghash, (also don't need `RHS().n` attribute)
""" 
Mod = random.choice(bigprimes63)
base = 26 # #alphabetic

# for an iterable
def rhs_iterable(A):
    hs = 0
    for ri in range(len(A)):
        hs = (base*hs + val(A[ri]))%Mod
    return hs

# all subarray of an iterable
def rhs_subarray(A):
    n = len(A)
    for l in range(n):
        hs = 0
        for r in range(l+1,n+1):
            hs = (base*hs + val(A[r-1]))%Mod
            yield l,r,hs

# all fixsize subarray of an iterable
def rhs_fixsize(A, sz):
    ns = len(A)
    if ns<sz: return
    pbsz = pow(base, sz, Mod) # base**sz
    hs = 0
    for ri in range(sz):
        hs = (base*hs + val(A[ri]))%Mod
    yield 0,hs
    for ri in range(sz,ns):
        li = ri - sz + 1
        hs = (base*hs + val(A[ri]))%Mod
        hs = (hs-val(A[li-1])*pbsz)%Mod
        yield li,hs

if __name__ == "__main__":
    # hash collision case1 https://codeforces.com/blog/entry/4898
    s = deque([0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1])
    
    tmp1 = rhs_iterable(s)
    s.rotate(1)
    assert tmp1 != rhs_iterable(s)

    pre = rhs_prefix([0,1,2,1,2])
    print(pre)