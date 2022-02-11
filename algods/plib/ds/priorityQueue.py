import heapq
class CapicityPriorityQueue:
    """ useful priority queue used on sliding window """
    def __init__(self, cap, type:str = "min", A=None):
        self.pq = []
        self.cap = cap
        self.cs = 0 # cumulative sum
        if type == "max":
            self.add = self.addmax
        if A:
            for v in A:
                self.add(v)
    def add(self, v):
        if len(self.pq)==self.cap:
            self.cs += v - heapq.heappushpop(self.pq, v)
        else:
            heapq.heappush(self.pq, v)
            self.cs += v
    def addmax(self, v):
        if len(self.pq)==self.cap:
            self.cs += v  +  heapq.heappushpop(self.pq, -v)
        else:
            heapq.heappush(self.pq, -v)
            self.cs += v