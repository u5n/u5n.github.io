# union find data structure implement use array
# design for common problems
class UnionFind():
    def __init__(self, n):
        # make_set 0,1,...,n-1
        # parent relation
        self.p = [i for i in range(n)]
        # size of each representative
        self.sz = [1]*n
        self.cnt = n
    def find(self,u):
        if self.p[u]!=u:
            self.p[u]=self.find(self.p[u])
        return self.p[u]

    def union(self,l,r):
        p,sz = self.p, self.sz
        repl,repr = self.find(l), self.find(r)
        if repl!=repr:
            if sz[repl]>sz[repr]:
                repl,repr = repr,repl
            p[repl] = repr
            sz[repr]+=sz[repl]
            self.cnt -= 1
