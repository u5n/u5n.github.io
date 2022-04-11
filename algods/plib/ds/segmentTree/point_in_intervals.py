"""
S is a set of intervals
    for convenience, 
        the border of the interval should be integer
        the intervals are unique

given a point, find all intervals in S that contain it
todo: 
    1. use lazy propagation
    2. rewrite subsegment function; remove ancester function
    3. given an interval, find all intervals in S that contain it
    4. given an interval, find all intervals in S that are contained in it
    
    
"""
import bisect

class SegmentTree:
    """
    ctor:
        intervals: 
            use closed interval
            left_border <= right_border
    data model:
        of a STNode suppose its corresponding segement on segmentTree is [STNodes_l, STNodes_r]
        then the real interval it stores is [coordinates[STNodes_l], coordinates[STNodes_r+1])
    """
    def __init__(self, intervals):
        v_rk = {}
        coordinates = set()
        for v1, v2 in intervals:
            coordinates.add(v1)
            coordinates.add(v2+1) # transform into right open interval
        self.coordinates = sorted(coordinates)
        for i,v in enumerate(self.coordinates):
            v_rk[v] = i

        self.rbor = len(self.coordinates)-2
        totalnodes = 1<<(1+(self.rbor).bit_length())
        self.nodes=[[] for _ in range(totalnodes)]
        
        for intervals_id, (begin, end) in enumerate(intervals):
            Al, Ar = v_rk[begin], v_rk[end+1]-1
            
            for node_idx in self.subsegment(Al, Ar):
                self.nodes[node_idx].append(intervals_id)

    def query_point(self, p):
        """ time: O(|ret| + log(totalnodes)) """
        # left extend p , right extend p
        ret = []

        Al = bisect.bisect_right(self.coordinates, p) - 1
        if Al == -1 or Al + 1 == len(self.coordinates):
            return ret

        for STNode_idx in self.ancestor(Al):
            ret.extend(self.nodes[STNode_idx])
        
        return ret
    
    def subsegment(self, Al, Ar, i=0, l=0, r=None):
        """ des: yield all nodes that contained in segment [Al, Ar]
        convention: use closed interval
        """
        if r is None: r = self.rbor
        if Al>r or l>Ar: return
        elif Al<=l and r<=Ar: 
            yield i
        else:
            m = (r+l)//2 # floor division
            yield from self.subsegment(Al,Ar,i*2+1,l,m)
            yield from self.subsegment(Al,Ar,i*2+2,m+1,r)
    
    def ancestor(self,Ai,i=0,l=0,r=None):
        """ 
        des: yield all node that is parent of self.nodes[Ai]
        convention: use closed interval
        """
        if r is None: r = self.rbor
        if r==l: 
            yield i
        else:
            m = (r+l)//2 # floor division
            if Ai<=m: yield from self.ancestor(Ai,i*2+1,l,m)
            else: yield from self.ancestor(Ai,i*2+2,m+1,r)
            yield i


if __name__ == "__main__":
    intervals = [[1,3],[4,9],[100,100],[-1000,1000],[100000, 200000], [50000,150000]]
    ST = SegmentTree(intervals)
    for p in -1000,1,2,3,4,5,9,10,100,1000,2000,120000:
        print(p, [intervals[idx] for idx in ST.query_point(p)])
    """
    expected:
        -1000 [[-1000, 1000]]
        1 [[1, 3], [-1000, 1000]]
        2 [[1, 3], [-1000, 1000]]
        3 [[1, 3], [-1000, 1000]]
        4 [[4, 9], [-1000, 1000]]
        5 [[4, 9], [-1000, 1000]]
        9 [[4, 9], [-1000, 1000]]
        10 [[-1000, 1000]]
        100 [[100, 100], [-1000, 1000]]
        1000 [[-1000, 1000]]
        2000 []
        120000 [[50000, 150000], [100000, 200000]]
    """