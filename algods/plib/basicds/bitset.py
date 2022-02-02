class Bitset:
    """ simulate cpp std::bitset, impl with a bigint  
    if the `n` is rather small or there is no limit like `n`, don't use this class
    test: lc#1981
    """
    __slots__ = 'A','n','mask'
    def __init__(self, n, A=0):
        """ n is number of bits; `self` can store numbers in `range(n)` """ 
        self.mask = (1<<n) - 1
        self.A = A # use `builtins.int` as a bytearray
        self.n = n
    
    def __setitem__(self, i, v:bool):
        if v: self.A |= (1<<i)
        else: self.A &= ~(1<<i)
    def __getitem__(self, i):
        if self.A & (1<<i): return True
        else: return False
    def test(self, i):
        if self.A & (1<<i): return True
        else: return False
    def __contains__(self, i):
        if self.A & (1<<i): return True
        else: return False
    def __hash__(self): return hash(self.A)
    
    def __lshift__(self, d):
        if d >= self.n: return Bitset(self.n, 0)
        # you don't care overflow
        return Bitset(self.n, (self.A<<d)&self.mask)
    def __ilshift__(self, d):
        if d >= self.n: self.A = 0
        # you don't care overflow
        else: self.A= (self.A<<d)&self.mask
        return self
    def __rshift__(self, d): return Bitset(self.n, self.A >> d)
    def __irshift__(self, d): self.A>>=d; return self
    def __iand__(self, oth): self.A&=oth.A; return self
    def __ior__(self, oth): self.A|=oth.A; return self
    def __ixor__(self, oth): self.A^=oth.A; return self
    def __and__(self, oth): return Bitset(self.n, self.A & oth.A)
    def __xor__(self, oth): return Bitset(self.n, self.A ^ oth.A)
    def __or__(self, oth): return Bitset(self.n, self.A | oth.A)
    def __len__(self): return self.count()
    def set(self, i):  self.A |= (1<<i)
    def flip(self, i): self.A ^= (1<<i)
    def unset(self, i): self.A &= ~(1<<i)
    def all(self): return self.A == self.mask
    def any(self): return self.A != 0
    def none(self): return self.A == 0
    def clear(self): self.A = 0
    def __iter__(self):
        A = self.A
        while A:
            lowbit = A&-A
            yield lowbit.bit_length()-1
            A -= lowbit
    def __reversed__(self):
        A = self.A
        while A:
            higbit = A.bit_length()-1
            yield higbit
            A -= (1<<higbit)
    def max(self): 
        """ return -1 if self is empty """
        return self.A.bit_length()-1 
    def min(self): 
        """ return -1 if self is empty """
        return (self.A & -self.A).bit_length()-1
    def count(self):
        A = self.A
        r = 0
        while A:
            r += 1
            A &= A-1
        return r
    def __str__(self):
        binA = format(self.A, f"0{self.n}b")
        return f"Bitset<{self.n}>({binA})"