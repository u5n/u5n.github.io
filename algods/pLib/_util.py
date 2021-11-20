from copy import deepcopy
# decorator to print what the function return
# shorthand for "debug"
def D(func):
    def wrapper(*args, **kwargs):
        parg = deepcopy(args)
        ret = func(*args, **kwargs)
        l1 = f'func {func.__name__}(' 
        l1+=', '.join(str(e) for e in parg)
        if(kwargs):
            l1+=', '
            l1+=', '.join( f'{k}={v}' for k,v in kwargs.items())
        l1+=')'
        l2 = f'return `{ret}`'
        print(l1+'\n\t'+l2)
        return ret
    return wrapper

class ListShift:
    """ `list` on closed interval `[l,r]` """
    def __init__(self, l, r, default=0):
        n = r-l+1
        self.container = [default for _ in range(n)]
        self.shift = 0 - l
    def __getitem__(self, i):
        return self.container[i+self.shift]
    def __setitem__(self, i, v):
        self.container[i+self.shift] = v