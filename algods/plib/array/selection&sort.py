"""
TOC:
    find inversion pairs
    mergesort
    countsort
    cyclesort
    quicksort
    pivot partition into three interval
    pivot partition into two interval

"""
import random


def mergesort(A):
    """ convention: use left closed right open interval, cuz it's used to count number of sth.
    time: O(nlgn),O(lgn)
    """
    def merge(l,m,r):
        """ inplace merge A[l:m] and A[m:r] into A[l:r] """
        tmp = [] # external array to store the sorted A[l:r]
        ri=m
        # available O(r-l) algorithm 
        for li in range(l, m):
            while ri<r and A[ri]<A[li]:
                tmp.append(A[ri])
                ri+=1
            tmp.append(A[li])
        A[l:ri] = tmp
    
    def mergesort_dfs(l,r):
        if r-l<=1: return
        m = (l+r)//2
        mergesort_dfs(l,m)
        mergesort_dfs(m,r)
        merge(l,m,r)

    mergesort_dfs(0, len(A))

def countsort(A, key=lambda x:x):
    """ assume key >= 0, key is int """
    maxk = max(key(e) for e in A)
    count = [0]*(1+maxk)
    for e in A: count[key(e)] += 1
    for i_count in range(1, maxk+1): count[i_count] += count[i_count-1]
    
    # sorted A
    As = [None]*len(A)
    for e in reversed(A):
        k = key(e)
        count[k] -= 1
        As[count[k]] = e
    return As

def cyclesort(A):
    """ 
    _: reduce the procedure by dfa 
    des: theoretical min times of swap
    time: 
        O(n^2),O(1)
        if rank of elment can get at O(1), the time complexity will be O(n)
    """
    n = len(A)
    min_swap = 0
    for i in range(n):
        # A[:i] is sorted 
        while True:
            nlt = 0 # get rank of A[i]
            for j in range(i+1,n):
                if A[j]<A[i]:
                    nlt+=1
            if nlt==0: break
            # in case of equal elements
            while A[i+nlt] == A[i]: 
                # loop inv: A[i+nlt] is already sorted
                nlt += 1
            # next to-sort element place in A[i]
            A[i+nlt],A[i]=A[i],A[i+nlt]
            min_swap += 1
    return min_swap

def quicksort(A, l, r):
    """
    quicksort subroutine, 
    call quicksort(A,0,len(A)) to sort A inplace
    """
    if r-l<=1: return
    p1,p2 = three_partition(A,l,r)
    quicksort(A,l,p1)
    quicksort(A,p2,r)

def three_partition(A, l, r, pivot=None):
    """
    pivot partition A[l:r] into three interval A[l:i], A[i:j], A[j:r]
    """
    # assert l!=r
    i = j = l
    k = r
    if pivot is None:
        pivot = A[random.randrange(l,r)]
    while j<k:
        # [l:i] < ; [i:j] == ; [k:] >
        if A[j]<pivot:
            A[j],A[i]=A[i],A[j]
            i+=1; j+=1
        elif A[j]==pivot:
            j+=1
        else:
            k-=1
            A[j],A[k]=A[k],A[j]
    return i,j

def partition(A, l, r, pivot=None):
    """ 
    des:
        rearrange `A` such that all elements less_than pivot are put before pivot
        return position of pivot
    feature: inplace, not stable 
    """
    if pivot is None:
        pivot_index = random.randrange(l,r)
        A[pivot_index], A[r-1] = A[r-1], A[pivot_index]
        pivot = A[r-1]

    i = l
    for j in range(l, r):
        # loop inv: A[l:i] <= pivot < A[i:j]
        if A[j] <= pivot:
            A[i],A[j] = A[j],A[i]
            i+=1
    return i-1