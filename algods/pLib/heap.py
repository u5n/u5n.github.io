from operator import lt
# implement c++ <algorithm> heap related
# i.e. heap operation on arraylist
# index start from 0
# default maxheap
def make_heap(A, l, r, opt=lt):
    """ heapify internal node from bottom to top
    time O(r-l), O(1)
    """
    for i in range((r+l)//2-1,l-1,-1):
        heapify(A, l, r, i, opt)

def heapify(A, l, r, i, opt=lt):
    """ heapify tree at A[l+i], assume two subtrees is a heap
    time O(lg(r-l)), O(1) """
    ext = i
    while True:
        for chi in i+i-l+1, i+i-l+2:
            if chi < r and opt(A[ext], A[i]):
                ext = chi
        if ext ==i: break
        A[i], A[ext] = A[ext], A[i]
        i = ext

def pop_heap(A, l, r, opt=lt):
    A[l], A[r-1] = A[r-1], A[l]
    heapify(A, l, r-1, l, opt)

def push_heap(A, l, r, opt=lt):
    i = r
    while i>0:
        par = (i+l-1)//2
        if opt(A[par], A[i]):
            A[i], A[par] = A[par], A[i]
            i = par

def heap_sort(A,l,r,opt=lt):
    make_heap(A,l,r)
    for i in range(r-l):
        pop_heap(A,l,r-i,opt)