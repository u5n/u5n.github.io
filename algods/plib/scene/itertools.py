"""
TOC:
    all_groups
    k_groups
    {distinct by values}
        subsetsum_distinct
        {string}
            subset_distinct
            disjoint_two_subset_distinct
glossary:
    distinct by value:
        the classic model divide n labeled object into k unlabled groups
        but some object are same, especially when it's string of a limited alphabetic.
"""
from functools import *
def all_groups(n):
    """ 
    des: 
        divide [0,n-1] into some unlabeled nonempty groups
        `ret` order: small group first
    impl: dfs ; hash unordered_set with sort
    time: ~BellB[n], first n (start from 1) [1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975, 678570 ] 
    """
    ret = []
    def dfs(i, grps):
        if i==n:
            ret.append(grps)
            return
        for grps_p, grp in enumerate(grps):
            dfs(i+1, grps[:grps_p]+(grp+(i,),)+grps[grps_p+1:])
        dfs(i+1, grps+((i,),))
    dfs(0, tuple())
    return ret

def k_groups(n, k):
    """ 
    des: 
        divide [0,n-1] into k unlabeled groups 
        related: the "submask" trick of bitmask can divide [0,n-1] into 3 labeled groups in O(3^n)
    time: second stirling number; ~O(k^n)
    """
    ret = []
    def dfs(i, grps, empty):
        if n-i == empty:
            if i==n:
                ret.append(grps)
            else:
                ret.append(grps[:i] + tuple((i,) for i in range(i,n)))
            return
        for grps_p, grp in enumerate(grps):
            if len(grp)==0:
                dfs(i+1, grps[:grps_p]+((i,),)+grps[grps_p+1:], empty-1)
                break
            else:
                dfs(i+1, grps[:grps_p]+(grp+(i,),)+grps[grps_p+1:], empty)
    dfs(0, (tuple(),)*k, k)
    return ret


###########################

def subsetsum_distinct(A, l, r):
    """ return list of sum of subset of A[l:r] , order by sum asc
    this is useful in meed-in-middle problems
    impl: bfs
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