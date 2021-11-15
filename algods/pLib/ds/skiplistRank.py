# skiplist
import random
import math
import operator

# example structure by node rank
# [0] ---------------> [3] -> None
# [0] -> [1] --------> [3] -> None
# [0] -> [1] -> [2] -> [3] -> None
# usage: similar to multiset in c++, support operation by index/rank
# header rank is 0, the first node rank is 1, and so on
# header has no index, node index = rank -1

class SkiplistNode:
    class skiplistLevel:
        def __init__(self):
            # skiplistNode
            self.forward = None  
            # number of nodes between node and node.levels[i].forward
            # including node.levels[i].forward
            # exclude node itself
            self.span = 0

    def __init__(self, level: int, val):
        """ parameter level means number of levels """
        self.val = val
        # index start from 0
        self.levels = [self.skiplistLevel() for _ in range(level)]
    def __repr__(self):
        return str(self.val)

class Skiplist:
    def __init__(self, maxlevel=32, p=0.5, opt=operator.lt):
        self.MAXLEVEL = maxlevel
        self.P = p
        # the header.val is only used for repr
        self.header = SkiplistNode(maxlevel, '/')
        self.length = 0
        self.level = 1
        # operator to compare node.val
        # operator.lt: asc
        # opeartor.gt: desc
        # first asc, second desc
            # lambda l,r: return l[0]<r[0] if l[0]!=r[0] else l[1]>r[1]
        self.opt_lt = opt
    

    def _find(self, pred):
        """
        return 
            update[i]: 
                at level i, update[i] is the last node that 
                    pred((update[i].val,update[i].rank))
                if no such node, it's header
                update[i] is guaranteed not None
            rank[i]: rank of update[i], rank of header is 0
        """
        update = [None] * self.level
        rank = [None] * self.level
        x = self.header
        traversed = 0
        for i in range(self.level - 1, 0 - 1, -1):
            # compare val or compare rank
            while x.levels[i].forward!=None and\
                pred(x.levels[i].forward.val, traversed + x.levels[i].span):
                traversed += x.levels[i].span
                x = x.levels[i].forward
            update[i] = x
            rank[i] = traversed

        return update, rank

    def add(self, val):
        """
        create a new node with val and insert it into zsl
        return (pointer to )new node
        """
        update, rank = self._find(lambda l_val,_: self.opt_lt(l_val,val))
        level = min(1-int(math.log(1/random.random(), self.P)), self.MAXLEVEL)
        # for those new levels
        for i in range(self.level, level):
            rank.append(0)
            update.append(self.header)
            update[i].levels[i].span = self.length

        self.level = max(self.level, level)

        x = SkiplistNode(level, val)
        for i in range(level):
            x.levels[i].forward = update[i].levels[i].forward
            update[i].levels[i].forward = x
            x.levels[i].span = update[i].levels[i].span - (rank[0] - rank[i])
            update[i].levels[i].span = (rank[0] - rank[i]) + 1

        for i in range(level, self.level):
            update[i].levels[i].span += 1        
            
        self.length += 1
        return x

    def deleteNode(self, x, update):
        """
        delete skiplistnode, but require a `update` information see self._find 
        """
        for i in range(len(x.levels)):
            update[i].levels[i].span += x.levels[i].span - 1
            update[i].levels[i].forward = x.levels[i].forward
        for i in range(len(x.levels), self.level):
            update[i].levels[i].span -= 1
            
        while self.level > 1 and self.header.levels[self.level-1].forward == None:
            self.level -= 1
        self.length -=1 
    def opt_le(self, lval, val): return not self.opt_lt(val, lval)
    def opt_eq(self, lval, val): return not self.opt_lt(val, lval) and not self.opt_lt(lval, val)
    def discard(self, val):
        """ 
        delete first node that node.val == val    
        return 1 if delete successful else fail 
        """
        update, _ = self._find(lambda lval,_: self.opt_lt(lval,val))
        x = update[0].levels[0].forward
        if x!=None and self.opt_eq(x.val,val):
            self.deleteNode(x, update)
            # del skiplistNode x
            return 1
        return 0

    def bisect_right(self, val):
        # find first node opt(val, node.val)
        # return node and its index
        update, updaterank = self._find(lambda lval,_: self.opt_le(lval, val))
        return update[0].levels[0].forward, updaterank[0]
        
    def bisect_left(self, val):
        # find first node not opt(node.val, val)
        # return node and its index
        update, updaterank = self._find(lambda lval,_: self.opt_lt(lval,val))
        return update[0].levels[0].forward, updaterank[0]
    
    def __getitem__(self, idx):
        # transfrom idx to rank
        if not 0<=idx<self.length: raise IndexError
        rank = idx + 1 
        # different from compare val, compare of rank is O(1), 
        # so the find process can terminate when node.rank ==rank
        # here for convenience, I reuse self._find function
        update, _ = self._find(lambda _,rrank:rrank<=rank)
        return update[0]
    def __delitem__(self, idx):
        if not 0<=idx<self.length: raise IndexError
        rank = idx + 1 
        # different from __getitem__, it can't terminate when node.levels[0].forward.rank==rank
        update, _ = self._find(lambda _,rrank:rrank<rank)
        self.deleteNode(update[0].levels[0].forward, update)

# below for debug 
    def __iter__(self):
        """ iterate levels[0] in O(n),O(1) """
        x = self.header.levels[0].forward
        while x:
            yield x
            x=x.levels[0].forward
    def __len__(self): return self.length
    def __repr__(self):
        mat = [[None]*(self.length+1) for _ in range(self.level)]
        maxlen = 0
        for i,x in enumerate(self):
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

        return "-"*5+f" size:{self.length}  level:{self.level} "+'-'*5+\
            '\n'+"\n".join(sbuilder)+'\n'+'-'*30

if __name__ == "__main__":
    d = [0,1,0]
    if d[0]:
        print("test case 1\n")
        z = Skiplist()
        z.add((9, 'a'))
        z.add((2, 'b'))
        z.add((1, 'd'))
        z.add((4, 'c'))
        z.add((5, 'e'))
        assert z.discard((1, 'd')) == 1
        assert z.discard((1, 'd')) == 0
        z.add((0, 'g'))
        print(z)
    # as multiset
    if d[1]:
        print("test case 2\n")
        z2 = Skiplist()
        for e in 1,2,3,3,2,4,2:
            z2.add(e)
        print(z2[2])
        print(z2)
        assert z2.discard(3)==1
        print(z2)
        assert z2.discard(3)==1
        print(z2)
        assert z2.discard(3)==0
        print(z2)
        print(z2.bisect_left(100))
        print(z2.bisect_left(-100))
        print(z2.bisect_right(100))
        print(z2.bisect_right(-100))
        print(z2.bisect_left(2))
        print(z2.bisect_right(2))
        print(list(z2))
    # as min priority_queue
    if d[2]:
        print("test case 2\n")
        z3 = Skiplist()
        for e in range(10):
            z3.add(e)
        print(z3)
        print(z3.header.levels[0].forward.val) # O(1)
        del z3[0] # O(lg(n))
        print(z3)
