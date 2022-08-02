class adjll:
    __slots__ = 'n', 'end', 'head', 'm', 'add', 'edges'
    def __init__(self, n, weighted=False):
        self.head = [-1]*n

        self.end = []
        self.n = n
        self.m = 0
        if weighted: 
            self.add = self.__add_weight
            self.edges = self.__edges_weight
        else:
            self.add = self.__add
            self.edges= self.__edges
    
    def __add(self, u, v):
        self.end.append([v, self.head[u]])
        self.head[u] = self.m
        self.m += 1

    def __add_weight(self, u, v, w):
        self.end.append([v, w, self.head[u]])
        self.head[u] = self.m
        self.m += 1

    def __edges(self, u):
        end = self.end
        eid = self.head[u]
        
        while eid!= -1:
            yield end[eid][0]
            eid = end[eid][1]

    def __edges_weight(self, u):
        end = self.end
        eid = self.head[u]

        while eid!= -1:
            yield end[eid][0], end[eid][1]
            eid = end[eid][2]
    
    def __len__(self): return self.n


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