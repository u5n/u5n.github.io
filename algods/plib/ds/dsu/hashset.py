class Dsu:
    """
    implement dsu with a set of hashset
    the element is numbered from 0 to n-1
    operation:
        unite two set
            time: amortized O(lgn)
        
        compare with dsu implement with arraylist:
            much slower
            support detach operation
    """
    def __init__(self, n):
        self.idx_hs = [{i, } for i in range(n)]
    
    def unite(self, l, r):
        # assert: 0<=l<n; 0<=r<n
        idx_hs = self.idx_hs
        sl = idx_hs[l]
        sr = idx_hs[r]
        # compare address
        if sl is sr: return False
        if len(sl)>len(sr): sr, sl = sl, sr
        # merge sl into sr
        for idx in sl:
            idx_hs[idx] = sr
        sr |= sl
        # consider `del sl` ?
        return True
        
    def detach(self, i):
        idx_hs = self.idx_hs
        if len(idx_hs[i])>1:
            idx_hs[i].remove(i)
            idx_hs[i] = {i, }