"""
_
    TOC:
        numberof
        outline_lower
        outline_upper
            generalization of sliding window
monotonic matrix: 
    2d array, row descending, column ascending
"""

def numberof(mat, f):
    """ 
    parameters: 
        f: unary bool function
        mat: 
            np.vectorize(f)(mat) is monotonic
                example:
                    [[T,T,F,F,F],
                     [T,T,T,T,F],
                     [T,T,T,T,T]]

    """
    x = y = ans = 0
    nx, ny = len(mat), len(mat[0])
    while x < nx and y < ny:
        if f(mat[x][y]):
            ans += nx - x
            y += 1
        else:
            x += 1

    return ans

def outline_lower(mat, f):
    """
    parameters: 
        f: unary bool function
        mat: np.vectorize(f)(mat) is monotonic
    """
    x = y = 0 
    nx, ny = len(mat), len(mat[0])
    while x < nx and y < ny:
        if f(mat[x][y]):
            yield x,y
        if y+1<ny and f(mat[x][y+1]):
            y += 1
        else:
            x += 1

def outline_upper(mat, f):
    """
    parameters: 
        f: unary bool function
        mat: np.vectorize(f)(mat) is monotonic
    """
    x = y = 0
    nx, ny = len(mat), len(mat[0])
    while x < nx and y < ny:
        if not f(mat[x][y]):
            yield x,y
        if x+1<nx and not f(mat[x+1][y]):
            x += 1
        else:
            y += 1