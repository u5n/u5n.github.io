def D(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f'func {func.__name__} return `{ret}`')
        return ret
    return wrapper