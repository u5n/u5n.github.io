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

def divisor(x):
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

# single point euler totient function
def euler_totient(x):
    ret = x
    for p,_ in prime_factor(x):
        ret=ret//p*(p-1)
    return ret