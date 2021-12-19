# divide and conquer + list
def count_inversion(A):
    n = len(A)
    inv_cnt = 0
    def mergesort(l,r):
        if r-l<=1: return
        m = (l+r)//2
        mergesort(l,m)
        mergesort(m,r)
        merge(l,m,r)
    def merge(l,m,r):
        nonlocal inv_cnt
        ret = []
        ri=m
        for li in range(l, m):
            while ri<r and A[ri]<A[li]:
                ret.append(A[ri])
                ri+=1
            # available two pointer algorithm
            inv_cnt += ri-m
            ret.append(A[li])
        A[l:ri] = ret
    mergesort(0,n)
    return inv_cnt