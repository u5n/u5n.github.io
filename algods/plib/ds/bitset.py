"""
don't use yield or generator
TOC:
    <Bitset(with limit digits)>
    {function class for other bitset}
        bs_max
        bs_min
        bs_iter
    {type_convert}
        lowercase_BS
        BS_lowercase
    depart_single
    subset
    partition_two_subset
    disjoint_two_subset
"""
from string import *
class Bitset:
    """ use a big integer to represent a bool arraylist
    if the `n` is rather small or there is no limit like `n`, don't use this class
    intend: intend to speed up dp transfer calculation especially for knapsack problems
    test: 
        @lc#1981
        @lc#6002
    preformance: 
        time: O(n/w) per bitwise opeartion compare to impl of `[0]*n`, where w is 1000 when n is 100000
        space: around 1b per bit
    """
    __slots__ = 'A','n','mask'
    def __init__(self, n, A=0):
        """ n is number of bits; `self` can store numbers in `range(n)` """ 
        self.mask = (1<<n) - 1
        self.A = A # use `builtins.int` as a bytearray
        self.n = n
    
    def __setitem__(self, i, v:bool):
        self.A |= (1<<i)
        if not v: self.A ^= (1<<i)
    def __getitem__(self, i):
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
    def set(self, i):  self.A |= (1<<i)
    def flip(self, i): self.A ^= (1<<i)
    def unset(self, i): self.A = (self.A|(1<<i))^(1<<i)
    def all(self): return self.A == self.mask
    def any(self): return self.A != 0
    def none(self): return self.A == 0
    def clear(self): self.A = 0
    def count(self): 
        """  
        python version >=3.10
        alternative: 
            https://stackoverflow.com/questions/9829578/fast-way-of-counting-non-zero-bits-in-positive-integer
            or maintain an single variable that dynamiclly count number of 1 after each function
        """
        return self.A.bit_count()
    def __iter__(self):
        A = self.A
        while A:
            lowbit = A&-A
            yield lowbit.bit_length()-1
            A ^= lowbit
    def __reversed__(self):
        A = self.A
        while A:
            higbit = A.bit_length()-1
            yield higbit
            A ^= (1<<higbit)
    def max(self): 
        """ return -1 if self is empty """
        return -1 if self.A == 0 else self.A.bit_length()-1 
    def min(self): 
        """ return -1 if self is empty """
        return (self.A & -self.A).bit_length()-1
    def range_set(self, l, r):
        """ self[l:r] = 1 
        assert: 0<=l<=r<=n
        """
        self.A |= ((1<<(r-l)) - 1)<<l
    def range_count(self, l, r):
        """ return #elements in self[l:r] """
        return ( (self.A>>l) & ((1<<(r-l)) - 1) ).bit_count()
    def issubset(self, oth):
        return self.A&oth.A == self.A
    def __repr__(self):
        binA = format(self.A, f"0{self.n}b")
        return f"Bitset<{self.n}>({binA})"

