"""
_
    TOC:
        numberof
        shortestSubarray
            the subarrays implicitly compose a bool monotonic matrix
                the value of each cells
                    is heavy to calculate, can't cumulate like `max` or `sum`
                    can be calculated use math induction if fix one endpoint


monotonic matrix: 
    2d array, row descending, column ascending
"""
import math
def numberof(mat, f):
    """ 
    parameters: 
        f: unary bool function
        mat: 
            np.vectorize(f)(mat) is monotonic
                column ascending
                row descending
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

def shortestSubarray(A):
    """
    test: 
        @lc#727
            unknown time
        @lc#1521 https://leetcode.cn/submissions/detail/326397446/
            O(n^2)
    time:
        O(n^2), but depend on problems
        hardly has worst case 
        hard to construct worst case
    """
    n = len(A)
    def rightUntil(l):
        pass
    def leftUntil(r):
        pass
    l = 0
    ans = math.inf
    while True:
        r = rightUntil(l)
        if r is None: break
        l = leftUntil(r)
        ans = min(ans, (r-l+1))
        l += 1
    return ans