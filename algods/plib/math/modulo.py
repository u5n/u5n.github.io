"""
TOC
    combCache
    solve_linear_congruence
    extgcd
    chinese_remainder_theorem
    {single point calculation}
        modular_multiplication_inverse
        is_prime
        factors
        prime_factors
        prime_factors_exp
        euler_totient

"""
from functools import reduce
from math import gcd, isqrt
from operator import *
from typing import List
from itertools import count

class combCache:
    def __init__(self, mod, maxn):
        self.mod = mod
        self.fac = fac = [1]*(maxn)
        self.invfac = invfac = [1]*(maxn)
        self.inv = inv = [1]*(maxn)
    
        for i in range(2, maxn):
            inv[i] = inv[mod%i]*(-mod/i)%mod
            fac[i]=fac[i-1]*i%mod
            invfac[i]=invfac[i-1]*inv[i]
        
    def perm(self, n, r):        
        assert n>=0
        if r<0 or n<r: return 0
        return self.fac[n]*self.invfac[n-r]%self.mod
        
    def comb(self, n, r):
        return self.perm(n,r)*self.invfac[r]%self.mod
    
    
def trunc_div(a, b):
    """ integer division, quotient truncated towards zero, as same as c++  """
    q, r = divmod(a,b)
    if q < 0 and r: q += 1
    return q

def extgcd(a, b):
    """
    solve equation `ax + by = gcd(a,b)`
        x = ps + k*b//d
        y = pt - k*a//d
        ps * a + pt * b  = abs(pr) = gcd(a,b)
    """
    ps,s =1,0
    pt,t =0,1
    while b:
        quo = trunc_div(a, b)
        a,b=b,a-quo*b
        ps,s=s,ps-quo*s
        pt,t=t,pt-quo*t
    return a, ps, pt

def solve_linear_congruences(a,b,m):
    """ solve equation ax ≡ b (mod m) && 0<=x<m
    i.e. ax+my = b
    """
    d = gcd(a,m)
    if b%d!=0: return 
    _,x0,_ = extgcd(a,m)
    x0*=b//d
    # if l==1: min(x0%m, (x0+m//d)%m) is the minimum solution that >= 0
    for _ in range(d):
        yield x0%m
        x0 += m//d

def chinese_remainder_theorem(A:List[int], mods:List[int]) -> int:
    """ 
    M[i] is prime
    solve equation of x: 
        x ≡ A[i] mod M[i] for all i
    """
    P = reduce(mul, mods)
    M = [P//mod for mod in mods]
    T = list(pow(Mi, -1, mi) for Mi,mi in zip(M, mods))
    return sum(Ai*Ti*Mi for Ai,Ti,Mi in zip(A,T,M))%P


def modular_multiplication_inverse(a, Mod):
    assert gcd(a, Mod)==1
    return extgcd(a, Mod)[1]%Mod



