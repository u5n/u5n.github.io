from collections import defaultdict
from functools import reduce
from math import log2,ceil
class SegmentTree:
    """ segment tree build on closed interval [lbor, rbor]
    all use closed interval 
    usg: range max/min query with single point assign
    """
    __slots__='n','seg'
    def __init__(self, lbor, rbor, opt):
        self.lbor = lbor
        self.rbor = rbor
        
        totalnodes = 1<<(1+(rbor-lbor).bit_length())
        self.nodes=[0 for _ in range(totalnodes)]
        
        self.opt = opt

    def build(self,A,i=0,l=None,r=None):
        # assert len(A)>=self.rbor+1, self.lbor==0
        if r==None: r=self.rbor
        if r==l: 
            # initialization leaf
            self.nodes[i] = A[l]
            return
        m=(r+l)//2 # floor division
        self.build(A,i*2+1,l,m)
        self.build(A,i*2+2,m+1,r)
        self.pull(i)

    def pull(self,i):
        self.nodes[i] = self.opt(self.nodes[i*2+1]+self.nodes[i*2+2])

    def query(self,l,r):
        return reduce(self.opt, map(lambda e:self.nodes[e], self.subsegment(l,r)), 0)

    def assign(self, Ai, new):
        seg=self.nodes
        p = self.ancestor(Ai)

        seg[next(p)] = new # seg[next(p)]+=new # for addition opearation

        for i in p: self.pull(i)
    
    def subsegment(self,Al,Ar,i=0,l=None,r=None):
        """ des: interval operation template, without update(pull function)
        ret: yield all node that contained in interval [Al,Ar], in order of traverse_postorder desc
        """
        if r is None: l, r = self.lbor, self.rbor
        if Al>r or l>Ar: return
        elif Al<=l and r<=Ar: 
            yield i
        else:
            m = (r+l)//2 # floor division
            yield from self.subsegment(Al,Ar,i*2+1,l,m)
            yield from self.subsegment(Al,Ar,i*2+2,m+1,r)
    
    def ancestor(self,Ai,i=0,l=None,r=None):
        """ des: point opeartion template, without update; 
        ret: yield all node that contain point Ai, in order of depth desc
        """
        if r is None: l, r =self.lbor, self.rbor
        if r==l: yield i
        else:
            m = (r+l)//2 # floor division
            if Ai<=m: yield from self.ancestor(Ai,i*2+1,l,m)
            else: yield from self.ancestor(Ai,i*2+2,m+1,r)
            yield i