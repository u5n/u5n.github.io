def border(s):
    """ 
    B[i] is length of longest proper border of s[i+1] 
    where border means a string that is the prefix and suffix of s[:i+1]
    """
    n = len(s)
    B = [None] * n
    B[0] = ml = 0
    for i in range(1, n):
        # loop inv: ml is B[i-1]
        while ml > 0 and s[i] != s[ml]:
            ml = B[ml - 1]
        if s[i] == s[ml]:
            ml += 1
        B[i] = ml
    return B
    
class KmpQuery:
    def __init__(self, pattern):
        self.B = border(pattern)
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

# def search_wild(T, P):
#     """ P maybe contain asterisks, such as 'abc*ef', 
#     '*' can be used to match any single char 
#     time: O(|P|+k|T|), O(k)
#     """
#     np = len(P)
#     nt = len(T)

#     Ps = []

#     prv = 0
#     for cur in range(np + 1):
#         if cur == np or P[cur] == '*':
#             if cur - prv > 0:
#                 Ps.append([prv, search(T, P[prv:cur]), None])
#             prv = cur + 1
#     nk = len(Ps)
#     for iT in range(nt - np + 1):
#         for ik in range(nk):
#             while Ps[ik][2] == None or (Ps[ik][2] < iT + Ps[ik][0]):
#                 try:
#                     Ps[ik][2] = next(Ps[ik][1])
#                 except StopIteration:
#                     return

#             if Ps[ik][2] != iT + Ps[ik][0]:
#                 break

#         else:
#             # the length of matched substring is determined
#             yield iT


# def search_wild_match2(T, P):
#     """ P maybe contain asterisks, such as 'abc*ef', 
#     '*' can match any word with any length including 0
#     time:O((|T|/k)^k)
#     """
#     np = len(P)
#     Ps = []

#     prv = 0
#     for cur in range(np + 1):
#         if cur == np or P[cur] == '*':
#             if cur - prv > 0:
#                 indices = list(search(T, P[prv:cur]))
#                 if len(indices)==0: return
#                 Ps.append([cur - prv, indices, 0])
#                 # Ps[i][2] is index on Ps[i][1]
#                 # Ps[i][1][ Ps[i][2] ] is index on T
#             prv = cur + 1
#     # similar to combinations
#     nk = len(Ps)
#     if nk == 0:
#         # this is meaningless and time complexity become O(2^t)
#         raise Exception("not valid")

#     def iToiT(i):
#         return Ps[i][1][ Ps[i][2] ]
#     for i in range(1, nk):
#         while Ps[i][2] < len(Ps[i][1]) and iToiT(i) < iToiT(i-1) + Ps[i - 1][0]:
#             Ps[i][2] += 1
#         if Ps[i][2] == len(Ps[i][1]):
#             return
    
#     while True:
#         yield tuple(Ps[i][1][Ps[i][2]] for i in range(nk))
#         last = None
#         for i in reversed(range(nk)):
#             if Ps[i][2] < len(Ps[i][1]) - 1:
#                 last = i
#                 break
#         else:
#             break

#         Ps[last][2] += 1
#         for i in range(last + 1, nk):
#             while Ps[i][2] < len(Ps[i][1]) and iToiT(i) < iToiT(i-1) + Ps[i - 1][0]:
#                 Ps[i][2] += 1
#             if Ps[i][2] == len(Ps[i][1]):
#                 return
