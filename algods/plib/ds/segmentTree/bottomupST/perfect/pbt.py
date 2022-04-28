"""
use special sentry to fill leaves into 2**i numbers 
application: 
    when node needs to store continous interval
"""

class ST_template_perfectbinarytree:
    """ point modify, range query 
    operator: 
        any monoid operator such as max, min, xor
        if the opeartor is commutative, the class need a little change, refer to https://codeforces.com/blog/entry/18051
    """
    __slots__ = 'n', 'nodes', 'leaves'
    class Node:
        pass
    def __init__(self, A):
        n_lvl = (len(A)-1).bit_length() + 1
        self.n = 2**(n_lvl - 1)
        self.leaves = A + ["dummy"]*(self.n - len(A))

        sentryNode = self.Node("Sentry")
        self.nodes = [
            self.Node("IdentityElement") if i < self.n + len(A) else sentryNode
            for i in range(self.n * 2)
        ]

        for inode in reversed(range(1, self.n)):
            self.pull(inode)

    def __get_segment_sz(self, inode):
        return 1<<(self.n.bit_length() - inode.bit_length())
    def __get_left_endpoint(self, inode):
        """
        formula:
            lend = (inode - level_begin)*segment_sz
                 = inode*segment_sz - n
        """
        return inode*self.__get_segment_sz(inode) - self.n
    def __get_right_medium(self, inode):
        return self.__get_left_endpoint(inode) + self.__get_segment_sz(inode)//2

    def pull(self, paridx):
        nodes = self.nodes
        # nodes[paridx].val = nodes[paridx*2].val + nodes[paridx*2+1].val

    def ancester(self, Ai):
        par = (self.n + Ai)//2
        while par:
            yield par
            par//=2

    def subsegment(self, l, r):
        nodes = self.nodes

        l += self.n
        r += self.n
        while l<r:
            if l&1: yield nodes[l]; l+=1
            if r&1: r-=1; yield nodes[r]
            l//=2
            r//=2


class ST_repeatsubarray:
    """
    find maximum size of subarrays with same characters
    test: @lc#2213
    """
    __slots__ = 'n', 'nodes', 'leaves'
    class Node:
        """
        premax: max size prefix with same characters
        sufmax: max size suffix with same characters
        max: max size of subarray with same characters
        """
        __slots__ = 'premax', 'sufmax', 'max'
        def __init__(self, premax, sufmax, max):
            self.premax, self.sufmax, self.max = premax, sufmax, max
        def __repr__(self): return f'Node(premax:{self.premax}, sufmax:{self.sufmax}, max:{self.max})'

    def __init__(self, A):
        n_lvl = (len(A)-1).bit_length() + 1
        self.n = 2**(n_lvl - 1)
        self.leaves = list(A) + ['\0']*(self.n - len(A))

        sentryNode = self.Node(0,0,0)
        self.nodes = [
            self.Node(1,1,1) if i < self.n + len(A) else sentryNode
            for i in range(self.n * 2)
        ]

        for inode in reversed(range(1, self.n)):
            self.pull(inode)

    def pull(self, paridx):
        nodes = self.nodes
        par, lchi, rchi = nodes[paridx], nodes[paridx*2], nodes[paridx*2+1]
        child_segment_sz = 1<<(self.n.bit_length() - paridx.bit_length() - 1)
        rmid = (paridx*2+1)*child_segment_sz - self.n
        mid_connect = (self.leaves[rmid] == self.leaves[rmid-1])

        par.premax = lchi.premax + (mid_connect and lchi.premax == child_segment_sz)*rchi.premax
        par.sufmax = (mid_connect and rchi.sufmax == child_segment_sz)*lchi.sufmax + rchi.sufmax
        par.max = max(lchi.max, rchi.max, mid_connect*(lchi.sufmax + rchi.premax))

    def assign(self, Ai, newchr):
        self.leaves[Ai] = newchr
        par = (self.n + Ai)//2
        while par:
            self.pull(par)
            par//=2
