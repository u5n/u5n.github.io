import random
import math
import operator

class SkiplistNode:
    __slots__ = 'levels','val'
    def __init__(self, nlevel: int, val):
        self.val = val
        # (forward, num_steps_reach_next)
        self.levels = [[None, 42] for _ in range(nlevel)]
    def __str__(self): return str(self.val)

class SkiplistArray:
    """
    the interface is `builtins.list`
    the design target: 
        as quick as possible
    however, this is far slower than `builtins.list` when n is rather small(<=100000)
    """
    __slots__ = 'senhead', 'sz', 'maxlvl', 'lvllim', 'riseprob'
    def __init__(self, lvllim=32, riseprob=0.3, A=[]):
        self.lvllim, self.riseprob = lvllim, riseprob
        self.senhead = SkiplistNode(lvllim, '$')
        if not A:
            self.sz = self.maxlvl = 0
        else:
            # O(n/(1-riseprob))
            n = len(A)
            createdNode =[None]*n
            maxlvl = 0
            mul = int(1/riseprob)
            step = 1
            while step <= n: 
                maxlvl += 1
                step *= mul
            step //= mul
            for ilvl in reversed(range(maxlvl)):
                cur = self.senhead
                for Ai in range(step-1, n, step):
                    if createdNode[Ai] is None:
                        createdNode[Ai] = SkiplistNode(ilvl+1, A[Ai])
                    
                    cur.levels[ilvl][0] = createdNode[Ai]
                    cur.levels[ilvl][1] = step
                    cur = createdNode[Ai]
                step //= mul

            self.sz = n
            self.maxlvl = maxlvl
        
    def getNodeByRank(self, rank):
        x = self.senhead
        x_rank = -1 # senhead rank is -1
        for i in reversed(range(self.maxlvl)):
            while x.levels[i][0]!=None and x_rank+x.levels[i][1]<=rank:
                x_rank += x.levels[i][1]
                x = x.levels[i][0]
            if x_rank==rank: return x
        raise Exception(".getNodeByRank: invalid rank")


    def __template_getPrevByRank(self, rank):
        # this is code template
        x = self.senhead
        x_rank = -1
        for i in reversed(range(self.maxlvl)):
            while x.levels[i][0]!=None and x_rank+x.levels[i][1]<rank:
                x_rank += x.levels[i][1]
                x = x.levels[i][0]
            # prevnodes[i] = x
            # prevnodes_rank[i] = x_rank
    
    def deleteByRank(self, rank):
        assert 0<=rank<self.sz
        x = self.senhead
        x_rank = -1
        toremove = None
        for i in reversed(range(self.maxlvl)):
            while x.levels[i][0]!=None and x_rank+x.levels[i][1]<rank:
                x_rank += x.levels[i][1]
                x = x.levels[i][0]
            if toremove is None and x_rank + x.levels[i][1] == rank:
                toremove = x.levels[i][0]
            
            if toremove:
                x.levels[i][0] = toremove.levels[i][0]
                x.levels[i][1] += toremove.levels[i][1] - 1
            else:
                x.levels[i][1] -= 1
            
        while len(toremove.levels)==self.maxlvl and self.senhead.levels[self.maxlvl-1][0] == None:
            self.maxlvl -= 1
        self.sz -=1 
        return toremove
            

    def pop(self, rank): return self.deleteByRank(rank).val
    def insert(self, rank, val):
        if rank > self.sz: rank = self.sz
        newnode_nlvl = min(1-int(math.log(1/random.random(), self.riseprob)), self.lvllim)
        newnode = SkiplistNode(newnode_nlvl, val)
        x = self.senhead
        x_rank = -1
        for i in reversed(range(max(self.maxlvl, newnode_nlvl))):
            while x.levels[i][0]!=None and x_rank+x.levels[i][1]<rank:
                x_rank += x.levels[i][1]
                x = x.levels[i][0]
            
            if i >= newnode_nlvl:
                x.levels[i][1] += 1
            else:
                newnode.levels[i][0] = x.levels[i][0]
                newnode.levels[i][1] = x.levels[i][1] - (rank - x_rank) + 1
                x.levels[i][0] = newnode
                x.levels[i][1] = rank - x_rank
        
            
        self.maxlvl = max(self.maxlvl, newnode_nlvl)
        self.sz += 1
        

    def __getitem__(self, rank): return self.getNodeByRank(rank).val
    def __setitem__(self, rank, val): self.getNodeByRank(rank).val = val
    def __delitem__(self, rank): self.pop(rank)
    def __len__(self): return self.sz
    def __iter__(self):
        # iterate nodes
        x = self.senhead.levels[0][0]
        while x:
            yield x.val
            x=x.levels[0][0]
    def iterateNode(self):
        x = self.senhead.levels[0][0]
        while x:
            yield x
            x=x.levels[0][0]

    def __eq__(self, oth):
        if self.sz != len(oth): return False
        for v1, v2 in zip(self, oth):
            if v1 != v2: return False
        return True


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
            '\n'+"\n".join(sbuilder)+'\n'+'-'*30 +'\n'
