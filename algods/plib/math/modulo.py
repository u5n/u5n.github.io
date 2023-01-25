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

def combCache(mod, maxn):
    fac = [1]*(maxn)
    invfac = [1]*(maxn)
    inv = [1]*(maxn)
    
    for i in range(2,maxn):
        inv[i] = inv[mod%i]*(-mod/i)%mod
        fac[i]=fac[i-1]*i%mod
        invfac[i]=invfac[i-1]*inv[i]
        
    def perm(n, r):
        assert n>=0
        if r<0 or n<r: return 0
        return fac[n]*invfac[n-r]%mod
        
    def comb(n, r):
        return perm(n,r)*invfac[r]%mod

    
    
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


def prime_generator():
    """ infinite prime generator 
    performance: 2μs per prime (first 1000000)
    original: https://stackoverflow.com/a/10733621/7721525
    space: O(√n); where n is number of primes produced
    """
    yield 2; yield 3; yield 5; yield 7;  # original code David Eppstein, 
    sieve = {}                           #   Alex Martelli, ActiveState Recipe 2002
    ps = prime_generator()               # a separate base Primes Supply:
    p = next(ps) and next(ps)            # (3) a Prime to add to dict
    q = p*p                              # (9) its sQuare 
    for c in count(9,2):                 # the Candidate
        if c in sieve:               # c's a multiple of some base prime
            s = sieve.pop(c)         #     i.e. a composite ; or
        elif c < q:  
             yield c                 # a prime
             continue              
        else:   # (c==q):            # or the next base prime's square:
            s=count(q+2*p,2*p)       #    (9+6, by 6 : 15,21,27,33,...)
            p=next(ps)               #    (5)
            q=p*p                    #    (25)
        for m in s:                  # the next multiple 
            if m not in sieve:       # no duplicates
                break
        sieve[m] = s                 # original test entry: ideone.com/WFv4f

def _namespace_single_point(Mod):
    """
        others:
            max number of divisors: 
                evaluate:U**(1.066/log(log(U)))
                n=1000000000
                ~=1344

    """
    def modular_multiplication_inverse(a, Mod):
        assert gcd(a, Mod)==1
        return extgcd(a, Mod)[1]%Mod
    
    def is_prime(n:int):
        if n<=1: return False
        elif n<=3: return True
        elif n%2==0 or n%3==0: return False
        i = 5
        while i*i<=n:
            if n%i==0 or n%(i+2)==0:
                return False
            i+=6
        return True

    
    def factors(x):
        ret = []
        p = 1
        while p*p<x:
            if x%p==0:
                ret.append(p)
                ret.append(x//p)
            p+=1
        if p*p==x:
            ret.append(p)
        return ret

    def prime_factor(x):
        ms = Counter()
        i = 2
        while i*i <= x:
            cnt = 0
            while x%i == 0:
                x//=i
                cnt += 1
            if cnt!=0: 
                ms[i] = cnt
            i+=1
        if x>1: ms[x] = 1
        return ms

    # euler totient function
    def euler_totient(x):
        ret = x
        for p,_ in prime_factors(x).items():
            ret=ret//p*(p-1)
        return ret