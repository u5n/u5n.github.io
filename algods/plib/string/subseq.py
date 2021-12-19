from collections import defaultdict
import string
def next_char(s):
    """ next[i][ch] -> MIN{j; s[j]==ch; j>=i; default=n+1} 
    """
    n = len(s)
    next = [defaultdict(lambda:n) for _ in range(n+1)]
    for c in string.ascii_lowercase:
        ic = n
        for i in reversed(range(n)):
            if s[i]==c:
                ic = i
            next[i][c] = ic
    return next
