"""
collection of some O(n) patterns, instead of copy from those code, recite and dictate is faster
TOC
    groupby
"""
from typing import *
import itertools
from math import *

def groupby(A:Iterable):
    """ group A by its value
    can also be used to split string
    performance: slower than `itertools.groupby`
    """
    n = len(A)
    i = 0
    for j in range(1, n+1):
        if j==n or A[i]!=A[j]:
            yield i,j
            i = j

def discretize(A):
    """
    put all values of A into number axis
    return a mapper that map value of A into its rank(start of 0) on numebr axis
    """
    pv = None
    uuid = 0
    mapper = {}
    for v in sorted(A):
        if v == pv: continue
        mapper[v] = uuid; uuid += 1
        pv = v
    return mapper