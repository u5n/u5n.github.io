from collections import deque
from copy import copy
import random
"""
linear congruential generator + cyclic polynomial
 key: 
    1. randomize parameter
    2. `mod` should be prime and as larger as possible 
    3. after AC, try different parameters
 
 `mod`: 
    https://primes.utm.edu/lists/2small/100bit.html
    128 bit candidate 2**128-x, x\in [159, 173, 233, 237, 275, 357, 675, 713, 797, 1193]
    64 bit candidate 2**64-x, x\in [59, 83, 95, 179, 189, 257, 279, 323, 353, 363]
    32 bit candidate 2**32-x, x\in [5, 17, 65, 99, 107, 135, 153, 185, 209, 267 ]

"""
prime64bit = [2**64-x for x in [59, 83, 95, 179, 189, 257, 279, 323, 353, 363]]
prime32bit = [2**32-x for x in [5, 17, 65, 99, 107, 135, 153, 185, 209, 267 ]]
prime128bit = [2**128-x for x in [159, 173, 233, 237, 275, 357, 675, 713, 797, 1193]]
# https://primes.utm.edu/curios/index.php?stop=1
bigprimes = [10**600+543, 10**776 + 1777,3*10**910-1,10**1000-8202269, 4*10**1473+1 ,10**1748+1] 
# def val(v): return ord(v)-ord('a')
def val(v): return v

class RHS:
    """
    only for variable length
    """
    __slots__ = 'v','n','mod','base'
    def __init__(self,base,mod,s=''):
        self.mod = mod
        self.base=base
        self.v = self.n = 0
        for c in s: self.append(c)
    def reset(self): self.v = self.n = 0
    def append(self, c): 
        self.v = (self.base*self.v + val(c))%self.mod
        self.n += 1
    def pop(self, c): 
        self.v = ((self.v-val(c))*pow(self.a,-1,self.mod))%self.mod
        self.n -= 1
    def popleft(self, c): 
        self.v = (self.v-val(c)*pow(self.a,self.n-1,self.mod))%self.mod
        self.n -= 1
    def appendleft(self, c): 
        self.v = (self.v+val(c)*pow(self.a,self.n,self.mod))%self.mod
        self.n += 1
    def subprefix(self, pre): 
        return (self.v - pre.v*pow(self.a,self.n-pre.n,self.mod))%self.mod
    def __eq__(self, oth): return self.v==oth.v and self.n==oth.n
    def __hash__(self): return hash(self.v, self.n)

# generate list of RHS object of prefixes
def rhs_prefix(s):
    n = len(s)
    hs = RHS()
    pre = [None]*(n+1); pre[0] = copy(hs)
    for i in range(n):
        hs.append(s[i])
        pre[i+1] = copy(hs)
    return pre

# for fixed size RHS
def rhs_fixsize(s, sz, base, mod):
    ns = len(s)
    if ns<sz: return
    pasz = pow(base, sz, mod)
    hs = 0
    for ri in range(sz):
        hs = (base*hs + val(s[ri]))%mod
    yield hs
    for ri in range(sz,ns):
        li = ri - sz + 1
        hs = (base*hs + val(s[ri]))%mod
        hs = (hs-val(s[li-1])*pasz)%mod
        yield hs

if __name__ == "__main__":
    # case1 https://codeforces.com/blog/entry/4898
    s = deque([0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1])
    mod = random.choice(prime128bit)
    base = random.choice(prime32bit)
    tmp1 = RHS(base,mod,s).v
    s.rotate(1)
    assert tmp1 != RHS(base,mod,s).v
    