"""
avoid pass dimension as parameter, most function is defined under a function
"""
from functools import cache
from math import inf

def solve(grid):
    n,m=len(grid), len(grid[0])

    @cache
    def adj_cells(ux, uy):
        """ yield adjacent cells that in bounds """
        # top tr right rd down dl left lt
        # (-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)
        # top right down left 
        ret = []
        for dx,dy in (-1,0),(0,1),(1,0),(0,-1):
            x,y = ux+dx,uy+dy
            if 0<=x<n and 0<=y<m: # and grid[x][y]
                ret.append((x,y))
        return ret
    
    
    def bfs(start: list):
        """ bfs start at `start`, on `grid` """
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

def spiral_traverse(grid):
    """
    spiral matrix generator
    start at topleft
    test: @lc#54
    """
    if len(grid)==0: return
    minx, rmaxy, rmaxx, miny  = 0, len(grid[0]),  len(grid), 0
    while True:
        for y in range(miny, rmaxy):
            yield minx,y
        minx += 1
        if minx == rmaxx: break
        
        for x in range(minx, rmaxx):
            yield x, rmaxy-1
        rmaxy -= 1
        if rmaxy == miny: break
        
        for y in reversed(range(miny, rmaxy)):
            yield rmaxx-1, y
        rmaxx -=1 
        if rmaxx == minx: break

        for x in reversed(range(minx, rmaxx)):
            yield x, miny
        miny += 1
        if miny == rmaxy: break
        
    