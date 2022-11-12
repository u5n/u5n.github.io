# def crossed_backedge(G):
#     """
#     of undirected 
#     """
#     n = len(G)

def find_bridges(adj):
    """ des:
        find bridge in undirect grpah use tarjan algorithm
    args:
        adj: undirect graph store with adjacent list
    algo:
        iterate every edge once to find all bridges
    test:@lc#1192
    """
    n = len(adj)
    pre = [-1]*n # preorder sequence
    
    # u -> MIN{u; u can reach u through any outward_span_edge and only one inward_back_edge} 
    low = [-1]*n 

    preid = 0
    bridges = [] 
    def dfs(pu, u):
        nonlocal preid
        low[u] = pre[u] = preid; preid += 1

        for v in adj[u]:
            if pre[v] == -1:
                dfs(u, v)

                low[u] = min(low[u], low[v])
                if low[v] == pre[v]:
                    bridges.append((u, v))

            # since it's undirect graph, parallel edge (v,pu) in adjacent list should be ignore
            elif v!=pu:
                """
                if inroot back_edge: 
                  assert pre[v] == low[v]
                if outroot back_edge: 
                  assert pre[v] > low[u]
                  therefore invalid
                """
                low[u] = min(low[u], pre[v])

    for u in range(n):
        if pre[u]==-1:
            dfs(None, u)
    
    return bridges
