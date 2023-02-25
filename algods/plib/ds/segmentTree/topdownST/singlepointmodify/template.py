"""
todo: determine whether treenode id start from 1
"""
from functools import reduce

class ST_template:
    """ segment tree build on closed interval [lbor, rbor]
    all use closed interval 
    """
    __slots__='n','seg'
    def __init__(self, lbor, rbor, opt):
        self.lbor = lbor
        self.rbor = rbor
        
        totalnodes = 2<<(rbor-lbor).bit_length() # upperbound as if it's perfect binary tree
        self.nodes=[0 for _ in range(totalnodes)]
        
        self.opt = opt

    def buildfrom(self, A):
        # A is defined on [l,r]
        def build(nid, l, r):
            if r==l: 
                # initialization leaf
                self.nodes[nid] = A[l]
                return
            m=(r+l)//2 # floor division
            build(nid*2,l,m)
            build(nid*2+1,m+1,r)
            self.pull(nid)

        build(1, self.lbor, self.rbor)
        

    def pull(self,i):
        self.nodes[i] = self.opt(self.nodes[i*2]+self.nodes[i*2+1])

    def range_query(self,l,r):
        return reduce(self.opt, map(lambda e:self.nodes[e], self.subsegment(l,r)), 0)

    def point_assign(self, Ai, new):
        seg=self.nodes
        p = self.ancestor(Ai)

        seg[next(p)] = new # seg[next(p)]+=new # for addition opearation

        for i in p: self.pull(i)
    
    def subsegment(self,Al,Ar):
        """ des: interval operation template, without update(pull function)
        ret: yield all node that contained in interval [Al,Ar], in order of traverse_postorder desc
        """
        def subsegment(nid ,l, r):
            if Al>r or l>Ar: return
            elif Al<=l and r<=Ar: 
                yield nid
            else:
                m = (r+l)//2 # floor division
                yield from self.subsegment(nid*2,l,m)
                yield from self.subsegment(nid*2+1,m+1,r)
    
        subsegment(1, self.lbor, self.rbor)

    def __ancestor(self,Ai):
        """ des: point opeartion template, without update; 
        ret: yield all node that contain point Ai, in order of depth desc
        """
        def ancestor(nid, l, r):
            if r==l: yield nid
            else:
                m = (r+l)//2 # floor division
                if Ai<=m: yield from ancestor(nid*2,l,m)
                else: yield from ancestor(nid*2+1,m+1,r)
                yield nid

        ancestor(1, self.lbor, self.rbor)