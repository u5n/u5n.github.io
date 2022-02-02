"""
TOC
    get_raw_edges
    bfs
    dijkstra
    dijkstra_matrix
    bellmanford
    topo_sort
    read_graph_from_std
    get_raw_edges
    
convention
    vertices numbered from `0` to `n-1`
    `G` is graph adjacent list whose length is `n`, type is `list`
"""
from collections import deque
from typing import *
from math import *
from heapq import *

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

    

def read_graph_from_std(matrix=False, directed=False, weighted=False):
    """ construct a graph from a codeforce style stdinput"""
    n,m=map(int, input().split())
    # read m edges with format `f"{from} {to} {weight}"`
    if matrix:
        if weighted:
            G = [[float('inf')]*n for _ in range(n)]
        else:
            G = [[0]*n for _ in range(n)]
        for _ in range(m):
            if weighted:
                fr,to,wei = map(int, input().split())
                G[fr][to] = wei
                if not directed: G[to][fr] = wei
            else:
                fr,to = map(int, input().split())
                G[fr][to] = 1
                if not directed: G[to][fr] = 1
    else:
        G = [[] for _ in range(n)]
        for _ in range(m):
            if weighted:
                fr,to,wei = map(int, input().split())
                G[fr].append((to, wei))
                if not directed: G[to].append((fr, wei))
            else:
                fr,to = map(int, input().split())
                G[fr].append(to)
                if not directed: G[to].append(fr)
    return G

def get_raw_edges(G, weighted=False):
    """ can be used to draw a graph https://csacademy.com/app/graph_editor/ """
    n = len(G)
    ret = []
    if weighted:
        for u in range(n):
            for v,w in G[u]:
                ret.append(f'{u} {v} {w}')
    else:
        for u in range(n):
            for v in G[u]:
                ret.append(f'{u} {v}')
    return "\n".join(ret)