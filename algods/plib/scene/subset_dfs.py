from functools import lru_cache
from linecache import cache
cache = lru_cache(None)

def subsetsum_ordered(A, l, r):
    """ return list of sum of subset of A , order by sum asc 
    impl: bfs
    """
    ret = {0}
    for i in range(l, r):
        ret |= {v+A[i] for v in ret}
    return sorted(ret)

def subset_distinct(s: str):
    """ """
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

def disjoint_two_subset_distinct(s:str, partition=False):
    """ ret: 
        if not partition: all unordered and value distinct pairs@[s1, s2]{s1&s2==∅; s1 and s2 are indexed_subset of s}, where s1<=s2
        else: all unordered and value distinct pairs@[s1, s2]{s1&s2==∅; s1|s2=s; s1 and s2 are indexed_subset of s}, where s1<=s2
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
        if not partition:
            dfs(i+1, s1, s2)
    dfs(0, '', '')
    return ret