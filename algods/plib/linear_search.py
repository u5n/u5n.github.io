"""
TOC
    groupby
    parition
    _ilog2_cache
    countsort
    {palindrome related}
"""
from collections import defaultdict
from typing import *
import random
from math import *
import builtins
import heapq


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

def partition(A, l, r):
    """ inplace, not stable """
    pivot = A[random.randrange(l,r)]
    i = l
    for j in range(l, r):
        # loop inv: A[l:i] <= pivot < A[i:j]
        if A[j] <= pivot:
            A[i],A[j] = A[j],A[i]
            i+=1
    return i-1

def _ilog2_cache(maxn):
    ilog2 = [0]*(maxn+1)
    for i in range(1, maxn+1):
        ilog2[i] = ilog2[i-1] + (i%2==0)

def countsort(A, key=lambda x:x):
    """ assume key >= 0, key is int """
    maxk = max(key(e) for e in A)
    count = [0]*(1+maxk)
    for e in A: count[key(e)] += 1
    for i_count in range(1, maxk+1): count[i_count] += count[i_count-1]
    
    # sorted A
    As = [None]*len(A)
    for e in reversed(A):
        k = key(e)
        count[k] -= 1
        As[count[k]] = e
    return As

def _namespace_palindrome():
    import numpy as np
    from itertools import count
    def is_pal(A: Iterable):
        n = len(A)
        l,r = 0,n-1
        while l<r:
            if A[l]!=A[r]: return False
            l+=1
            r-=1
        return True
    min_d10 = [0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000, 100000000000]
    def tra_pal10() -> int:
        """ traverse base 10 palindromes in accending order """
        for d_lhf in count(1):
            # loop inv: d_lhr is digit of left half
            for lhf in range(min_d10[d_lhf], min_d10[1+d_lhf]):
                # d_pal = d_lhf*2-1
                slhf = str(lhf)
                yield int(slhf + slhf[-2::-1])
            for lhf in range(min_d10[d_lhf], min_d10[1+d_lhf]):
                # d_pal = d_lhf*2
                slhf = str(lhf)
                yield int(slhf + slhf[::-1])

    def int_iterable(x:int, base=10)->List[int]:
        ret = []
        while x:
            ret.append(x%base)
            x//=base
        return ret
    # the `builtins.int` function transfrom a base `base` digital string to an int (2<=base<=36)
    # the `np.base_repr` function transfrom a int to base `base` digital string (2<=base<=36)
    #     -> the `str`` function transfrom an int to base 10 digital string
if __name__ == "__main__":
    import numpy as np
    def is_pal(A):
        n = len(A)
        l,r = 0,n-1
        while l<r:
            if A[l]!=A[r]: return False
            l+=1
            r-=1
        return True
    cnt = 0
    import itertools
    for i in itertools.count(1):
        if is_pal(np.base_repr(i, base=2)):
            cnt += 1
            if cnt == 1000: print(i); break