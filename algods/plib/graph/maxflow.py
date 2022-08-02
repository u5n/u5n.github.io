from math import inf

def dinic(adj: adjll, s, t):
    """ 
        find max flow from s to t in graph G
        adj:
            adjacent linkedlist of a residual graph of G 
                store use `dict`
                vertex numbered in [0,len(adj))
                add reverse edge with flow 0
        test: @acw2172
    """
    n= len(adj)
    bfsseq = []
    fi_res = [None]*n

    def get_bfsseq():
        for i in range(n): fi_res[i] = adj.head[i]
        bfsseq[:] = [None]*n; bfsseq[s] = 0
        q = [s]    
        
        for u in q:
            for v, w in adj.edges(u):
                if w and bfsseq[v] is None:
                    bfsseq[v] = bfsseq[u] + 1
                    if v==t: return True
                    q.append(v)
        return False
    
    def findpaths(u, lim):
        """ max flow from `s` to `u` """

        if u == t: return lim
        cs = 0 # cumulative sum of flow from `u` to `t`

        eid = fi_res[u]
        while eid!=-1:
            if cs >= lim: break
            fi_res[u] = eid
            v, w = adj.end[eid][:2]
            
            if bfsseq[v] == bfsseq[u] + 1 and w > 0:
                res = findpaths(v, min(w, lim - cs))
                if res: 
                    adj.end[eid][1] -= res
                    adj.end[eid^1][1] += res
                    cs += res
                else:
                    # don't revisit node v in `findpath`
                    bfsseq[v] = -1

            eid = adj.end[eid][2]
        return cs


    ans = 0
    while get_bfsseq():
        while flow := findpaths(s, inf):
            ans += flow
    return ans