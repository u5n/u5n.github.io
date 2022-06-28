# TODO: rewrite everything use getPrevByCond
# skiplist
import random
import math
import operator

class SkiplistNode:
    __slots__ = 'levels','val'
    class SkipListNodeLevel:
        __slots__ = 'next','span'
        def __init__(self):
            # skiplistNode
            self.next = None
            # number of nodes between node and node.levels[i].next
            # including node.levels[i].next
            # exclude node itself
            self.span = 0

    def __init__(self, n_lvl: int, val):
        self.val = val
        # index start from 0
        self.levels = [self.SkipListNodeLevel() for _ in range(n_lvl)]
    def __str__(self):
        return str(self.val)

class Skiplist:
    """
    des:
        use singly linkedlist
    glossary:
        rank:
            senhead rank is -1, the first node rank is 0, and so on
    example:
         structure
            [0] ---------------> [80] -> None
            [0] -> [19] --------> [80] -> None
            [0] -> [19] -> [22] -> [80] -> None
    usage: similar to SortedList in python
    """
    __slots__ = 'lvllim', 'riseprob', 'senhead', 'sz', 'maxlvl', 'opt_lt'
    def __init__(self, lvllim=32, riseprob=0.5, opt=operator.lt):
        self.lvllim, self.riseprob = lvllim, riseprob
        # the senhead.val is only used for repr
        self.senhead = SkiplistNode(lvllim, '$')
        self.sz = self.maxlvl = 0
        # operator to compare node.val
        # operator.lt: asc
        # opeartor.gt: desc
        # first asc, second desc
            # lambda l,r: return l[0]<r[0] if l[0]!=r[0] else l[1]>r[1]
        self.opt_lt = opt

    def getPrevByCond(self, pred):
        """
        return 
            prevnodes[i]: 
                at level i, prevnodes[i] is the last node that `pred(prevnodes[i].val)`
                    the pred function is ascending
                if no such node, it's senhead
                guaranteed not None
            prevnodes_rank[i]: rank of prevnodes[i]
        """
        prevnodes = [None] * self.maxlvl
        prevnodes_rank = [None] * self.maxlvl
        x = self.senhead
        x_rank = -1 # rank of senhead 
        for i in reversed(range(self.maxlvl)):
            # compare val or compare rank
            while x.levels[i].next!=None and\
                pred(x.levels[i].next.val, x_rank + x.levels[i].span):
                x_rank += x.levels[i].span
                x = x.levels[i].next
            prevnodes[i] = x
            prevnodes_rank[i] = x_rank

        return prevnodes, prevnodes_rank
    
    def getNodeByRank(self, rank):
        x = self.senhead
        nstep = rank + 1 # senhead rank is -1
        for i in reversed(range(self.maxlvl)):
            while x.levels[i].next!=None and nstep>=x.levels[i].span:
                nstep -= x.levels[i].span
                x = x.levels[i].next
            if 0==nstep:
                return x
        raise Exception(".getNodeByRank: invalid rank")

    def deleteNode(self, x, prevnodes):
        """
        delete skiplistnode, but require a `prevnodes` information see self.getPrevByCond 
        """
        for i in range(len(x.levels)):
            prevnodes[i].levels[i].span += x.levels[i].span - 1
            prevnodes[i].levels[i].next = x.levels[i].next
        for i in range(len(x.levels), self.maxlvl):
            prevnodes[i].levels[i].span -= 1
            
        while len(x.levels)==self.maxlvl and self.senhead.levels[self.maxlvl-1].next == None:
            self.maxlvl -= 1
        self.sz -=1 

    def opt_le(self, lval, val): return not self.opt_lt(val, lval)
    def opt_eq(self, lval, val): return not self.opt_lt(val, lval) and not self.opt_lt(lval, val)
    def remove(self, val) -> bool:
        """ 
        delete first node that node.val == val    
        return 1 if delete successful else fail 
        """
        prevnodes = self.getPrevByCond(lambda lval,_: self.opt_lt(lval,val))[0]
        x = prevnodes[0].levels[0].next
        if x==None or not self.opt_eq(x.val,val):
            return 0

        self.deleteNode(x, prevnodes)
        # delete skiplistNode x
        return 1

    
    def top(self):
        return self.senhead.levels[0].next.val
        
    def __getitem__(self, rank):
        """ get item like a SortedList"""
        if not 0<=rank<self.sz: raise IndexError
        return self.getNodeByRank(rank).val

    def __delitem__(self, rank):
        """ delete item like a SortedList"""
        if not 0<=rank<self.sz: raise IndexError 
        prevnodes = self.getPrevByCond(lambda _,rrank:rrank<rank)[0]
        self.deleteNode(prevnodes[0].levels[0].next, prevnodes)

    def __len__(self): return self.sz
    
    def __iter__(self):
        x = self.senhead.levels[0].next
        while x:
            yield x.val
            x=x.levels[0].next
    def iterateNode(self):
        x = self.senhead.levels[0].next
        while x:
            yield x
            x=x.levels[0].next


    def __repr__(self):
        mat = [[None]*self.sz for _ in range(self.maxlvl)]
        maxlen = 0
        for i,x in enumerate(self.iterateNode()):
            for l in range(len(x.levels)):
                mat[l][i] = str(x)
                maxlen = max(maxlen, len(str(x)))
        
        sbuilder = []
        for level in mat[::-1]:
            level_sbuilder = []
            for e in level:
                if e!=None:
                    level_sbuilder.append(str(e).ljust(maxlen))
                else:
                    level_sbuilder.append("".ljust(maxlen))
            sbuilder.append("  ".join(level_sbuilder))

        return "-"*5+f" size:{self.sz}  maxlvl:{self.maxlvl} "+'-'*5+\
            '\n'+"\n".join(sbuilder)+'\n'+'-'*30+'\n'


# TODO: write testcases
# if __name__ == "__main__":
#     d = [1,1,1]
#     if d[0]:
#         print("test case 1\n")
#         z = Skiplist()
#         z.add((9, 'a'))
#         z.add((2, 'b'))
#         z.add((1, 'd'))
#         z.add((4, 'c'))
#         z.add((5, 'e'))
#         assert z.remove((1, 'd')) == 1
#         assert z.remove((1, 'd')) == 0
#         z.add((0, 'g'))
#         print(z)
        
#     # as multiset
#     if d[1]:
#         print("test case 2\n")
#         z2 = Skiplist()
#         for e in 1,2,3,3,2,4,2:
#             z2.add(e)
#         print(z2[2])
#         print(z2)
#         assert z2.remove(3)==1
#         print(z2)
#         assert z2.remove(3)==1
#         print(z2)
#         assert z2.remove(3)==0
#         print(z2)
#         print(list(z2))

#     # as min priority_queue
#     if d[2]:
#         print("test case 3\n")
#         z3 = Skiplist()
#         for e in range(10):
#             z3.add(e)
#         print(z3)
#         print(z3.senhead.levels[0].next.val) # O(1)
#         del z3[0] # O(lg(n))
#         print(z3)
