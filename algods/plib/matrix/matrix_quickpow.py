"""
    if numpy is not available, use c++
"""
import numpy as np
Mod = int(1e9+7)
def matpow_mod(mat, b):
    """ 
    the normal version
    equiv to `np.power(mat, b)%Mod`(ignore precision problem) 
    assert: mat is square
    time: O(n^3*lg(b))
    """
    n = len(mat)
    ret = np.eye(n, n, dtype=np.uint64) 
    while b:
        if b&1:
            ret = (ret@mat)%Mod
        b >>= 1
        mat = (mat@mat)%Mod
    return ret


def _namespace_quickpow_cached():
    """
    the cached version, use when initial_statement.shape[1] is rather small
    """
    def 得到mat的2的x次幂(mat, nbit):
        """ cache of [mat**(1<<i) for i in range(nbit)] 
        time: O(n^3*nbit)
        """
        ret = [None]*nbit
        ret[0] = mat
        for i in range(1, nbit):
            mat = (mat@mat)%Mod
            ret[i] = mat
        return ret

    def 矩阵快速幂带预处理(mat, b, ini, cac):
        """ calc `np.power(mat,b) @ ini`
        ni1 = ini.shape[1]
        time: O(log(b)* n^2 * ni1)
        """
        i = 0
        while b:
            if b&1:
                ini = cac[i]@ini%Mod
            b>>=1
            i += 1
        return ini