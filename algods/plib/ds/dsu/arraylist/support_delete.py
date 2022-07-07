from collections import defaultdict
class Dsu:
    """ 
    the parent relationship is maintain by a list A
        of a representative r, `-A[r]` is size of set correspond r
        of a non-representative x, `A[x]` is parent of x
    the element is numbered in [0,n)
    assert: every set that size>=2 will have dummynode as representatives
    """
    __slots__ = 'p', 'n_sets', 'n', 'dummy_uid'
    def __init__(self, n, maxdetachtimes=0):
        self.p = [-1]*(n+n//2+maxdetachtimes//2+2)
        self.dummy_uid = self.n = self.n_sets = n
        
    def find(self, u):
        p = self.p
        if p[u] >= 0:
            p[u] = self.find(p[u])
            return p[u]
        else:
            return u

    def unite(self, oril, orir):
        p = self.p
        l, r = self.find(oril), self.find(orir)
        if l == r: return False
        # when merge two single-element-sets, create a dummy node
        if -1 == p[l] == p[r]:
            p[r] = self.dummy_uid
            r = self.dummy_uid
            self.dummy_uid += 1
        elif p[l] < p[r]: l, r = r, l
            
        p[r] += p[l]
        p[l] = r

        self.n_sets -= 1
        return True

    def detach(self, u):
        p = self.p
        repru = self.find(u)
        if p[repru] < -1:
            p[repru] += 1
            p[u] = -1
            self.n_sets += 1

    def is_repr(self, u): return self.find(u) < 0
    def to_sets(self):
        """
        key is resentative
        value is the set
        """
        ret = defaultdict(list)
        for k in range(self.n):
            ret[self.find(k)].append(k)
        return ret

    def __len__(self): return self.n_sets
    def __repr__(self): return str(self.to_sets().items()).replace("dict_items", "Dsu")

def solve(A):
    n,m = len(A),len(A[0])
    dp = defaultdict(int)
    for nstep in range(n+m-2):
        p1x_range = range(max(0,nstep-m+1),min(nstep+1,n))
        for p1x in p1x_range:
            p1y = nstep - p1x
            if A[p1x][p1y]==-1: continue
            for p2x in range(max(p1x, p1x_range.start), p1x_range.stop):
                p2y = nstep - p2x
                if A[p2x][p2y]==-1: continue
                
                d = max(A[p1x][p1y],A[p2x][p2y])
                dp[p1x,p1y,p2x]=max(
                    dp[p1x-1,p1y,p2x-1],
                    dp[p1x,p1y-1,p2x-1],
                    dp[p1x,p1y-1,p2x],
                    dp[p1x-1,p1y-1,p2x],
                )
    return dp[n-1,m-1,n-1]

class Sys:
    def __init__(self, n):
        self.getfollowing = [None]*n
        self.mapper = [i for i in range(n)]
        self.getfollower = [set() for _ in range(n)]

    def following_with_followers(self, a, b):
        if a == b: return
        getfollower, getfollowing = self.getfollower, self.getfollowing
        fb = getfollower[b]
        fa = getfollower[a]
        if len(fa) < len(fb):
            fb |= fa
            getfollower[b] = fb
        else:
            fa |= fb
            getfollower[b] = fa
        
        if getfollowing[a]:
            getfollower[getfollowing[a]].remove(a)
        getfollowing[a] = b
        getfollower[b].add(a)

        if getfollower[a]: 
            getfollower[a] = set()

    def unfollowing(self, a, b):
        if self.getfollowing[a] == b:
            self.getfollowing[a] = None
            self.getfollower[b].remove(a)