from math import *
import string
import random

def Z_function(A):
    """ ret: z[i] is length of longest prefix of A and A[i:]
    test: https://leetcode-cn.com/problems/sum-of-scores-of-built-strings/
    """
    n = len(A)
    z = [0]*n; z[0] = n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min (r - i + 1, z[i - l])
        while i + z[i] < n and A[z[i]] == A[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1
    
    return z


def suffix_array(A):
    """ 
    des: the suffix array implement with some constant optimize
    time: O(nlgn) """
    n = len(A)
    cnt = [0]*n 
    # rank -> suffix number
    sa = sorted(range(n), key=lambda i:A[i])
    # suffix number -> rank
    rk = [0]*n
    rkp = [-1]*(2*n)
    ids = [0]*n
    def equal(k, iA1, iA2): return rkp[iA1] == rkp[iA2] and rkp[iA1+k]==rkp[iA2+k]

    i_class = 0
    for i_sa in range(1, n):
        if A[sa[i_sa]] != A[sa[i_sa-1]]: i_class += 1
        rk[sa[i_sa]] = i_class
    if i_class == n-1: return sa, rk

    k = 1
    while k<n:
        # first countsort
        i_ids = 0
        for iA in range(n-k, n): ids[i_ids] = iA; i_ids += 1
        for e_sa in sa:
            if e_sa >= k: ids[i_ids] = e_sa - k; i_ids += 1        
        
        # second countsort 
        for e_rk in rk: cnt[e_rk] += 1
        for i_cnt in range(1, i_class+1): cnt[i_cnt] += cnt[i_cnt-1]
        for iA in reversed(ids): cnt[rk[iA]] -= 1; sa[cnt[rk[iA]]] = iA
        for i_cnt in range(i_class+1): cnt[i_cnt] = 0
        
        rkp[:n] = rk
        i_class = 0
        for i_sa in range(1, n):
            if not equal(k, sa[i_sa-1], sa[i_sa]):
                i_class += 1
            rk[sa[i_sa]] = i_class
        if i_class == n-1: break
        k *= 2

    return sa, rk
    

if __name__ == '__main__':
    A = [random.random() for _ in range(100)]
    sa, rk = suffix_array(A)
    n = len(A)
    assert sorted(range(n), key=lambda i:A[i:]) == sa