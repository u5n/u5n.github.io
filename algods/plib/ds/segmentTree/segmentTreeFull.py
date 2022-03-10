from math import *
from functools import reduce

class Data:
    __slots__="sum","ma","mi","add","prop"
    def __init__(self,sum=None,ma=None,mi=None,add=0,prop=None):
        self.sum,self.ma,self.mi,self.add,self.prop = sum,ma,mi,add,prop
    def __str__(self):
        return f"[s:{self.sum} ma:{self.ma} mi:{self.mi} a:{self.add} p:{self.prop}]"
class SegmentTree:
    """ segment tree build on closed interval [lbor, rbor]
    all use closed interval
    usg: range change(addition/assign), range query
    """
    def __init__(self, lbor, rbor): 
        self.rbor,self.lbor=rbor,lbor
        self.seg=[Data() for _ in range( 2**ceil(log2(rbor-lbor+1) +1))]
    def reinit(self, lbor, rbor):
        self.lbor, self.rbor = lbor, rbor
        self.seg.assign(lbor, rbor, 0)
    def build(self,A,i=0,l=None,r=None):
        if r==None: l=self.lbor; r=self.rbor
        if r==l: 
            self.seg[i]=Data(A[l],A[l],A[l])
            return
        m=l+(r-l)//2
        self.build(A,i*2+1,l,m)
        self.build(A,i*2+2,m+1,r)
        self.pull(i)
    def query_max(self,Al,Ar):
        return reduce(lambda l,r:max(l,self.seg[r].ma),self.subsegment(Al,Ar),-inf)
    def query_min(self,Al,Ar):
        return reduce(lambda l,r:min(l,self.seg[r].mi),self.subsegment(Al,Ar),inf)
    def query_sum(self,Al,Ar):
        return reduce(lambda l,r:l+self.seg[r].sum,self.subsegment(Al,Ar),0)
    def addition(self,Al,Ar,add):
        for i,l,r in self.subsegment(Al,Ar,update=True):
            self.seg[i].sum+=add*(r-l+1)
            self.seg[i].ma+=add
            self.seg[i].mi+=add
            self.seg[i].add+=add
    def assign(self,Al,Ar,val):
        for i,l,r in self.subsegment(Al,Ar,update=True):
            self.seg[i]=Data(val*(r-l+1),val,val,0,val)
    def pull(self,i):
        seg=self.seg
        seg[i]=Data(seg[i*2+1].sum+seg[i*2+2].sum,
                    max(seg[i*2+1].ma,seg[i*2+2].ma),
                    min(seg[i*2+1].mi,seg[i*2+2].mi))
    def push(self,i,l,m,r):
        seg=self.seg
        if seg[i].prop!=None:
            prop = seg[i].prop
            seg[i*2+1].prop=seg[i*2+2].prop=prop
            seg[i*2+1].ma=seg[i*2+1].mi=seg[i*2+2].ma=seg[i*2+2].mi=prop
            seg[i*2+1].add=seg[i*2+2].add=0
            seg[i*2+1].sum=prop*(m-l+1)
            seg[i*2+2].sum=prop*(r-m)
            seg[i].prop=None
        if seg[i].add!=0:
            add = seg[i].add
            seg[i*2+1].ma+=add
            seg[i*2+1].mi+=add
            seg[i*2+1].sum+=add*(m-l+1)
            seg[i*2+1].add+=add

            seg[i*2+2].add+=add
            seg[i*2+2].ma+=add
            seg[i*2+2].mi+=add
            seg[i*2+2].sum+=add*(r-m)
            seg[i].add=0
            
    def subsegment(self,Al,Ar,i=0,l=None,r=None,update=False):
        if r==None: l=self.lbor; r=self.rbor
        if Al>r or l>Ar: return
        elif Al<=l and r<=Ar: 
            if update: yield i,l,r
            else: yield i
        else:
            m = l+(r-l)//2
            self.push(i,l,m,r)
            yield from self.subsegment(Al,Ar,i*2+1,l,m,update)
            yield from self.subsegment(Al,Ar,i*2+2,m+1,r,update)
            if update: self.pull(i)

if __name__ == "__main__":
    A = [1,2,2,3,1,1,0]
    S1 = SegmentTree(0,len(A)-1)
    S1.build(A)
    print(S1.query_max(0,3))

    n=10
    S2 = SegmentTree(0, n-1)
    S2.assign(0,n-1,0) # initilize `A` to `[0]*n`
    print([S2.query_min(i,i) for i in range(n)]) # query `A[i]` in `log(n)`
