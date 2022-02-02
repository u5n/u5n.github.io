from collections import deque
from typing import *

def eulerian_circuits_directed(G, n_edges):
    """ a more commonly used version, the `eulerian_path_directed` covers this function
    but this is shorter, and has side effect that clear `G` (so that `G` can be reused in competitive algorithm)
    """
    ret = deque([0]) # ret = deque([None, 0])
    while n_edges:
        u = ret[-1]
        if G[u]:
            ret.append(G[u].pop());  n_edges -= 1
            # ret.append([u, G[u].pop()])
        else:
            ret.rotate()
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