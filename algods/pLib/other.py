from collections import deque
from types import List
"""
TOC:
    find inversion pairs
    mergesort
    cyclesort
    quicksort
    pivot partition into three interval
    pivot partition into two interval
    
    2d point class
    
    {matrix}
        transpose
        square matrix transpose_inplace

        mul_mod
        pow_mod
        spiral matrix traverse by layer
"""
def cyclesort(A):
    n = len(A)
    for i in range(n):
        while True:
            numles = 0
            for j in range(i+1,n):
                if A[j]<A[i]:
                    numles+=1
            if numles==0: break
            
            while A[i+numles] == A[i]: numles += 1
            A[i+numles],A[i]=A[i],A[i+numles]

def quicksort(A, l, r):
    """
    quicksort subroutine, 
    call quicksort(A,0,len(A)) to sort A inplace
    """
    if r-l<=1: return
    p1,p2 = three_partition(A,l,r)
    quicksort(A,l,p1)
    quicksort(A,p2,r)

def three_partition(A,l,r):
    """
    pivot partition into three interval
    interval: [,)
    assert: not empty interval
    """
    i = j = l
    k = r-1
    pivot = A[r-1]
    while j<=k:
        # [l:i] < ; [i:j] == ; [k:] >
        if A[j]<pivot:
            A[j],A[i]=A[i],A[j]
            i+=1
            j+=1
        elif A[j]==pivot:
            j+=1
        else:
            A[j],A[k]=A[k],A[j]
            k-=1
    return i,j
def partition(A, l, r):
    """
    pivot partition into two interval
    interval: [,)
    assert: not empty interval
    """
    i = l
    pivot = A[r-1]
    for j in range(l,r):
        # [l:i] <= ; [i:j] >
        if A[j]<=pivot:
            A[i],A[j]=A[j],A[i]
            i+=1
    return i

from points import V
def _namespace_matrix():
    Mod = int(1e9+7)
    def mul_mod(matL, matR):
        m,n,p = len(matL), len(matR), len(matR[0])
        assert n==len(matL[0])
        ret = [[None]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                val = 0
                for k in range(n):
                    val = (val + matL[i][k]*matR[k][j])%Mod
                ret[i][j] = val
        return ret
    def mat_pow_mod(mat: List[List[int]], b) -> List[List[int]]:
        n = len(mat)
        ret= [ [0]*n for _ in range(n) ]
        for i in range(n): ret[i][i]=1
        
        while b:
            if b%2:
                ret = mul_mod(ret, mat)
            mat = mul_mod(mat, mat)
            b>>=1
        return ret
    def square_rotate_inplace2(mat, tim=1):
        """ 试着用中心对称写 """
    def square_rotate_inplace(mat, tim=1):
        """
        rotate clockwise 90deg `tim` times
        or `mat[:] = np.rot90(mat,-tim).tolist()`
        """
        m = len(mat)
        maxl = (m+1)//2
        di = [V(0,1),V(1,0),V(0,-1),V(-1,0)]
        for l in range(maxl):
            w = m - l*2
            poi = [V(l,l),V(l,l+w-1),V(l+w-1,l+w-1),V(l+w-1,l)]
            for d in range(w-1):
                newpoi = [poi[i]+di[i]*d for i in range(4)]
                print(newpoi)
                dq = deque([newpoi[i].getAsIndex(mat) for i in range(4)])
                dq.rotate(tim)
                for i in range(4):
                    newpoi[i].setAsIndex(mat, dq.popleft())

    def square_transpose_inplace(mat):
        m = len(mat)
        for i in range(m):
            for j in range(i+1,m):
                mat[i][j],mat[j][i]=mat[j][i],mat[i][j]
        return mat

    def transpose(mat):
        m,n = len(mat),len(mat[0])
        ans = [[0]*m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                ans[j][i]=mat[i][j]
        return ans

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
                


