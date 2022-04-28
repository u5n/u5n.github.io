from math import inf
import heapq

class CapicityPriorityQueue:
    """ useful priority queue used on sliding window """
    def __init__(self, cap, key=None):
        self.pq = []
        self.cap = cap
        self.cs = 0 # cumulative sum
        if key is None:
            self.add = self.__add
        else:
            self.add = self.__addkey
            self.key = key
                
    def __add(self, v):
        if len(self.pq)==self.cap:
            self.cs += v - heapq.heappushpop(self.pq, v)
        else:
            heapq.heappush(self.pq, v)
            self.cs += v
            
    def __addkey(self, v):
        kv = self.key(v)
        if len(self.pq)==self.cap:
            self.cs += v - heapq.heappushpop(self.pq, (kv, v))[1]
        else:
            heapq.heappush(self.pq, (kv, v))
            self.cs += v
    
    def __iter__(self):
        if self.key is None:
            return iter(self.pq)
        else:
            return (v for (kv, v) in self.pq)

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