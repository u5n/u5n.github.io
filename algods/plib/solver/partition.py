from math import *
"""
input A,k
denote: A2: divide `A` into exactly [`k` subarrays]@A2{without overlap; union to `A`; not empty}, 
output: [maximize|minimize]@f1 f2( f3(part) for part in A2)

f2: add|max|min (use `add` instead of `sum`)
f3: any function
"""

def solve(f1,f2, f3=None):
    """ `f3` can't be used directly, mostly it need preprocess to become a O(1) operation
    dp[i][vk] means ~problem(A[:i], vk)
    border: 
        1. if i==0 and vk==0: allow with zero cost 
        2. elif vk==0: disallow, (meaningless)
        3  elif vk >i: disallow, (can't be empty)
    so consider `vk` from 1
    """
    f1_ie = inf if f1 is min else -inf
    def dp(A, k):
        f3_cac = None; assert f3_cac != None
        n = len(A)
        dpl = [None]*(n+1)
        for i in range(1, 1+n): dpl[i] = f3_cac(0,i)
        for vk in range(2, 1+k):
            dpu = [f1_ie]*(n+1)
            for i in range(vk,1+n):
                for i2 in reversed(range(vk-1, i)): # filter those vk > i
                    dpu[i] = f1(dpu[i], f2(f3_cac(i2,i), dpl[i2]))
            dpl = dpu
        return dpl[n]
    return dp