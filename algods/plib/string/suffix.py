from math import *
import string
import random


def suffix_array(A):
    n = len(A)
    cnt = [0]*n 
    sa = sorted(range(n), key=lambda i:A[i])
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
        i_ids = 0
        for iA in range(n-k, n): ids[i_ids] = iA; i_ids += 1
        for e_sa in sa:
            if e_sa >= k: ids[i_ids] = e_sa - k; i_ids += 1        

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
        k = k*2
    return sa, rk
    
def test():
    A = [random.random() for _ in range(100)]
    sa, rk = suffix_array(A)
    n = len(A)
    suffixs = []
    for i in range(n):
        suffixs.append((i, A[i:]))
    suffixs.sort(key=lambda e:e[1])
    for pair, i in zip(suffixs, sa):
        assert pair[0] == i