from functools import cache
def all_groups(n):
    """ 
    des: 
        divide [0,n-1] into some unlabeled nonempty groups
    time: 
        ~BellB[n], first n (start from 1) [1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975, 678570, 4213597, 27644437 ] (n<=13)
        https://oeis.org/A000110
        all_groups(9); 20ms; 21147
        all_groups(10); 100ms; 115975
        all_groups(11); 750ms; 678570
        all_groups(12); 6700ms; 4213597
    """
    ret = []
    def dfs(i, grps):
        if i==n:
            ret.append(grps)
            return
        for grps_p, grp in enumerate(grps):
            dfs(i+1, grps[:grps_p]+(grp+(i,),)+grps[grps_p+1:])
        dfs(i+1, grps+((i,),))
    dfs(0, tuple())
    return ret

def k_groups(n, k):
    """ 
    des: 
        divide [0,n-1] into k unlabeled nonempty groups 
        related: the "submask" trick of bitmask can divide [0,n-1] into 3 labeled groups in O(3^n)
    time: 
        https://oeis.org/A008277
        1.3e-6s per loop
            k_groups(10, 5) ; 60 ms;  42525
            k_groups(11, 5) ; 300 ms;  246730
            k_groups(12, 5) ; 1800 ms;  1379400
        second stirling number; ~O(k^n)
    """
    ret = []
    if n < k: return ret
    def dfs(i, grps, empty):
        if n-i == empty:
            if i==n:
                ret.append(grps)
            else:
                ret.append(grps[:k-empty] + tuple((i,) for i in range(i,n)))
            return
        for grps_p, grp in enumerate(grps):
            if len(grp)==0:
                dfs(i+1, grps[:grps_p]+((i,),)+grps[grps_p+1:], empty-1)
                break
            else:
                dfs(i+1, grps[:grps_p]+(grp+(i,),)+grps[grps_p+1:], empty)
    dfs(0, (tuple(),)*k, k)
    return ret