"""
principle:
    the purpose of this file is to demonstrate how the algorithm work
    simple is better, only necessary optimization
usage:
    persistent array
test: without test
"""
from collections import namedtuple
Node = namedtuple("Node", "lchi rchi val", defaults=[None,None,0])
class PersistentArray:
    """ The internal(not leaf) node don't have `val` attribute
    use closed interval everywhere
    """
    INITIAL_VERSION_NUMBER = 0
    def __init__(self, initarr):
        def build(l, r):
            if l==r: return Node(val=initarr[l])
            m = (l+r)//2
            return Node(build(l, m), build(m+1, r))
        self.n = len(initarr)
        self.roots = {}
        self.roots[self.INITIAL_VERSION_NUMBER] = build(0, self.n-1)
    
    def dispatch(self, prv_version, cur_version, index, value):
        """ dispatch a new version named `cur_version` based on `prv_version`, with only underlying array value at `index` changed to `value`
        time space complexity: O(lg(n)), increase O(lg(n)) space
        """
        def dfs(node, l, r):
            if l==r: return Node(val=value)
            m = (l+r)//2
            if index<=m: return Node(dfs(node.lchi , l, m), node.rchi)
            else: return Node(node.lchi, dfs(node.rchi, m+1, r))
        self.roots[cur_version] = dfs(self.roots[prv_version], 0, self.n-1)
    
    def assign_point(self, version, index, value):
        def dfs(node, l, r):
            if l==r: node.val = value; return
            m = (l+r)//2
            if index<=m: dfs(node.lchi, l, m)
            else: dfs(node.rchi, m+1, r) 
        dfs(self.roots[version], 0, self.n-1)

    def get_point(self, version, index):
        def dfs(node, l, r):
            if l==r: return node.val
            m = (l+r)//2
            if index<=m: return dfs(node.lchi, l, m)
            else: return dfs(node.rchi, m+1, r) 
        return dfs(self.roots[version], 0, self.n-1)

    def get_array(self, version):
        sta = [self.roots[version]] # recursion stack
        ret = []
        while sta:
            cur = sta.pop()
            if cur.lchi is None: 
                ret.append(cur.val)
            else:
                sta.append(cur.rchi)
                sta.append(cur.lchi)
        return ret


class STNode:
    __slots__ = 'lchi','rchi','val'
    def __init__(self, lchi=None, rchi=None, val=0):
        # create internal node 
        if lchi!=None:
            self.val = lchi.val + rchi.val
        # create leaves
        else:
            self.val = val
        self.lchi, self.rchi = lchi, rchi
        
class PersistentSegmentTree:
    """ The internal node val is sum of their childs value
    use closed interval everywhere
    don't support change values, can only make immutable copy
    test: -[] @CSES#1737
    """
    INITIAL_VERSION_NUMBER = 0
    def __init__(self, initarr):
        def build(l, r):
            if l==r: return STNode(val=initarr[l])
            m = (l+r)//2
            return STNode(build(l, m), build(m+1, r))
        self.n = len(initarr)
        self.roots = {}
        self.roots[self.INITIAL_VERSION_NUMBER] = build(0, self.n-1)
    
    def dispatch(self, prv_version, cur_version, index, value):
        """ dispatch a new version named `cur_version` based on `prv_version`, with only underlying array value at `index` changed to `value`
        time space complexity: O(lg(n)), increase O(lg(n)) space
        """
        def dfs(node, l, r):
            if l==r: return STNode(val=value)
            m = (l+r)//2
            if index<=m: return STNode(dfs(node.lchi , l, m), node.rchi)
            else: return STNode(node.lchi, dfs(node.rchi, m+1, r))
        self.roots[cur_version] = dfs(self.roots[prv_version], 0, self.n-1)
    
    def query_interval_sum(self, version, Al, Ar):
        def dfs(node, l, r):
            if l>Ar or r<Al: return 0
            if l>=Al and r<=Ar: 
                if node.lchi:
                    return node.lchi.val + node.rchi.val
                return node.val
            m = (l+r)//2
            return dfs(node.lchi, l, m) + dfs(node.rchi, m+1, r)
        return dfs(self.roots[version], 0, self.n-1)

    def get_point(self, version, index):
        def dfs(node, l, r):
            if l==r: return node.val
            m = (l+r)//2
            if index<=m: return dfs(node.lchi, l, m)
            else: return dfs(node.rchi, m+1, r) 
        return dfs(self.roots[version], 0, self.n-1)

    def get_array(self, version):
        sta = [self.roots[version]] # recursion stack
        ret = []
        while sta:
            cur = sta.pop()
            if cur.lchi is None: 
                ret.append(cur.val)
            else:
                sta.append(cur.rchi)
                sta.append(cur.lchi)
        return ret

if __name__ == "__main__":
    n = 500
    import random
    A = [random.randrange(-2**32, 2**32) for _ in range(n)]
    pst = PersistentArray(A)
    # create version-199, where change A[2] to 30
    pst.dispatch(0, 199, 2, 30)
    # create version-100, where change A[3] to 400
    pst.dispatch(0, 100, 3, 40)
    # change A[1] to 200 in version-0
    pst.assign_point(0, 1, 200)
    # change A[5] to 500 in version-0
    pst.assign_point(0, 5, 500)
    pst.dispatch(100, 200, 10, 10000)
    A_version200 = pst.get_array(200)
    assert A_version200[1] == 200, "ancester change where descendant remain"