# skiplist, for explanation refer to skiplistRank.py
import random
import math
import operator

class SkiplistNode:
    def __init__(self, level: int, val) -> None:
        self.val = val
        self.levels = [None for _ in range(level)]
    def __repr__(self):
        return str(self.val)

class Skiplist:
    def __init__(self, maxlevel=32, p=0.5, opt=operator.lt) -> None:
        self.MAXLEVEL = maxlevel
        self.P = p
        self.header = SkiplistNode(maxlevel, '/')
        self.length = 0
        self.level = 1
        self.ltopt = opt

    def find(self, pred):
        update = [None] * self.level
        x = self.header
        for i in range(self.level - 1, 0 - 1, -1):
            # compare val
            while x.levels[i]!=None and\
                pred(x.levels[i].val):
                x = x.levels[i]
            update[i] = x
        return update

    def insert(self, val):
        update = self.find(lambda l_val: self.ltopt(l_val,val))
        level = min(1-int(math.log(1/random.random(), self.P)), self.MAXLEVEL)
        # for those new levels
        for i in range(self.level, level):
            update.append(self.header)

        self.level = max(self.level, level)
        x = SkiplistNode(level, val)
        for i in range(level):
            x.levels[i] = update[i].levels[i]
            update[i].levels[i] = x
            
        self.length += 1
        return x

    def deleteNode(self, x, update):
        for i in range(len(x.levels)):
            update[i].levels[i] = x.levels[i]

        while self.level > 1 and self.header.levels[self.level-1] == None:
            self.level -= 1
        self.length -=1 
    def delete(self, val):
        update = self.find(lambda lval: self.ltopt(lval,val))
        x = update[0].levels[0]
        if x!=None and self.eq_opt(x.val,val):
            self.deleteNode(x, update)
            # del skiplistNode x
            return 1
        return 0

    def eq_opt(self, lval, val):
        # (not < ) and (not >)
        return not self.ltopt(lval, val) and not self.ltopt(val, lval)

    def bisect_right(self, val):
        update = self.find(lambda lval: not self.ltopt(val, lval))
        return update[0].levels[0]
        
    def bisect_left(self, val):
        update = self.find(lambda lval: self.ltopt(lval,val))
        return update[0].levels[0]
    
# below for debug
    def __iter__(self):
        """ iterate levels[0] in O(n),O(1) """
        x = self.header.levels[0]
        while x:
            yield x
            x=x.levels[0]
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
    if True:
        print("test case 1\n")
        z = Skiplist()
        z.insert((9, 'a'))
        z.insert((2, 'b'))
        z.insert((1, 'd'))
        z.insert((4, 'c'))
        z.insert((5, 'e'))
        assert z.delete((1, 'd')) == 1
        assert z.delete((1, 'd')) == 0
        z.insert((0, 'g'))
        print(z)
        
    if True:
        print("test case 2\n")
        s = Skiplist()
        for e in 1,2,3,3,2,4,2:
            s.insert(e)
        print(s)
        assert s.delete(3)==1
        print(s)
        assert s.delete(3)==1
        print(s)
        assert s.delete(3)==0
        print(s)
        print(s.bisect_left(100))
        print(s.bisect_left(-100))
        print(s.bisect_right(100))
        print(s.bisect_right(-100))
        print(s.bisect_left(2))
        print(s.bisect_right(2))
        print(list(s))
        