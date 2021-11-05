from collections import deque
def topo_sort(G):
    """ topological sort for adjacent list """
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