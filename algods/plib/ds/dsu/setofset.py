class setofset:
    """
    the set of hashset, don't use parent relationship like dsu
    the element is numbered from 0 to n-1
    operation:
        unite two set
            time: amortized O(lgn)
        
        compare with dsu implement with arraylist(and also the dsu support delete):
            much slower
            can get all elements of a set
    """
    def __init__(self, n):
        self.idx_set = [{i,} for i in range(n)]
    
    def unite(self, l, r):
        # assert: 0<=l<n; 0<=r<n
        idx_set = self.idx_set
        sl = idx_set[l]
        sr = idx_set[r]
        # compare address
        if sl is sr: return False
        if len(sl)>len(sr): sr, sl = sl, sr
        # merge sl into sr
        for idx in sl:
            idx_set[idx] = sr
        sr |= sl
        # python will gc sl if not ref
        return True
    
    def detach(self, i):
        idx_set = self.idx_set
        if len(idx_set[i])>1:
            idx_set[i].remove(i)
            idx_set[i] = {i, }