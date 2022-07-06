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

def unique_sorted(A:list):
    """ A is sorted """
    return [v for v,g in itertools.groupby(A)]


