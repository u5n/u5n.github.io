class ListShift:
    """ `list` on closed interval `[l,r]`, support negative """
    __slots__ = 'shift', 'container'
    def __init__(self, l, r, default=0):
        n = r-l+1
        self.container = [default for _ in range(n)]
        self.shift = 0 - l
    def __getitem__(self, i):
        return self.container[i+self.shift]
    def __setitem__(self, i, v):
        self.container[i+self.shift] = v

