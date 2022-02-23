from math import *
___ = (lambda s: exec(f"raise Exception('{s}')"))("The code has to be finished by the programmer")

def partition_solver(f1,f2, f3=None):
    """
    des: return the dp to solve problem
    arg:
        f2: add|max|min (use `add` instead of `sum`)
        f3: any function
    problem des:
        input A,k
        output: [maximize|minimize]@f1{f2( f3(part) for part in A2); A2 is a partition of A; len(A2)<=k; A2[i] is not empty}
    """
    f1_ie = inf if f1 is min else -inf
    f3_cac = None; assert f3_cac != None
    def dp(A, k):
        """ `f3` can't be used directly, mostly it need preprocess to become a O(1) operation
        dp:
            dp[i][vk] means ~problem(A[:i], vk)
        border condition:
            old border condition: 
                1. if i==0 and vk==0: allow with zero cost 
                2. elif vk==0: disallow, (meaningless)
                3  elif vk > i: disallow, (can't be empty)
            so consider `vk` from 1 , and restrict range of `vk` and `i` and `i2`
            new border condition:
                1. vk == 1: calc directly use `f3_cac`
        time: O(n^2*k)
        """
        
        n = len(A)
        dp = [None]*(n+1)
        # when vk == 1
        for i in range(1, 1+n): dp[i] = f3_cac(0,i)
        for vk in range(2, 1+k):
            dpp = dp
            dp = [f1_ie]*(n+1)
            for i in range(vk, 1+n):
                for i2 in reversed(range(vk-1, i)): # filter those vk > i
                    # dp[vk][i] = min(dp[vk][i], f2(f3_cac(i2, i), dp[vk-1][i2]))
                    dp[i] = f1(dp[i], f2(f3_cac(i2,i), dpp[i2]))
    
    return dp

def interval(n):
    """ des: code snippets to for interval dp 
    dp:
        def: dp[l][r] is ~problem(A[l:r])
        border: dp[l][l] = 0
        order: big interval rely small interval
    """
    # dp = [[___]*(n+1) for _ in range(n+1)]
    # the ___ should be dp[l][l]
    dp = [___]*n
    for r in range(1, 1+n):
        for l in reversed(range(r)):
            """ calc dp[l][r] use dp[l+1][r] and dp[l][r-1] """
            dp[l] = ___(dp[l+1], dp[l])
    return dp[0]