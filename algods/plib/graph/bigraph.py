from math import inf
def is_bigraph(adj):
    # `-COLOR0`` to get COLOR1
    COLOR0, COLOR1 = -1, 1
    n = len(adj)
    q = []
    colored = [0]*n
    for start in range(n):
        if not colored[start]:
            q.append(start)
            colored[start] = COLOR0
            for u in q:
                for v in adj[u]:
                    if not colored[v]:
                        colored[v] = -colored[u]
                        q.append(v)
                    else:
                        if colored[v] == colored[u]: 
                            return False
    return True


def hungarian_dense(adjmat):
    """ des: hungarian algorithm implement use bfs 
    app: dense graph, bigraph maximum cardinality matching 
    time: O(nl^2 * nr), O(nl+nr)
    """
    ans = 0
    nl, nr = len(adjmat)
    paired_y = [None]*nr
    paired_l = [None]*nr
    def dfs(x):
        for y in range(nr):
            if adjmat[x][y] and not inpath_y[y]:
                inpath_y[y] = True
                if paired_y[y] is None or dfs(paired_y[y]):
                    paired_y[y] = x
                    paired_l[x] = y
                    return True
        return False

    for x in range(nl):
        if paired_l[x] is None:
            # right vertex → whether in augmentpath
            inpath_y = [False]*nr
            ans += dfs(x)
    return ans


def hungarian_weighted_perfect(adjmat):
    """
    _: 
        source: https://github.com/kth-competitive-programming/kactl/blob/master/content/graph/WeightedMatching.h
        todo: understand the principle
    des:
        for a complete bigraph represent use "costmatrix" `adjmat`, find one perfect matching{ sum of edge weight is min }
            adjmat can't contain `math.inf`
        use `-adjmat` to get the maximum sum of edge weight
    assert: len(adjmat) <= len(adjmat[0])
    impl:
        add two sentry, x0=len(adjmat), y0=len(adjmat[0])
    time: O(nx**2 * ny)
    """
    nx,ny = len(adjmat)+1,len(adjmat[0])+1
    lx = [0]*nx
    ly = [0]*ny
    paired_y = [nx-1]*ny
    for x in range(nx-1):
        y0 = ny-1 
        paired_y[y0] = x
        dist = [inf]*ny
        prev = [-1]*ny
        inpath_y = [0]*ny
        while True:
            inpath_y[y0] = True
            x0 = paired_y[y0]
            delta = inf
            for y in range(ny-1):
                if not inpath_y[y]:
                    cur = adjmat[x0][y]-lx[x0]-ly[y]
                    if cur<dist[y]: 
                        dist[y]=cur
                        prev[y]=y0
                    if dist[y]<delta:
                        delta=dist[y]
                        y1=y
            for y in range(ny):
                if inpath_y[y]:
                    lx[paired_y[y]] += delta
                    ly[y] -= delta
                else:
                    dist[y] -= delta
            y0=y1
            if nx-1==paired_y[y0]: break
        
        while y0!=-1:
            y1 = prev[y0]
            paired_y[y0] = paired_y[y1]
            y0 = y1
    
    """
    -ly[-1]: min cost
    [(paired_y[y]-1, y-1) for y in range(1, ny)]: 0-indexed matching coordinate(x,y)
    """
    return -ly[-1]