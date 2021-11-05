import string
from collections import defaultdict

class SubseqQuery:
    """
    input string s
    output an algorithm
        input string t
        output whether t is subseq of s
    """
    def __init__(self, s):
        n = len(s)
        next = [defaultdict(lambda:n) for _ in range(n+1)]
        for c in string.ascii_lowercase:
            ic = n
            for i in reversed(range(n)):
                if s[i]==c:
                    ic = i
                next[i][c] = ic
        self.n,self.next = n,next
    def query(self, t, sta=0, end=None):
        """ check whether t is subseq of s[sta:end] """
        if end==None: end = self.n
        for c in t:
            sta = self.next[sta][c]
            if sta>=self.n: return False
            sta += 1
        return True



def SupseqQuery(s, dic):
    chtopoi = defaultdict(list)
    nw = len(dic)
    for wi in range(nw):
        chtopoi[dic[wi][0]].append((wi,0))
    for c in s:
        pois = chtopoi[c]
        chtopoi[c] = []
        for wi,wii in pois:
            if wii < len(dic[wi])-1:
                chtopoi[dic[wi][wii+1]].append((wi,wii+1))
            else:
                yield dic[wi]