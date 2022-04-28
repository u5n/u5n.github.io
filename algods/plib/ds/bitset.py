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


def bs_max(bs): 
    """ return -1 if self is empty """
    return -1 if bs == 0 else bs.bit_length()-1 
def bs_min(bs): 
    """ return -1 if self is empty """
    return (bs & -bs).bit_length()-1

def bs_iter(bs):
    """ return arraylist of indices of 1s of bitset `bs` """
    ret = []
    while bs:
        lb = bs&-bs
        ret.append(lb.bit_length()-1)
        bs ^= lb
    return ret


def subsetsum(A):
    """ preprocess subset sum of A 
    {A[0]} -> 0b1
    """
    n = len(A)
    dp = [0]*(1<<n)
    for BS in range(1<<n):
        lb = BS&-BS
        dp[BS] = dp[BS-lb] + A[lb.bit_length()-1]
    return dp
    
def subset(BS):
    """ ret: all subset of bitset BS, reverse order by `bit_count`
    """
    ret = []
    bs1 = BS
    while bs1:
        ret.append(bs1)
        bs1 = (bs1-1)&BS
    ret.append(0)
    return ret
    
def partition_two_subset(BS):
    """ ret: all unordered pairs@[bs1, bs2]{ bs1 & bs2 = 0; bs1 | bs2 in U}, where bs1>=bs2
    """
    ret = []
    bs1 = BS
    while bs1 and bs1*2>=BS:
        ret.append((bs1, BS-bs1))
        bs1 = (bs1-1)&BS
    return ret

def disjoint_two_subset(U):
    """ args: U: for convenience, all bits in U should be one
    ret: all unordered pairs@[bs1, bs2]{ bs1 & bs2 = 0; bs1 | bs2 in U; bs1|bs2 !=0}, where bs1>=bs2
    time: 
        len(ret) == 3**n / 2
        sum of one in bs1 and bs2 is n*3**(n-1)
    performance: high risk TLE
    """
    ret = []
    while U:
        # U = bitset1 | bitset2
        bs1 = U
        while bs1 and bs1*2>=U:
            ret.append((bs1, U-bs1))
            bs1 = (bs1-1)&U
        """ # subset of subset
        while bs1:
            ret.append((U, bs1))
            bs1 = (bs1-1)&U
        """
        U-=1
    return ret

def combinations(n, r):
    """ des: example: combinations(5,3) yield '0011', '0101', '0110', '1001', '1010', '1100'
    assert: n>=1
    performance: far slower than itertools.combinations
    """
    if r>n: return 
    x = (1<<r)-1
    last = x<<(n-r)
    while True:
        yield x
        if x==last: return
        u = x&-x
        v = x+u
        if v==0: return
        x = v + (((x^v)//u)>>2)