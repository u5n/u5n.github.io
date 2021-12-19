from collections import deque
import copy 
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
# https://primes.utm.edu/curios/index.php?stop=1
# bigprimes = [10**600+543, 10**776 + 1777,3*10**910-1,10**1000-8202269, 4*10**1473+1 ,10**1748+1] 

prime16bit = [2**16-x for x in [15, 17, 39, 57, 87, 89, 99, 113, 117, 123]]
prime32bit = [2**32-x for x in [5, 17, 65, 99, 107, 135, 153, 185, 209, 267 ]]
prime64bit = [2**64-x for x in [59, 83, 95, 179, 189, 257, 279, 323, 353, 363]]
prime128bit = [2**128-x for x in [159, 173, 233, 237, 275, 357, 675, 713, 797, 1193]]

class RHS:
    """ rollinghash for deque/arraylist
    """
    __slots__ = 'v','n'
    mod = random.choice(prime128bit)
    base = random.choice(prime32bit)
    def __init__(self, n, v=0):
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

def val(v): return ord(v)-97
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
below don't need `RHS().n` attribute
""" 

mod = random.choice(prime128bit)
base = random.choice(prime32bit)

# for an iterable
def rhs_iterable(A):
    hs = 0
    for ri in range(len(A)):
        hs = (base*hs + val(A[ri]))%mod
    return hs
# for subarray of a iterable
def rhs_subarray(A):
    n = len(A)
    for l in range(n):
        hs = 0
        for r in range(l+1,n+1):
            hs = (base*hs + val(A[r-1]))%mod
            yield l,r,hs

# for fixsize subarray of a iterable
def rhs_fixsize(A, sz):
    ns = len(A)
    if ns<sz: return
    pbsz = pow(base, sz, mod) ## base**sz
    hs = 0
    for ri in range(sz):
        hs = (base*hs + val(A[ri]))%mod
    yield 0,hs
    for ri in range(sz,ns):
        li = ri - sz + 1
        hs = (base*hs + val(A[ri]))%mod
        hs = (hs-val(A[li-1])*pbsz)%mod
        yield li,hs

if __name__ == "__main__":
    # hash collision case1 https://codeforces.com/blog/entry/4898
    s = deque([0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1])
    
    tmp1 = rhs_iterable(s, RHS.base, RHS.mod)
    s.rotate(1)
    assert tmp1 != rhs_iterable(s, RHS.base, RHS.mod)

    pre = rhs_prefix("01212")
    print(pre[0].v)