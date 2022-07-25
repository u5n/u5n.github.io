"""
TOC:
    insertion_sort
    merge_sort
    count_sort
    cycle_sort
    quick_sort
    pivot partition into three interval
    pivot partition into two interval
don't involve unless algorithm such as introsort(just use builtin sort), heapsort(just use builtin sort)
"""
import random
import sys; sys.path.append('../')

def insertion_sort(A, l, r):
    """ 
    sort islice(A,l,r)(its slice, not copy)
    feature: use adjacent sawp only
    """
    for i in range(l+1, r):
        # loop inv: A[l:i] is sorted
        for j in reversed(range(l+1, i+1)):
            if A[j]>=A[j-1]: break
            A[j],A[j-1]=A[j-1],A[j]
    
def merge_sort(A):
    """ convention: use left closed right open interval
    time: O(nlgn),O(lgn)
    """
    def merge(l,m,r):
        """ inplace merge A[l:m] and A[m:r] into A[l:r] 
        could use `A[l:r]=heapq.merge(A[l:m],A[m:r])`
        """
        tmp = [] # external array to store the sorted A[l:r]
        ri=m
        # available O(r-l) algorithm 
        for li in range(l, m):
            while ri<r and A[ri]<A[li]:
                tmp.append(A[ri])
                ri+=1
            tmp.append(A[li])
        A[l:ri] = tmp
    
    def merge_sort_dfs(l,r):
        if r-l<=1: return
        m = (l+r)//2
        merge_sort_dfs(l,m)
        merge_sort_dfs(m,r)
        merge(l,m,r)

    merge_sort_dfs(0, len(A))

def count_sort(A, key=lambda x:x):
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

def cycle_sort(A):
    """ 
    feature: 
        min swap times(without duplicates)
        min write to arrays(code should change a little)
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


def quick_sort(A, l, r):
    """
    quick_sort subroutine, 
    call quick_sort(A,0,len(A)) to sort A inplace
    """
    if r-l<=1: return
    p1,p2 = three_partition(A,l,r)
    quick_sort(A,l,p1)
    quick_sort(A,p2,r)


def three_partition(A, l, r, pivot=None):
    """ des:
        accoring to `pivot` partition A[l:r] into three interval A[l:i], A[i:j], A[j:k]
            A[l:i]<pivot
            A[i:j]==pivot
            A[j:k]>pivot
    """
    # assert l!=r
    i = j = l
    k = r
    if pivot is None:
        # or median of A[l],A[r-1],A[(l+r)//2]
        pivot = A[random.randrange(l,r)]
        
    while j<k:
        # [l:i] < ; [i:j] == ; [k:] >
        if A[j]<pivot:
            A[j],A[i]=A[i],A[j]
            i+=1; j+=1
        elif A[j]>pivot:
            k-=1
            A[j],A[k]=A[k],A[j]
        else:
            j+=1
    return i,j


def partition(A, l, r, pred):
    """ des: similar to std::partition
    return the beginning of second group
    this can't be directly use for quicksort
        can't process elements has same value 
        can't find position of pivot
    """
    i = l
    for j in range(l, r):
        # loop inv: all(pred(v) for v in A[l:i]); not any(pred(v) for v in A[i:r])
        if pred(A[j]):
            A[i],A[j] = A[j],A[i]
            i+=1
    return i