def solve(mat):
    m,n=len(mat), len(mat[0])

    def adj_cells(ux, uy):
        """ yield adjacent cells that in bounds """
        # top tr right rd down dl left lt
        # (-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)
        # top right down left 
        ret = []
        for dx,dy in (-1,0),(0,1),(1,0),(0,-1):
            x,y = ux+dx,uy+dy
            if 0<=x<m and 0<=y<n: # and mat[x][y]
                ret.append((x,y))
        return ret

    def bfs(start):
        """ single source bfs start at `start`, on `mat` """
        q = [start]
        vis = set(q)
        d = 0 
        while q:
            pq = q
            q = []
            for x, y in pq:
                # d is distance from (x,y) to start
                for nxt in adj_cells(x, y):
                    if nxt not in vis:
                        q.append(nxt)
                        vis.add(nxt)
            d += 1