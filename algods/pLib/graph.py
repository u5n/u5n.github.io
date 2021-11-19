from collections import deque
def topo_sort(G):
    """ topological sort for adjacent list graph """
    n = len(G)
    q = deque()
    inds = [0]*n
    for i in range(n):
        for to in G[i]:
            inds[to]+=1
    for i in range(n):
        if inds[i]==0:
            q.append(i)
    
    ret = []
    while q:
        u = q.pop()
        ret.append(u)
        for to in G[u]:
            inds[to]-=1
            if inds[to]==0:
                q.append(to)
    
    if len(ret)==n:
        return ret
    raise Exception("not DAG")

def read_graph(matrix=False, directed=False, weighted=False):
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