from typing import *
from itertools import count
"""
TOC:
    is_pal
    tra_pal10
"""
    
def is_pal(A: Iterable):
    """ judge palindromic of arraylist without create a copy """
    l,r = 0,len(A)-1
    while l<r:
        if A[l]!=A[r]: return False
        l+=1; r-=1
    return True

min_d10 = [0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000, 100000000000]
def tra_pal10() -> int:
    """ traverse base 10 palindromes in accending order """
    for d_lhf in count(1):
        # d_lhr is the left half(if odd, include median) of palindromic number
        # odd length
        for lhf in range(min_d10[d_lhf], min_d10[1+d_lhf]):
            # d_pal = d_lhf*2-1
            slhf = str(lhf)
            yield int(slhf + slhf[-2::-1])
        # even length
        for lhf in range(min_d10[d_lhf], min_d10[1+d_lhf]):
            # d_pal = d_lhf*2
            slhf = str(lhf)
            yield int(slhf + slhf[::-1])