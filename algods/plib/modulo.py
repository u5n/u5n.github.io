"""
TOC
    _combinatorial_cache
        fac;invfac;inv;perm;comb
    solve_linear_congruence
    extended_gcd
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

def _combinatorial_cache(Mod, maxn):
    fac = [1]*(maxn+1)
    invfac = [1]*(maxn+1)
    # inv = [1]*(maxn+1)
    for i in range(2,maxn+1):
        fac[i]=fac[i-1]*i%Mod
        invfac[i]=pow(fac[i], -1, Mod)
        
        # inv[i]=Mod-((Mod//i)*inv[Mod%i])%Mod
    def perm(n, r):
        return fac[n]*invfac[n-r]%Mod
    def comb(n, r):
        return perm(n,r)*invfac[r]%Mod

def extended_gcd(a,b):
    """
    old_s * a + old_t * b  = abs(old_r) = gcd(a,b)
    solve equation `ax + by = gcd(a,b)`
        x = old_s + k*b//d
        y = old_t - k*a//d
    """
    old_r,r =a,b
    old_s,s =1,0
    old_t,t =0,1
    while r:
        quo = old_r//r # floored division
        old_r,r=r,old_r-quo*r
        old_s,s=s,old_s-quo*s
        old_t,t=t,old_t-quo*t
    return old_s, old_t

def solve_linear_congruences(a,b,m):
    """ solve equation ax ≡ b (mod m) && 0<=x<m
    i.e. ax+my = b
    """
    d = gcd(a,m)
    if b%d!=0: return 
    x0,_ = extended_gcd(a,m)
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
    def modular_multiplication_inverse(a, Mod):
        assert gcd(a, Mod)==1
        return extended_gcd(a, Mod)[0]%Mod
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
        for i in range(isqrt(x)+1):
            if x%i==0:
                yield i
                if i*i!=x:
                    yield x//i
    def prime_factors(x):
        i = 2
        while i*i <= x:
            if x%i==0:
                while x%i==0:
                    x//=i
                yield i
            i+=1
        if x>1: yield x
    
    # prime factors in order, with exponent 
    def prime_factors_exp(x):
        i = 2
        while i*i <= x:
            cnt = 0
            while x%i == 0:
                x//=i
                cnt += 1
            if cnt!=0: 
                yield i,cnt
            i+=1
        if x>1: yield x,1

    # euler totient function
    def euler_totient(x):
        ret = x
        for p in prime_factors(x):
            ret=ret//p*(p-1)
        return ret
