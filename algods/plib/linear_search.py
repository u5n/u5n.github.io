"""
TOC
    groupby
"""
from collections import defaultdict
from typing import *
from math import *


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

if __name__ == "__main__":
    pass