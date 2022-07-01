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
    """ the cached version, faster on query
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

    def 矩阵快速幂右乘ini带预处理(cac, b, ini):
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

def overflow_prob_estimate(n, maxcof = 50, Mod=10**9+7):
    """ n*n matrix @ n*n matrix, estimate prob of overflow when mod `Mod` 
    algorithm: fft
    change discrete uniform distribution [0,Mod) into discrete uniform distribution [0,maxcof]
    """
    import numpy as np
    from scipy.fft import fft, ifft
    # from numpy.fft import fft, ifft
    from itertools import product
    longdouble = np.complex256
    percentage = 2**64 / ((Mod-1)*(Mod-1)*n)
    if percentage >= 1: return 0, 0
    
    def polymul(a,b):
        n = len(a)+len(b)-1
        return np.real(ifft(fft(a, n)*fft(b, n)))

    a = np.zeros((maxcof*maxcof + 1,), longdouble)
    for l,r in product(range(maxcof+1), repeat=2):
        a[l*r] += 1
    a/=sum(a)
    
    b = np.array([1], dtype=longdouble)
    for bit in bin(n)[:1:-1]:
        if '1'==bit:
            b = polymul(b, a)
        a = polymul(a, a)
        print(">", end="")
    
    p = sum(b[int(percentage*maxcof*maxcof*n):]) / sum(b)
    # single element / whole matrix 
    return p, 1-(1-p)**(n*n)