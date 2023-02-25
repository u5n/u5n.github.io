class ST_add:
    """ segment tree build on closed interval [0, rbor]
    all use closed interval 
    treenode stores in a array, treenode id start from 1
    usg: range operator.add query with single point assign
    test: @lc#307
    design: as simple as possible
    """
    __slots__ = 'n', 'nodes'
    
    def __init__(self, n):
        self.n = n
        self.nodes = [0]*(1 << (1 + (n - 1).bit_length()))

    def buildfrom(self, A):
        # assert len(A)>=self.n

        def build(nid, l, r):
            if r == l:
                self.nodes[nid] = A[l]
                return
            m = (r + l) // 2
            build(nid * 2, l, m)
            build(nid * 2 + 1, m + 1, r)
            self.pull(nid)

        build(1, 0, self.n - 1)

    def pull(self, i):
        self.nodes[i] = self.nodes[i * 2] + self.nodes[i * 2 + 1]

    def assign(self, Ai, new):
        nodes = self.nodes

        def ancestor(nid, l, r):
            if r == l:
                nodes[nid] = new
            else:
                m = (r + l) // 2
                if Ai <= m: ancestor(nid * 2, l, m)
                else: ancestor(nid * 2 + 1, m + 1, r)
                self.pull(nid)

        ancestor(1, 0, self.n - 1)

    def range_sum(self, Al, Ar):
        nodes = self.nodes

        def subsugment(nid, l, r):
            if Al > r or l > Ar: return 0
            elif Al <= l and r <= Ar:
                return nodes[nid]
            else:
                m = (r + l) // 2
                return subsugment(nid * 2, l, m) + subsugment(nid * 2 + 1, m + 1, r)

        return subsugment(1, 0, self.n - 1)

if __name__ == '__main__':
    A = ST_add(5)
    A.buildfrom([0,9,5,7,3])
    print(A.range_sum(4,4))
    print(A.range_sum(2,4))
    print(A.range_sum(3,3))
