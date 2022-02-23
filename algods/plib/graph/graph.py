"""
TOC
    get_raw_edges
    bfs
    dijkstra
    dijkstra_matrix
    bellmanford
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
    """ single/multi source shortest path in graph adjacent list `G` """
    dis = [inf]*len(adj)
    pq = []
    for u in start:
        heappush(pq, (0, u))
        dis[u] = 0
    while pq:
        cost, u = heappop(pq)
        if cost > dis[u]: continue
        for v,w in adj[u]:
            newcost = dis[u] + w
            if dis[v] > newcost:
                heappush(pq, (newcost, v))
                dis[v] = newcost
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
    n = len(adjmat)
    dp = copy.deepcopy(adjmat)
    for med in range(n):
        for i in range(n):
            for j in range(n):
                dpv = dp[i][med] + dp[med][j]
                if dpv < dp[i][j]:
                    dp[i][j] = dpv
    return dp
    
