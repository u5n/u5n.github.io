""" 
_
    TOC:
        binary_search_first
        binary_search_last
        binary_search
        binary_search_continuous
        tarnary_search_continuous
        exponential_search
        exponential_search_last

"""

from this import d


def binary_search_first(l, r, f):
    """
    des:
        input:
            `f` is a monotonic increasing predicate functions defined on integers
                example: "X X X X √ √ √ √"
            the domain of `f` is [`l`,`r`), where `r` is a sentry
        output:
            first `i` in interval [`l`,`r`) such that `f(i)` is True
            if not found, return `r`
    side effect: None
    performance: maybe TLE if `bisect` is available
    """
    assert l<=r
    while l<r:
        m = (r+l)//2
        if f(m): r=m
        else: l=m+1
    return l

# useful
def binary_search_last(l, r, f):
    """ 
    des: 
        example: √ √ √ √ X X X X 
        find last `x` in (`l`,`r`] that `f(x)`; if not found return `l`
    """
    assert l<=r
    while l<r:
        m = (r+l+1)//2
        if f(m): l=m
        else: r=m-1
    return l

def binary_search(l, r, f):
    """ f is an increasing function in discrete interval [l,r], 
    return the zero point of f if not found, return None """
    while r-l>=0:
        m = (l+r)//2
        ret= f(m)
        if ret ==0: return m
        elif ret>0: r = m-1
        else: l = m+1
    return None

def binary_search_continuous(l, r, f, precision=1e-9):
    """ f is an increasing continuous function in [l,r], return the approximate zero point of f 
    """
    # if f(l)>0 or f(r)<0: return None
    # assume zero point in [l,r]
    while r-l > precision:
        m = (l+r)/2
        ret = f(m)
        if ret>0:
            r=m
        elif ret==0:
            return m
        else:
            l=m
    return l
    
def tarnary_search_continuous(l, r, f, precision=1e-9):
    """ f is an continuous function with Δf>0, return the minimum point"""
    while r-l>precision:
        lmid = l + (r-l)/3
        rmid = r - (r-l)/3
        if f(lmid) > f(rmid): # concave use `>`, convex  use `<`
            l = lmid
        else:
            r = rmid
    return l

def tarnary_search():
    """ f is an discrete function with Δf>0, ... 
    todo: https://codeforces.com/contest/1633
    """
    pass
def exponential_search_last(l, f):
    """ `binary_search_last` that don't have a right bound  """
    step = 1
    while f(l+step):
        step *= 2
    
    return binary_search_last(l+step//2, l+step-1, f)

def exponential_search_first(l, f):
    """ `binary_search_first` that don't have a right bound  """
    step = 1
    while not f(l+step):
        step *= 2
    
    return binary_search(l+step//2+1, l+step, f)
    