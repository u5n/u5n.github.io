from copy import deepcopy
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