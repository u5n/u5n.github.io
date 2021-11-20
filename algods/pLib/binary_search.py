# X X X X √ √ √ √
# `f` is a monotonic increasing predicate functions
# find first `i` in interval [`l`,`r`) such that `f(i)`` is True
# if not found, return `r`
def binary_search(l, r, f):
    assert l<=r
    while l<r:
        m = (r+l)//2
        if f(m):
            r=m
        else:
            l=m+1
    return l