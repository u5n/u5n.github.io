"""
to find longest palindrome, manacher is not recommend
TOC
    longestPalindrome
    manacher(parity)
    substr_pal_query
"""
from collections import namedtuple

from ..list import groupby
def longestPalindrome(s):
    """ des: groupby then expand around
    time:
        O(n^2), example "ababababababababababababab" 
        perform better under random data
    """
    n = len(s)
    ans = 0
    for prv, cur in groupby(s):
        left, right = prv-1, cur
        while left >= 0 and right < n and s[left]==s[right]:
            left-=1; right+=1
        ans = max(ans, right - left -1)

    return ans

Center = namedtuple('Center', ('i', 'r'))
def manacher_parity(s, parity):
    """ return P, 
    if parity==1: P[i]*2+1 is length of longest odd palindrome center at s[i] 
    else: P[i]*2 is length of longest even palindrome center at gap after s[i]
    """
    n = len(s)
    P = [0]*n
    cen = Center(0, 0)
    for i in range(n):
        if cen.r > i:
            l = 2*cen.i-i
            if P[l] < cen.r - i:
                P[i] = P[l]
                continue
            else:
                P[i] = cen.r - i
            
        while (il:=i-P[i]-parity)>=0 and (ir:=i+P[i]+1)<n and s[il]==s[ir]:
            P[i]+=1
        if i+P[i]>cen.r:
            cen = Center(i, i+P[i])
        # ans = max(ans, P[i]*2 + parity) # find length
        # if ...: ans = (i-P[i]-parity+1, i+P[i]+1) # find substring 
    return P
    
def substr_pal_query(s):
    """
    des: return function `is_pal(l,r)` that find `s[l:r]==s[l:r][::-1]` in O(1)
    time:
        preprocess: O(n)
        query: O(1)
    """
    P0 = manacher_parity(s, 0)
    P1 = manacher_parity(s, 1)
    def is_pal(l, r):
        """ s[l:r] """
        if r-l<=1: return True
        if (r-l)%2==0: return P0[(l+r-1)//2]>=(r-l)//2
        else: return P1[(l+r)//2]>=(r-l-1)//2
    return is_pal

