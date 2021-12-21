from collections import defaultdict
import string
def next_char(s):
    """ 
    assume s only contain lowercases
    next[i][ch] -> MIN{j; ord(s[j])-97==ch; j>=i; default=n+1} 
    """
    n = len(s)
    next = [None]*n
    next_arr = [n]*26
    for i in reversed(range(n)):
        e = ord(s[i])-97
        next_arr[e] = i
        next[i] = tuple(next_arr)
    return next