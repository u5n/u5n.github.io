# range sum query
# single point update
# data stores on hashtable
from collections import defaultdict
import operator
from functools import reduce
class SegmentTree:
    __slots__='n','seg'
    def __init__(self,n):
        self.n,self.seg=n,defaultdict(int)
    def build(self,A,i=0,l=0,r=None):
        """A can be a List or Dict"""
        # assert len(A)>=self.n
        if r==None: r=self.n
        if r==l: 
            self.seg[i]=A[l]
            return
        m=l+(r-l)//2
        self.build(A,i*2+1,l,m)
        self.build(A,i*2+2,m+1,r)
        self.pushup(i)
    def pushup(self,i):
        self.seg[i]=self.seg[i*2+1]+self.seg[i*2+2]
    def query(self,l,r):
        return reduce(operator.add, map(lambda e:self.seg[e], self.subsegment(l,r)), 0)
    def update(self,Ai,new):
        seg=self.seg
        p = self.ancestor(Ai)
        seg[next(p)]=new
        for i in p: self.pushup(i)
    def subsegment(self,Al,Ar,i=0,l=0,r=None):
        if r==None: r=self.n-1
        if Ar>r or l>Ar: return
        elif Al<=l and r<=Ar: 
            yield i
        else:
            m = l+(r-l)//2
            yield from self.subsegment(Al,Ar,i*2+1,l,m)
            yield from self.subsegment(Al,Ar,i*2+2,m+1,r)
    
    def ancestor(self,Ai,i=0,l=0,r=None):
        if r==None: r=self.n-1
        if r==l: yield i
        else:
            m = l+(r-l)//2
            if Ai<=m: yield from self.ancestor(i,i*2+1,l,m)
            else: yield from self.ancestor(i,i*2+2,m+1,r)
            yield i