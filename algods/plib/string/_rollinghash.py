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

Mod = random.choice(bigprimes63)
radix = 26 # #alphabetic
def val(v): return v

class RHS:
    """ rollinghash for a deque ( also hash its size ) """
    __slots__ = 'v','n'
    def __init__(self, n=0, v=0):
        self.v, self.n = v,n
    def reset(self): self.v = self.n = 0
    def append(self, e: int): 
        self.v = (radix*self.v + e)%Mod
        self.n += 1
    def pop(self, e: int): 
        self.v = ((self.v-e)*pow(radix,-1,Mod))%Mod
        self.n -= 1
    def popleft(self, e: int): 
        self.v = (self.v-e*pow(radix,self.n-1,Mod))%Mod
        self.n -= 1
    def appendleft(self, e: int): 
        self.v = (self.v+e*pow(radix,self.n,Mod))%Mod
        self.n += 1
    def __sub__(self, left): 
        """ difference of prefixes to get rollinghash of an interval """
        return (self.v - left.v*pow(radix,self.n-left.n,Mod))%Mod
    def __eq__(self, oth): return self.v==oth.v and self.n==oth.n
    def __hash__(self): return hash((self.v, self.n))
    def __repr__(self): return f"RHS{self.n, self.v}"

def rhs_prefix(A):
    """ for prefixes: generate list of RHS object """
    n = len(A)
    pre = [None]*(n+1)
    pre[0] = RHS(0, 0)
    for i in range(n):
        pre[i+1] = copy.copy(pre[i])
        pre[i+1].append(val(A[i]))
    return pre


def rhs_iterable(A):
    """ for an iterable """
    hs = 0
    for ri in range(len(A)):
        hs = (radix*hs + val(A[ri]))%Mod
    return hs

def rhs_slidingwindow(A, sz):
    """ all fixsize subarray of an iterable """
    ns = len(A)
    if ns<sz: return
    pbsz = pow(radix, sz, Mod) # radix**sz
    hs = 0
    for ri in range(sz):
        hs = (radix*hs + val(A[ri]))%Mod
    yield 0,hs
    for ri in range(sz,ns):
        li = ri - sz + 1
        hs = (radix*hs + val(A[ri]))%Mod
        hs = (hs-val(A[li-1])*pbsz)%Mod
        yield li,hs

def rhs_multiset():
    """ assume A[i] is integer
    refer:
        cpython
        https://github.com/python/cpython/blob/06e1701ad3956352bc0f42b8f51c2f8cc85bf378/Objects/setobject.c#L686
    ret: uint64 
    rolling hash: the value of `base` can be calculate with sliding window
    """
    def _shuffle_bits(h):
        """ Work to increase the bit dispersion for closely spaced hash values.
        This is important because some use cases have many combinations of a
        small number of elements with nearby hashes so that many distinct
        combinations collapse to only a handful of distinct hash values. """
        return ((h ^ 89869747) ^ (h << 16)) * 3644798167

    def base(A):
        """ this part could be "rolling" """
        hs = 0
        for v in A:
            hs^=_shuffle_bits(v)
        return hs

    def gethash(A):
        hs = base(A)
        hs ^= (len(A)+1)*1927868237
        hs &= (hs>>11)^(hs>>25)
        # truncate use 64 bit
        hs = (hs * 69069 + 907133923)&(2**64-1)
        return hs


if __name__ == "__main__":
    # hash collision case1 https://codeforces.com/blog/entry/4898
    s = deque([0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1,0,1,2,1,2,1,0,1,0,1,2,1,2,1,0,1,2,1,0,1,0,1,2,1])
    
    tmp1 = rhs_iterable(s)
    s.rotate(1)
    assert tmp1 != rhs_iterable(s)

    pre = rhs_prefix([0,1,2,1,2])
    print(pre)