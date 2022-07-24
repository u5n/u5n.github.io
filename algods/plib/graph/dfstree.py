def crossed_backedge(G):
    """
    of undirected 
    """
    n = len(G)

def tarjan_bridge(adj):
    """ undirect graph with adjacent list
    """
    n = len(adj)
    pre = [-1]*n # preorder sequence
    low = [-1]*n # u -> MIN{u; u can reach u through downward_span_edge and back edge} 

    uuid = 0
    bridges = [] 
    def dfs(pu, u):
        nonlocal uuid
        pre[u] = uuid; uuid += 1

        low[u] = pre[u]
        for v in adj[u]:
            if pre[v] == -1:
                dfs(u, v)

                low[u] = min(low[u], low[v])
                if low[v] == pre[v]:
                    bridges.append((u, v))

            # since it's undirect graph, parallel edge in adjacent list should be ignore
            elif v!=pu:
                low[u] = min(low[u], pre[v])

    for u in range(n):
        if pre[u]==-1:
            dfs(u, u)

    return bridges
