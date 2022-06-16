""" this page wants a useful PriorityQueue
"""
from operator import lt
from typing import Iterable

class BinaryHeap:
    """ des: 
        use binary heap, implement with arraylist
        this class is useless 
        refer to https://stackoverflow.com/a/71295291/7721525
    constraint: the key of parent <= the key of child
    convention: index start from 0
    memory management: the capacity won't decrease, mul three if not enough 
    performance: 
        test lc#1353:
            withoutkey: 4x slower than builtin heapq
            withkey: 3x slower than builtin heapq
    """
    def __init__(self, key=None, it: Iterable =None, capacity=5):
        self.A = [None]*capacity
        self.r = 0
        
        if it:
            self.A_ = list(it)
            self.r = len(self.A_)
            if len(self.A_) > capacity:
                self.A = self.A_
            else:
                self.A[:self.r] = self.A_
            self.make_heap()

        if key: 
            self.key = key
            self.sift_up = self.__sift_key_up
            self.sift_down = self.__sift_key_down
            self.pushpop = self.__pushpop_key
    
    def pop(self):
        if self.r==0:
            raise IndexError("pop from an empty priority queue")
        self.A[0], self.A[self.r-1] = self.A[self.r-1], self.A[0]
        self.r -= 1
        self.sift_down(0)
        return self.A[self.r]
        
    def push(self, v):
        if self.r == len(self.A): self.A.extend([None]*(self.r*2))
        self.A[self.r] = v
        self.r += 1
        self.sift_up(self.r-1)

    def pushpop(self, v):
        if v <= self.A[0]:
            return v
        else:
            ret = self.A[0]
            self.A[0] = v
            self.sift_down(0)
            return ret

    def __pushpop_key(self, v):
        if self.key(v) <= self.key(self.A[0]):
            return v
        else:
            ret = self.A[0]
            self.A[0] = v
            self.sift_key_down(0)
            return ret

    def top(self): return self.A[0]
            
    def __len__(self): return self.r
    def __iter__(self): 
        while self.r: yield self.pop()

    # below is binary heap related function, could be static but not necessary

    def make_heap(self):
        """ sift_down internal node from bottom to top 
        time: O(self.r) """
        for i in reversed(range(self.r//2)):
            self.sift_down(i)

    def __sift_key_up(self, i):
        """ assume A[i] increased, then make A[l:r] heap again
        time O(lg(i-l)), O(1) """
        A, key = self.A, self.key
        while i:
            par = (i-1)//2
            if key(A[par]) > key(A[i]):
                A[i], A[par] = A[par], A[i]
                i = par
            else:
                break

    def sift_up(self, i):
        A = self.A
        while i:
            par = (i-1)//2
            if A[par] > A[i]:
                A[i], A[par] = A[par], A[i]
                i = par
            else:
                break

    def __sift_key_down(self, i):
        """ assume A[i] decreased, then make A[l:r] heap again
        time O(lg(r-l)), O(1) """
        A, key, r = self.A, self.key, self.r
        min_idx = i # the index with min key
        while True:
            for chi in i*2+1, i*2+2:
                if chi < r and key(A[chi])<key(A[min_idx]):
                    min_idx = chi
            if min_idx == i: break
            A[min_idx], A[i] = A[i], A[min_idx]
            i = min_idx

    def sift_down(self, i):
        A, r = self.A, self.r
        min_idx = i # the index with min key
        while True:
            chi = i*2+1
            if chi < r and A[chi] < A[min_idx]: min_idx = chi
            chi += 1
            if chi < r and A[chi] < A[min_idx]: min_idx = chi
            if min_idx == i: break
            A[min_idx], A[i] = A[i], A[min_idx]
            i = min_idx

            
if __name__ == '__main__':
    # test `BinaryHeap` without key 
    pq = BinaryHeap()
    for i in reversed(range(100)):
        pq.push(i)
    print(list(pq))
    
    # test `PriorityQueue` with key
    pq = BinaryHeap(key=lambda x:-x[2])
    pq.push((233, 2, 3))
    pq.push((0, 9, 3))