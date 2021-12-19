"""
TOC
    _combinatorial_cache
        fac;invfac;inv;perm;comb
    solve_linear_congruence
    extended_gcd
    {single point calculation}
        is_prime
        factors
        prime_factors
        prime_factors_exp
        euler_totient

"""
from math import gcd, isqrt
from typing import List

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
    """ 
    solve equation ax ≡ b (mod m) && 0<=x<m
    reduce to ax+my = b
    """
    d = gcd(a,m)
    if b%d!=0: return 
    x0,_ = extended_gcd(a,m)
    x0*=b//d
    # if l==1: min(x0%m, (x0+m//d)%m) is the minimum solution that >= 0
    for _ in range(d):
        yield x0%m
        x0 += m//d

def _namespace_single_point(Mod):
    def modular_multiplication_inverse(a):
        # assert gcd(a, Mod)==1
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
