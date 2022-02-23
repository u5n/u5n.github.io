
def read_graph(matrix=False, directed=False, weighted=False):
    """ construct a graph from a codeforces style stdinput """
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

def print_graph(G, weighted=False):
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
    print("\n".join(ret))