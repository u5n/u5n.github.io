# skiplist
import random
import operator

# example structure by node rank
# [0] ---------------> [3] -> None
# [0] -> [1] --------> [3] -> None
# [0] -> [1] -> [2] -> [3] -> None
# usage: refer to bottom of this file
# header rank is 0, the first node rank is 1, and so on
# header has no index, node index = rank -1
class SkiplistNode:
    class skiplistLevel:
        def __init__(self) -> None:
            # skiplistNode
            self.forward = None  
            # number of nodes between node and node.levels[i].forward
            # including node.levels[i].forward
            # exclude node itself
            self.span = 0

    def __init__(self, level: int, val) -> None:
        """ parameter level means number of levels """
        self.val = val
        # index start from 0
        self.levels = [self.skiplistLevel() for _ in range(level)]
    def __repr__(self):
        return str(self.val)

class Skiplist:
    def __init__(self, maxlevel=32, p=0.5, opt=operator.lt) -> None:
        self.skiplist_MAXLEVEL = maxlevel
        self.skiplist_P = p
        # the header.val is only used for repr
        self.header = SkiplistNode(maxlevel, '/')
        self.length = 0
        self.level = 1
        # operator.lt: asc
        # opeartor.gt: desc
        self.opt = opt

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
        for i in range(self.level):
            x = self.header
            rank = 0
            while x:
                mat[i][rank] = str(x)
                maxlen = max(maxlen, len(str(x)))
                rank += x.levels[i].span
                x = x.levels[i].forward
        
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

    def randomLevel(self):
        """ return number of levels of a new node should have """
        level = 1
        while random.random() < self.skiplist_P:
            random.seed(random.random())
            level += 1
        return min(level, self.skiplist_MAXLEVEL)

    def find(self, pred):
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
            # horizental traverse
            while x.levels[i].forward!=None and\
                pred(x.levels[i].forward.val, traversed + x.levels[i].span):
                traversed += x.levels[i].span
                x = x.levels[i].forward
            update[i] = x
            rank[i] = traversed

        return update, rank

    def insert(self, val):
        """
        create a new node with val and insert it into zsl
        return (pointer to )new node
        """
        update, rank = self.find(lambda l_val,_: self.opt(l_val,val))
        level = self.randomLevel()
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
        for i in range(self.level):
            if update[i].levels[i].forward == x:
                update[i].levels[i].span += x.levels[i].span - 1
                update[i].levels[i].forward = x.levels[i].forward
            else:
                update[i].levels[i].span -= 1
        

        while self.level > 1 and self.header.levels[self.level-1].forward == None:
            self.level -= 1
        self.length -=1 

    def delete(self, val):
        """ return 1 if delete successful else fail """
        update, _ = self.find(lambda lval,_: self.opt(lval,val))
        x = update[0].levels[0].forward
        if x and x==val:
            self.deleteNode(x, update)
            # del skiplistNode x
            return 0
        return 1

    def bisect_right(self, val):
        # find first node opt(val, node.val)
        # return node and its index
        update, updaterank = self.find(lambda lval,_: not self.opt(val, lval))
        return update[0].levels[0].forward, updaterank[0]
        
    def bisect_left(self, val):
        # find first node not opt(node.val, val)
        # return node and its index
        update, updaterank = self.find(lambda lval,_: self.opt(lval,val))
        return update[0].levels[0].forward, updaterank[0]
    
    def __getitem__(self, idx):
        # transfrom idx to rank
        if not 0<=idx<self.length: raise IndexError
        rank = idx + 1 
        # different from compare val, compare of rank is O(1), 
        # so the find process can terminate when node.rank ==rank
        # here for convenience, I reuse zslFind function
        update, _ = self.find(lambda _,rrank:rrank<=rank)
        return update[0]
    def __delitem__(self, idx):
        if not 0<=idx<self.length: raise IndexError
        rank = idx + 1 
        # different from __getitem__, it can terminate when node.levels[0].forward.rank==rank
        update, _ = self.find(lambda _,rrank:rrank<rank)
        self.deleteNode(update[0].levels[0].forward, update)

if __name__ == "__main__":
    print("\ntest case 1\n")
    z = Skiplist()
    z.insert((9, 'a'))
    z.insert((2, 'b'))
    z.insert((1, 'd'))
    z.insert((4, 'c'))
    z.insert((5, 'e'))
    print(z.delete((1, 'a')))
    print(z.delete((1, 'a')))
    z.insert((0, 'g'))
    print(z)
    print("\ntest case 2\n")
    s = Skiplist()
    for e in 1,2,3,3,2,3,4,2,3:
        s.insert(e)
    print(s[2])
    print(s)
    print(s.bisect_left(100))
    print(s.bisect_left(-100))
    print(s.bisect_right(100))
    print(s.bisect_right(-100))
    print(s.bisect_left(2))
    print(s.bisect_right(2))
    print(list(s))
    
    