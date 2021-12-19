""" use when `n` is very large e.g. 1e9 """
class Bitset:
    __slots__ = 'A','n','mask'
    def __init__(self, n, A=0):
        """ n is number of bit """ 
        self.mask = (1<<n) - 1
        self.A = A # use `builtins.int` as a bytearray
        self.n = n
    def __contains__(self, i):
        if self.A & (1<<i): return True
        else: return False
    
    def __hash__(self):
        """ consider it as a hash of `builtins.set` instead of bytearray """
        return hash(self.A)
    def __getitem__(self, i):
        if self.A & (1<<i): return True
        else: return False
    def __setitem__(self, i, v:bool):
        if v: self.A |= (1<<i)
        else: self.A ^= (self.A & (1<<i))
    def test(self, i):
        if self.A & (1<<i): return True
        else: return False
    def set(self, i): 
        self.A |= (1<<i)
    def flip(self, i): 
        self.A ^= (1<<i)
    def unset(self, i):
        """ set pos `i` to false"""
        self.A ^= (self.A & (1<<i))
    def __lshift__(self, d):
        if d >= self.n: return Bitset(self.n, 0)
        # you don't care overflow
        return Bitset(self.n, (self.A<<d)&self.mask)
    def __ilshift__(self, d):
        if d >= self.n: self.d = 0
        # you don't care overflow
        self.A= (self.A<<d)&self.mask
    def __rshift__(self, d):
        return Bitset(self.n, self.A >> d)
    def __irshift__(self, d):
        self.A>>=d
    def __iand__(self, oth):
        self.A&=oth.A
    def __ior__(self, oth):
        self.A|=oth.A
    def __ixor__(self, oth):
        self.A^=oth.A
    def __and__(self, oth):
        return Bitset(self.n, self.A & oth.A)
    def __xor__(self, oth):
        return Bitset(self.n, self.A ^ oth.A)
    def __or__(self, oth):
        return Bitset(self.n, self.A | oth.A)
    def __len__(self): return self.n
    def all(self): return self.A == self.mask
    def any(self): return self.A != 0
    def none(self): return self.A == 0
    def clear(self):
        self.A = 0
    def __iter__(self):
        A = self.A
        while A:
            lowbit = A&-A
            yield lowbit.bit_length() - 1
            A -= lowbit
    def __reversed__(self):
        A = self.A
        while A:
            higbit = A.bit_length()-1
            yield higbit
            A -= (1<<higbit)
    def msb(self):
        return self.A.bit_length()-1
    def count(self):
        A = self.A
        r = 0
        while A:
            r += 1
            A &= A-1
        return r
    def __str__(self):
        binA = format(self.A, f"0{self.n}b")
        return f"Bitset<{self.n}>{{{binA}}})"