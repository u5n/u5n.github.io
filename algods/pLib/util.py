def D(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f'func {func.__name__}({args,kwargs}) return `{ret}`')
        return ret
    return wrapper