from functools import cache
from math import inf
def solve(mat):
    n,m=len(mat), len(mat[0])

    @cache
    def adj_cells(ux, uy):
        """ yield adjacent cells that in bounds """
        # top tr right rd down dl left lt
        # (-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)
        # top right down left 
        ret = []
        for dx,dy in (-1,0),(0,1),(1,0),(0,-1):
            x,y = ux+dx,uy+dy
            if 0<=x<n and 0<=y<m: # and mat[x][y]
                ret.append((x,y))
        return ret
    
    def bfs(start: list):
        """ dijkstra(bfs) start at `start`, on `mat` """
        q = start[:]
        dis = [[inf]*m for _ in range(n)]
        for x,y in start:
            dis[x][y] = 0

        d = 0 
        while q:
            pq = q
            q = []
            for x, y in pq:
                # d is distance from (x,y) to start
                for nx,ny in adj_cells(x, y):
                    if dis[nx][ny] > d+1:
                        q.append((nx, ny))
                        dis[nx][ny] = d+1
            d += 1
        return dis


def spiral_traverse(mat):
    """
    spiral matrix generator
    start at topleft
    clockwise
    """
    m,n=len(mat),len(mat[0])
    maxl = (min(m,n)+1)//2
    for l in range(maxl):
        h = m - l*2
        w = n - l*2
        if w==1:
            # right
            for i in range(h):
                yield l+i,l
        elif h==1:
            # down
            for i in range(w):
                yield l,l+i
        else:
            # topleft: l,l
            # topright: l,l+w-1
            # bottomright: l+h-1,l+w-1
            # bottomleft: l+h-1,l
            x = y = l
            # go right
            for _ in range(w-1):
                yield x,y
                y+=1
            # go down
            for _ in range(h-1):
                yield x,y
                x+=1
            # go left
            for _ in range(w-1):
                yield x,y
                y-=1
            # go up
            for _ in range(h-1):
                yield x,y
                x-=1