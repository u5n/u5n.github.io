"""
TOC
    get_raw_edges
    bfs
    dijkstra
    dijkstra_matrix
    spfa
    topo_sort
    
convention
    vertices numbered from `0` to `n-1`
    `G` is graph adjacent list whose length is `n`, type is `list`
"""
from typing import *
from math import *
from heapq import *
from collections import *
import copy

def bfs(G, start: Iterable):
    """ bfs traverse on graph adjacent list `G`
    can also be used to find shortest path length 
    """
    dis = [None]*len(G)
    q = list(start)
    for u in q: dis[u] = 0
    for u in q:
        for v in G[u]:
            if dis[v] is None:
                dis[v] = dis[u] + 1
                q.append(v)
    
def dijkstra(adj, start: Iterable):
    """ single/multi source shortest path in graph adjacent list `G` 
    node numbered from 0 to n-1
    test: @lc#743
    """
    dis = [inf]*len(adj)
    pq = []
    for u in start:
        heappush(pq, (0, u))
        dis[u] = 0
    while pq:
        disu, u = heappop(pq)
        if disu > dis[u]: continue
        for w,v in adj[u]:
            disv = dis[u] + w
            if dis[v] > disv:
                heappush(pq, (disv, v))
                dis[v] = disv
    return dis

def dijkstra_adjmat(M, start: Iterable):
    """ single/multi source shortest path in graph adjacent matrix `G`
    """
    n = len(M)
    dis = [inf]*n
    vis = [0]*n
    for e in start: dis[e] = 0; vis[e] = 1
    while True:
        u = None
        for e in range(n):
            if not vis[e] and (u is None or dis[e] < dis[u]):
                u = e
        if u is None: break
        # elif u == target: return dis[u]
        elif dis[u]==inf: break
        vis[u] = 1

        for v in range(n):
            dis[v] = min(dis[v], dis[u] + M[u][v])
    return dis


def spfa(adj, start):
    """ 
    queue optimized bellman ford
    time: O(VE) """
    n = len(adj)
    dis = [inf]*n
    q = deque(start)
    inq = [False]*n
    for u in start:
        dis[u] = 0
        inq[u] = 1
    while q:
        u = q.popleft(); inq[u] = False
        for w,v in adj[u]:
            disv = dis[u] + w
            if dis[v] > disv:
                dis[v] = disv
                if not inq[v]:
                    q.append(v); inq[v] = True
    return dis

def topo_sort(adj):
    """ topological sort for adjacent list `adj` 
    pop order: bfs order """
    n = len(adj)
    ind = [0]*n
    # enumerate all edges
    for u in range(n):
        for v in adj[u]: 
            ind[v]+=1
    # push all zero indegree vertices
    ret = [u for u in range(n) if ind[u]==0]
    # inplace queue
    for u in ret:
        for v in adj[u]:
            ind[v]-=1
            if ind[v]==0: 
                ret.append(v)
    
    # if len(ret)<n: raise Exception("not DAG")
    return ret

def floydWarshall(adjmat):
    """ glossary: 
        medium edge: the edge in a path; the edge is not first and not last
    """
    n = len(adjmat)
    # shortest path table when you can't use any medium edge
    dp = copy.deepcopy(adjmat)
    for med in range(n):
        # now you can use edge numbered `med`` as medium edge
        for i in range(n):
            for j in range(n):
                dpv = dp[i][med] + dp[med][j]
                if dpv < dp[i][j]:
                    dp[i][j] = dpv
    return dp
