""" this page don't intend to write a binaryHeap datastructure, it wants useful PriorityQueue
"""
from operator import lt
from typing import Iterable

class PriorityQueue:
    """ use binary heap, imlement with arraylist
    constraint: the key of parent <= the key of child
    convention: index start from 0
    dynamic memory: the capacity won't decrease, mul three if not enough 
    performance: 
        4x slower that builtin heapq
        test: lc#1353
        so use `SortedList` if avaiable
    """
    def __init__(self, key=None, it: Iterable =None, capacity=5):
        self.A = [None]*capacity
        self.r,self.key = 0, key
        
        if it:
            self.A_ = list(it)
            self.r = len(self.A_)
            if len(self.A_) > capacity:
                self.A = self.A_
            else:
                self.A[:self.r] = self.A_
            self.make_heap()

        if self.key: 
            self.sift_up = self.sift_key_up
            self.sift_down = self.sift_key_down
    
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
    
    def top(self): return self.A[0]
    # below is binary heap related function

    def make_heap(self):
        """ sift_down internal node from bottom to top 
        time: O(self.r) """
        for i in reversed(range(self.r//2)):
            self.sift_down(i)

    def sift_key_up(self, i):
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

    def sift_key_down(self, i):
        """ assume A[i] decreased, then make A[l:r] heap again
        time O(lg(r-l)), O(1) """
        A, key, r = self.A, self.key, self.r
        ext = i # the index with min key
        while True:
            for chi in i*2+1, i*2+2:
                if chi < r and key(A[chi])<key(A[ext]):
                    ext = chi
            if ext == i: break
            A[ext], A[i] = A[i], A[ext]
            i = ext

    def sift_down(self, i):
        A, r = self.A, self.r
        ext = i # the index with min key
        while True:
            chi = i*2+1
            if chi < r and A[chi] < A[ext]: ext = chi
            chi += 1
            if chi < r and A[chi] < A[ext]: ext = chi
            if ext == i: break
            A[ext], A[i] = A[i], A[ext]
            i = ext
            
    def __len__(self): return self.r
    def __iter__(self): 
        while self.r: yield self.pop()

if __name__ == '__main__':
    # test `PriorityQueue` without key 
    pq = PriorityQueue()
    for i in reversed(range(100)):
        pq.push(i)
    print(list(pq))
    
    # test `PriorityQueue` with key
    pq = PriorityQueue(key=lambda x:-x[2])
    pq.push((233, 2, 3))
    pq.push((0, 9, 3))