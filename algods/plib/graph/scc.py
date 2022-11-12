def scc(adj: "adjacent_arraylist"):    
    """
    currently don't find necessity of using adjacent linkedlist
    """
    n = len(adj)
    
    # vertex u -> |-> the scc id it belong to
    vid_sccid = [None]*n
    # preorder sequence
    pre = [None]*n
    # vertex  u |-> {preorder sequence s; if u has min preorder sequence in its scc, s == u; if u is not min preorder sequence }
    low = [None]*n
    
    insta = [0]*n
    sta = []
    
    preid = 0
    sccid = 0
    sccid_size = []
    
    def dfs(u):
        nonlocal preid, sccid
        pre[u] = low[u] = preid; preid += 1
        sta.append(u); insta[u] = 1
        
        # calc `low`
        for v in adj[u]: # `for v in adj.edges(u):` for adjacent linkedlist
            # is tree edge
            if pre[v] is None:
                dfs(v)
                low[u] = min(low[u], low[v])
            # is back edge
            # is forward edge to same scc as u
            # is cross_edge to same scc as u
            elif insta[v]:
                low[u] = min(low[u], pre[v])
        
        # in this line, `sta` store { v; v in subtree root at u; v in the same scc as `u`}
        
        # has min preorder sequence in a scc
        if pre[u] == low[u]:
            sccid_size.append(0)
            while 1:
                des = sta.pop(); insta[des] = 0
                vid_sccid[des] = sccid
                sccid_size[-1] += 1
                
                if des == u:
                    break
                
            sccid += 1
    
    for u in range(n):
        if pre[u] is None:
            dfs(u)
    
    return vid_sccid, sccid

def condgraph(adj: "adjacent_arraylist"):
    """
    get adjacent arraylist of condensation graph of `adj` 
    """
    vid_sccid, nscc = scc(adj)
    adjc = [[] for _ in range(nscc)]
    vis = set()
    for u in range(len(adj)):
        uscc = vid_sccid[u]
        for v in adj[u]:
            vscc = vid_sccid[v]
            if uscc!=vscc and (uscc,vscc)  not in vis:
                adjc[uscc].append(vscc)
                vis.add((uscc, vscc))
        
    return adjc