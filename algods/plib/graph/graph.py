"""
TOC
    bfs
    dijkstra
    dijkstra_matrix
    bellmanford
    topo_sort
    read_graph_from_std
    get_raw_edges
    eulerian_circuits_directed
    eulerian_path_directed
    eulerian_path_undirected
convention
    vertices numbered from `0` to `n-1`
    `G` is graph adjacent list whose length is `n`, type is `list`
"""
from collections import deque
from typing import *
from math import *
from heapq import *

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

def bfs(G, start: Iterable):
    """ bfs traverse on graph adjacent list `G`
    can also be used to find shortest path length 
    """
    q = deque(start)
    dis = [None]*len(G)
    for e in start:
        dis[e] = 0
    while q:
        u = q.popleft()
        yield u
        for v in G[u]:
            if dis[v] is None:
                dis[v] = dis[u] + 1
                q.append(v)
    
def dijkstra(G, start: Iterable):
    """ single/multi source shortest path in graph adjacent list `G`
    """
    dis = [inf]*len(G)
    pq = []
    for u in start:
        heappush(pq, (0, u))
        dis[u] = 0
    while pq:
        cost, u = heappop(pq)
        if cost > dis[u]: continue
        for v,w in G[u]:
            newcost = dis[u] + w
            if dis[v] > newcost:
                heappush(pq, (newcost, v))
                dis[v] = newcost
    return dis

def dijkstra_matrix(G, start: Iterable):
    """ single/multi source shortest path in graph adjacent matrix `G`
    """
    n = len(G)
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
            dis[v] = min(dis[v], dis[u] + G[u][v])
    return dis


def topo_sort(G):
    """ topological sort for graph adjacent list `G` """
    n = len(G)
    ind = [0]*n
    for u in range(n):
        for v in G[u]:
            ind[v]+=1
    
    q = deque()
    for u in range(n):
        if ind[u]==0:
            q.append(u)
    
    ret = []
    while q:
        u = q.pop()
        ret.append(u)
        for v in G[u]:
            ind[v]-=1
            if ind[v]==0:
                q.append(v)
    
    if len(ret)==n:
        return ret
    raise Exception("not DAG")

def eulerian_circuits_directed(G, n_edges):
    """ a more commonly used version, the `eulerian_path_directed` covers this function
    but this is shorter, and has side effect that clear `G` (so that `G` can be reused in competitve algorithm)
    """
    ret = deque([0])
    rshift = 0
    while n_edges:
        u = ret[-1]
        if G[u]:
            ret.append(G[u].pop());  n_edges -= 1
        else:
            ret.rotate(); rshift += 1
    ret.rotate(-rshift)
    return ret

    

def eulerian_path_directed(G):
    """ assume G is strongly connected and has 2 or 0 vertice@u that `deg[u]!=0`
    output a eulerian path/circuit represent use nodes
    """
    n = len(G)
    poi = [-1]*n # u -> edges G[u][poi[u]+1:] is deleted
    deg = [0]*n # u -> outdegree[u] - indegree[u]
    n_edges = 0

    for u in range(n):
        poi[u] = len(G[u])-1
        for v in G[u]:
            deg[u] += 1
            deg[v] -= 1
            n_edges += 1
    
    for start in range(n):
        if deg[start] == 1:
            break

    ret = deque([start])
    rshift = 0
    while n_edges:
        u = ret[-1]
        if poi[u]>=0:
            v = G[u][poi[u]]
            ret.append(v)
            n_edges -= 1; poi[u] -= 1
        else:
            ret.rotate(); rshift += 1
    ret.rotate(-rshift)
    return ret

def eulerian_path_undirected(G):
    """ assume G is connected and has 2 or 0 vertices that has even degree`
    output a eulerian path/circuit represent use nodes
    """
    n = len(G)
    poi = [-1]*n
    rmv = [set() for _ in range(n)] # mark edge that is removed
    deg = [0]*n
    n_edges = 0
    
    for u in range(n):
        poi[u] = len(G[u])-1
        for v in G[u]:
            deg[u] += 1
            deg[v] += 1
            n_edges += 1
    
    for start in range(n):
        if deg[start]%2!=0:
            break
    
    ret = deque([start])
    rshift = 0
    while n_edges:
        u = ret[-1]
        while poi[u] >= 0 and poi[u] in rmv[u]: poi[u] -= 1
        if poi[u] >= 0:
            v = G[u][poi[u]]
            ret.append(v)
            rmv[v].add(u); n_edges -= 1; poi[u] -= 1
        else:
            ret.rotate(); rshift += 1

    ret.rotate(-rshift)
    return ret
    

def read_graph_from_std(matrix=False, directed=False, weighted=False):
    """ for csacademy graph editor """
    n,m=map(int, input().split())
    # read m edges with format `f"{from} {to} {weight}"`
    if matrix:
        if weighted:
            G = [[float('inf')]*n for _ in range(n)]
        else:
            G = [[0]*n for _ in range(n)] # whether exist
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