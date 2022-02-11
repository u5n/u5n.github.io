from collections import defaultdict
import string
def next_char(s, prev=False):
    """ para: 
        s: assume only contain lowercases
        prev: if set True, return the `prev` array
    ret: next:
        i,ch -> MIN{j; ord(s[j])-97==ch; j>=i; default=n} 
    """
    n = len(s)
    next = [None]*n
    if prev:
        it = range(n)
        next_arr = [-1]*26
    else:
        it = reversed(range(n))
        next_arr = [n]*26
    for i in it:
        e = ord(s[i])-97
        next_arr[e] = i
        next[i] = tuple(next_arr)
    return next