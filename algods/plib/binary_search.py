""" 
des:
    input:
        `f` is a monotonic increasing predicate functions defined on integers
            example: "X X X X √ √ √ √"
        the domain of `f` is [`l`,`r`), value `r` is a sentry
    output:
        first `i` in interval [`l`,`r`) such that `f(i)` is True
        if not found, return `r`
    side effect: None
convention: normally `r` = max_value + 1
time: maybe TLE if `bisect` is available
"""
def binary_search(l, r, f):
    assert l<=r
    while l<r:
        m = (r+l)//2
        if f(m):
            r=m
        else:
            l=m+1
    return l

# backup
def binary_search_last(l, r, f):
    """ example: √ √ √ √ X X X X 
    des: find last `x` in (`l`,`r`] that `f(x)`; if not found return `l`
    """
    assert l<=r
    while l<r:
        m = (r+l+1)//2
        if f(m):
            l=m
        else:
            r=m-1
    return l

def binary_search_exact(l, r, f):
    """ f is an increasing function in discrete interval [l,r], 
    return the zero point of f if not found, return None """
    if f(l) > 0 or f(r) < 0: return None
    while r-l>=0:
        m = (l+r)//2
        ret= f(m)
        if ret ==0: return m
        elif ret>0: r = m-1
        else: l = m+1
    return None

def binary_search_exact_float(l, r, f, precision):
    """ f is an increasing function in [l,r], return the approximate zero point of f 
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

def exponential_search_last(l, f):
    """ `binary_search_last` that don't have a right bound  """
    step = 1
    while f(l+step):
        step *= 2
    
    return binary_search_last(l+step//2, l+step-1, f)

def exponential_search(l, f):
    """ `binary_search` that don't have a right bound  """
    step = 1
    while not f(l+step):
        step *= 2
    
    return binary_search(l+step//2+1, l+step, f)
    