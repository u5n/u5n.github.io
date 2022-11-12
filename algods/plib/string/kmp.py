def prefix_func(P):
    """ 
    B[i] is length of longest border{string a is border of string b if a is proper prefix of b and proper suffix of b} of s[:i+1] 
    """
    
    n = len(P)
    B = [None] * n
    B[0] = ml = 0
    for i in range(1, n):
        # loop inv: ml is B[i-1]
        while ml > 0 and P[ml] != P[i]:
            ml = B[ml - 1]
        if P[ml] == P[i]:
            ml += 1
        B[i] = ml
    return B

    
class KmpQuery:
    def __init__(self, pattern):
        self.B = prefix_func(pattern)
        self.P = pattern
    def search(self, T):
        """ yield every index j that T[j:j+np]==P, in order """
        P,B = self.P, self.B
        ml = 0
        np, nt = len(P), len(T)
        for i in range(nt):
            while ml > 0 and T[i] != P[ml]:
                ml = B[ml - 1]
            if T[i] == P[ml]:
                ml += 1
                if ml == np:
                    yield i + 1 - np
                    ml = B[ml - 1]
                    # ml = 0 # use this to yield nonoverlap substrings