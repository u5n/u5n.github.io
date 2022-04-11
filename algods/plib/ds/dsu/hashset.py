""" this page implement dsu by a set of hashset
operation
    unite two set
        time: amortized O(lgn)
    make a new set for an element 
        time: O(1)
    iterate all element in from a set s 
        time: O(|s|)
"""

class Dsu:
    """
    the element is numbered in [0,n)
    """
    def __init__(self, n):
        self.idx_hs = [{i} for i in range(n)]
    
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
        # del sl
        return True
        
    def detach(self, i):
        if len(self.idx_hs)>1:
            self.idx_hs[i].remove(i)
            self.idx_hs[i] = {i, }