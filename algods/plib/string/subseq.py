from collections import defaultdict
import string
import operator
from bisect import *

from plib.binary_search import binary_search_first
def lis(s):
    """ 
    des:
        find longest strictly ascending subsequence
    ret: 
        lis_prefix: i -> length of lis on s[:i]
        lis_endat: i -> length of longest lis ending at s[i]
    """
    n = len(s)
    lis_prefix = [0]*(n+1)
    # lis_endat = [0]*n

    # divide subsequence by their length
    # sz -> MIN{seq[-1]; seq is subsuquence of s; len(seq)==sz}
    dp = [None]*(n+1)
    maxsz = 0
    for i,ch in enumerate(s):
        # `>` for non-strict; `<=` for strict descending
        l = binary_search_first(1, 1+maxsz, lambda x: dp[x]>=ch)
        if l > maxsz: maxsz = l

        dp[l] = ch
        lis_prefix[i+1] = maxsz
        # lis_endat[i] = l
    
    return lis_prefix
    
def next_char(s, prev=False):
    """ para: 
        s: assume only contain lowercases
        prev: if set True, return the `prev` array
    ret: next:
        i,ch -> MIN{j; ord(s[j])-97==ch; j>=i; default=n} 
    """
    n = len(s)
    next = [None]*n
    if prev:
        it = range(n)
        next_arr = [-1]*26
    else:
        it = reversed(range(n))
        next_arr = [n]*26
    for i in it:
        e = ord(s[i])-97
        next_arr[e] = i
        next[i] = tuple(next_arr)
    return next