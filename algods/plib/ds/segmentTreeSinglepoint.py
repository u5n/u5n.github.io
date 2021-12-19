""" range max/min query with single point assign
    todo: change to range max/min query, range sum can be substitute by BIT
    adv: 
        faster on single point assign
            because `self.ancestor` is faster then `self.subsegment`
"""
from collections import defaultdict
from functools import reduce
from math import log2,ceil
class SegmentTree:
    __slots__='n','seg'
    def __init__(self, lbor, rbor, opt):
        self.lbor = lbor
        self.rbor = rbor
        self.seg=[0 for _ in range( 2**ceil(log2(rbor-lbor+1)+1) )]
        self.opt = opt
    def build(self,A,i=0,l=None,r=None):
        # assert len(A)>=self.rbor+1, self.lbor==0
        if r==None: r=self.rbor
        if r==l: 
            self.seg[i]=A[l]
            return
        m=(r+l)//2 # floor division
        self.build(A,i*2+1,l,m)
        self.build(A,i*2+2,m+1,r)
        self.pushup(i)
    def pushup(self,i):
        self.seg[i] = self.opt(self.seg[i*2+1]+self.seg[i*2+2])
    def query(self,l,r):
        return reduce(self.opt, map(lambda e:self.seg[e], self.subsegment(l,r)), 0)
    def assign(self,Ai,new):
        seg=self.seg
        p = self.ancestor(Ai)
        seg[next(p)]=new # seg[next(p)]+=new # for addition opearation
        for i in p: self.pushup(i)

    def subsegment(self,Al,Ar,i=0,l=None,r=None):
        if r==None: l=self.lbor; r=self.rbor
        if Ar>r or l>Ar: return
        elif Al<=l and r<=Ar: 
            yield i
        else:
            m = (r+l)//2 # floor division
            yield from self.subsegment(Al,Ar,i*2+1,l,m)
            yield from self.subsegment(Al,Ar,i*2+2,m+1,r)
    
    def ancestor(self,Ai,i=0,l=None,r=None):
        if r==None: l=self.lbor; r=self.rbor
        if r==l: yield i
        else:
            m = (r+l)//2 # floor division
            if Ai<=m: yield from self.ancestor(i,i*2+1,l,m)
            else: yield from self.ancestor(i,i*2+2,m+1,r)
            yield i