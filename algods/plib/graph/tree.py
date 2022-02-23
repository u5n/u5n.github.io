"""
convention 
    the tree stored in adjacent list, which is a out-tree
    the tree root has id `0`
TOC:
    postorder
    to_array_preorder
    binary_lift
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
                yield from postorder_dfs(v)
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
    """ in preorder seq@P, every subtree@u is a continuous subarrays 
    ret: mp: u (node_number in G) |-> P[mp[u][0]:mp[u][1]] correspond subtree at u
    impl: iterative postorder use breakpoint
    `preorder[mp[u][0]:mp[u][1]]` """
    n = len(G)
    sta = [[0, 0]] # breakpoint, vertex
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

def binary_lift(parent):
    """ des: of a tree, query kth(start from 1) ancester of any node 
    para:
        node number from 0 to `len(parent)`
        parent of node `i` is node `parent[i]`
        the tree root at node `0`
    test: @lc#1483
    time: O(nlgn)
    """
    n = len(parent)
    nj = n.bit_length()
    # node i |-> 2**j th(start from 1) ancester of i, if no, map to -1
    dp = [[-1]*n for _ in range(nj)]
    for i in range(1, n): dp[0][i] = parent[i]
    for j in range(1, nj):
        for i in range(1, n):
            pi = dp[j-1][i]
            if pi!=-1: dp[j][i] = dp[j-1][pi]
    def kthAncester_query(u, k):
        while k>0 and u!=-1:
            j = k.bit_length()-1
            u = dp[j][u]
            k -= (1<<j)
        return u
    return kthAncester_query