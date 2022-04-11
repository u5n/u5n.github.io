from math import inf
import heapq

class CapicityPriorityQueue:
    """ useful priority queue used on sliding window """
    def __init__(self, cap, type:str = "min", A=None):
        self.pq = []
        self.cap = cap
        self.cs = 0 # cumulative sum
        self.add = self.__addmax if type == "max" else self.__add
        if A:
            for v in A:
                self.add(v)
                
    def __add(self, v):
        if len(self.pq)==self.cap:
            self.cs += v - heapq.heappushpop(self.pq, v)
        else:
            heapq.heappush(self.pq, v)
            self.cs += v
    def __addmax(self, v):
        if len(self.pq)==self.cap:
            self.cs += v  +  heapq.heappushpop(self.pq, -v)
        else:
            heapq.heappush(self.pq, -v)
            self.cs += v

def _secondmin(self):
    """
    problems: @lc#1289
    code template snippets, capicity size 2 priority queue
    """
    mi = smi = inf
    def append_rank(v):
        nonlocal mi, smi
        """ used to find min and second min(by index in the sorted array) together """
        if v < mi:
            mi, smi = v, mi
        elif v < smi:
            smi = v

    def append_distinct(v):
        nonlocal mi, smi
        """ used to find min and second min(by index in the sorted set) together """
        if v < mi:
            mi, smi = v, mi
        elif mi < v < smi:
            smi = v