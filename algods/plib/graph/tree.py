"""
convention 
    the tree stored in adjacent list
    the tree root has id `0`
"""
# backup, inferior to postorder
# def rev_bfs(G):
#     """ reverse bfs order to traverse tree, ensure child is visited before parent
#     time 4n space n
#     """
#     n = len(G)
#     bfsseq = [0]
#     for e in range(n):
#         bfsseq.extend(G[bfsseq[e]])

#     for e in reversed(bfsseq):
#         yield e

def postorder(G):
    """ visit node in postorder, ensure child is visited before parent 
    dfs code: 
        def postorder_dfs(u):
        for v in G[u]:
            postorder_dfs(v)
        yield u
    """
    sta = [[0, 0]] # bpt, vertex
    while sta:
        bpt, u = sta[-1]
        if bpt<len(G[u]):
            sta[-1][0] += 1
            sta.append([0, G[u][bpt]])
        else:
            yield sta.pop()[1]
        

def to_array_preorder(G):
    """ in preorder seq, every subtree@u is a continuous subarrays `preorder[mp[u][0]:mp[u][1]]` """
    n = len(G)
    sta = [[0, 0]] # bpt, vertex
    mp = [[-1,-1] for _ in range(n)]
    seq = 0
    while sta:
        bpt, u = sta[-1]
        if bpt==0:
            mp[u][0] = seq
            seq += 1

        if bpt<len(G[u]):
            sta[-1][0] += 1
            sta.append([0, G[u][bpt]])
        else:
            sta.pop()
            mp[u][1] = seq
    return mp

