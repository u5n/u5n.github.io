import random
import math
import operator

class SkiplistNode:
    __slots__ = 'levels','val'
    def __init__(self, level: int, val):
        self.val = val
        self.levels = [None]*level
    def __str__(self):
        return str(self.val)

class Skiplist:
    """
    design: intend a min code size 
    usage: similar to std::multiset in c++
    test: @lc#1206
    """
    __slots__ = 'lvllim', 'riseprob', 'senhead', 'sz', 'maxlvl', 'opt_lt'

    def __init__(self, lvllim=32, riseprob=0.5, opt=operator.lt, optmin = -math.inf):
        self.lvllim = lvllim
        self.riseprob = riseprob
        self.senhead = SkiplistNode(lvllim, optmin)
        self.sz = 0
        self.opt_lt = opt

    def getPrevByCond(self, val, opt=None):
        """ draw a verticial line x=val, then sweep left on each level@l until meet a node which is prevNodePerLvl[l] 
        in layer i, prevNodePerLvl[i] is last node that opt(prevNodePerLvl[i].val, val)
        """
        if opt is None: opt = self.opt_lt
        prevNodePerLvl = [self.senhead] * self.lvllim
        x = self.senhead
        for i in reversed(range(self.lvllim)):
            while x and opt(x.val, val):
                prvx, x = x, x.levels[i]
            prevNodePerLvl[i] = x = prvx
        return prevNodePerLvl

    def add(self, val):
        prevNodePerLvl = self.getPrevByCond(val)
        newnode_level = min(1-int(math.log(1/random.random(), self.riseprob)), self.lvllim)
        x = SkiplistNode(newnode_level, val)
        for i in range(newnode_level):
            x.levels[i] = prevNodePerLvl[i].levels[i]
            prevNodePerLvl[i].levels[i] = x
        self.sz += 1
        return x

    def remove(self, val):
        prevNodePerLvl = self.getPrevByCond(val)
        x = prevNodePerLvl[0].levels[0]
        if x==None or not self.opt_eq(x.val, val):
            return False
        for i in range(len(x.levels)):
            prevNodePerLvl[i].levels[i] = x.levels[i]
        self.sz -=1 
        return True
    
    def count(self, val):
        firstnot = self.getPrevByCond(val)[0].levels[0]
        if firstnot and firstnot.val == val:
            return 1
        return 0


    def opt_le(self, lval, val): return not self.opt_lt(val, lval)
    def opt_eq(self, lval, val): return not self.opt_lt(val, lval) and not self.opt_lt(lval, val)

    def __iter__(self):
        """ iterate levels[0] in O(n),O(1) """
        x = self.senhead.levels[0]
        while x:
            yield x.val
            x=x.levels[0]

    def iterateNode(self):
        """ iterate levels[0] in O(n),O(1) """
        x = self.senhead.levels[0]
        while x:
            yield x
            x=x.levels[0]

    def __len__(self): return self.sz
    def __repr__(self):
        selflevel = self.lvllim
        while selflevel>1 and self.senhead.levels[selflevel-1]==None:
            selflevel -= 1
        mat = [[None]*self.sz for _ in range(selflevel)]
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

        return "-"*5+f" size:{self.sz}  maxlvl:{selflevel} "+'-'*5+\
            '\n'+"\n".join(sbuilder)+'\n'+'-'*30+'\n'

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
        z.add((3, 'e'))
        assert z.remove((1, 'd')) == 1
        assert z.remove((1, 'd')) == 0
        z.add((0, 'g'))
        print(z)
        print(len(z.senhead.levels))
        print(z.getPrevByCond((11212,'a'), z.opt_lt))
    # as multiset
    if d[1]:
        print("test case 2\n")
        z2 = Skiplist()
        for e in 1,2,3,3,2,4,2:
            z2.add(e)
        print(z2)
        assert z2.remove(3)==1
        print(z2)
        assert z2.remove(3)==1
        print(z2)
        assert z2.remove(3)==0
        print(z2)
        print([str(v) for v in z2])
    # as min priority_queue
    if d[2]:
        print("test case 2\n")
        z3 = Skiplist()
        for e in range(10):
            z3.add(e)
        # get heap top
        v = z3.senhead.levels[0].val
        print(v)
        z3.remove(v) # O(lg(n))
        print(z3)
        