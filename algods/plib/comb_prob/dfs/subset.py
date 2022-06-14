"""
glossary:
    distinct by value:
        the classic model divide n labeled object into k unlabled groups
        but some object are same, especially when it's string of a limited alphabetic.
"""

from functools import *

def subsetsum_distinct(A, l, r):
    """ return list of sum of subset of A[l:r] , order by sum asc
    this is useful in meed-in-middle problems
    impl: bfs
    time: O(2^(r-l))
    """
    ret = {0}
    for i in range(l, r):
        ret |= {v+A[i] for v in ret}
    return sorted(ret)

def subset_distinct(s: str):
    """ divide chars in `s` into two labeled group, return the all kinds of the first groups 
    time: O(2^n) """
    n = len(s)
    ret = []
    @cache
    def dfs(i, s1):
        if i == n: 
            ret.append(s1)
            return
        dfs(i+1, s1+s[i])
        dfs(i+1, s1)
    dfs(0, '')
    return ret

def disjoint_two_subset_distinct(s:str):
    """ des: divide chars in `s` into three labeled group@[g1,g2,g3], return all kinds of pairs (g1,g2) and additionally g1<=g2 
    time: O(3^n)
    performance:  magnitude faster than bitmask
    """
    n = len(s)
    ret = []
    @cache
    def dfs(i, s1, s2):
        if s1 > s2:
            dfs(i, s2, s1)
            return 
        if i==n: 
            ret.append((s1, s2))
            return
        
        dfs(i+1, s1+s[i], s2)
        dfs(i+1, s1, s2+s[i])
        dfs(i+1, s1, s2)
    dfs(0, '', '')
    return ret