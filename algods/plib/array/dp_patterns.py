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
        for sz in range(1, 1+n): dp[sz] = f3_cac(0,sz)
        for vk in range(2, 1+k):
            dpp = dp
            dp = [f1_ie]*(n+1)
            for sz in range(vk, 1+n):
                for i2 in reversed(range(vk-1, sz)): # filter those vk > i
                    # dp[vk][i] = min(dp[vk][i], f2(f3_cac(i2, i), dp[vk-1][i2]))
                    dp[sz] = f1(dp[sz], f2(f3_cac(i2,sz), dpp[i2]))
    
    return dp

def partition_optimizer(A, k):
    """ des: 
        if dp[sz] transition from dp[sz-1][p] + f3(p, sz), and p is monotonic by sz, then apply this method
    assert: f1 = min; f2 = sum
    convention: empty part is not allowed
    test: @lc#1478
    """
    f3 = ___
    n = len(A)
    dp = [None]*(n+1)
    ndp = [None]*(n+1)
    # divide into one group
    for sz in range(1, 1+n): dp[sz] = f3(0, sz)

    def push(sz_l, sz_r, p_l, p_r):
        """ both closed interval"""
        if sz_l > sz_r: return
        sz_m = (sz_l + sz_r+1)//2
        p, p_cost = p_l, dp[p_l] + f3(p_l, sz_m)
        for can_p in range(p_l+1, p_r+1):
            if (can_p_cost:= dp[can_p] + f3(can_p, sz_m)) < p_cost:
                p, p_cost = can_p, can_p_cost
        ndp[sz_m] = p_cost
        push(sz_l, sz_m-1, p_l, p)
        push(sz_m+1, sz_r, p, p_r)

    for vk in range(2, 1+k):
        push(vk, n, vk-1, n-1)
        for sz in range(vk-1, n+1): dp[sz] = ndp[sz]
    return dp[n]

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