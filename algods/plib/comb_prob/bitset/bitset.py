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

def bs_subbs(BS):
    """ ret: all subset of bitset BS """
    ret = []
    bs1 = BS
    while bs1:
        ret.append(bs1)
        bs1 = (bs1-1)&BS
    ret.append(0)
    return ret


def bs_2partition(BS):
    """ ret: all unordered pairs@[bs1, bs2]{ bs1 & bs2 = 0; bs1 | bs2 in U}, where bs1>=bs2
    """
    ret = []
    bs1 = BS
    while bs1 and bs1*2>=BS:
        ret.append((bs1, BS-bs1))
        bs1 = (bs1-1)&BS
    return ret

def ubs_2disjoint(U):
    """ args: U: for convenience, all bits in U should be one
    ret: all unordered pairs@[bs1, bs2]{ bs1 & bs2 = 0; bs1 | bs2 in U; bs1|bs2 !=0}, where bs1>=bs2
    time: 
        len(ret) == 3**n / 2
        sum of one in bs1 and bs2 is n*3**(n-1)
    performance: high risk TLE
    """
    ret = []
    while U:
        # assert: U == bs1 | bs2
        bs1 = U
        while bs1 and bs1*2>=U:
            ret.append((bs1, U-bs1))
            bs1 = (bs1-1)&U
        """ # subset of subset
        while bs1: `U` is subset of original `U`, bs1 is subset of `U`
            ret.append((U, bs1))
            bs1 = (bs1-1)&U
        """
        U-=1
    return ret

def cache_bs_subbs(max_bit_count=12):
    ret = [[] for _ in range(1<<max_bit_count)]
    for bs in range(1<<max_bit_count):
        subbs = bs
        while subbs:
            ret[bs].append(subbs)
            subbs=(subbs-1)&bs
        ret[bs].append(0)
    return ret
    
def cache_bs_sum(A):
    """ preprocess subset sum of A 
    {A[0], A[1]} -> 0b11
    """
    n = len(A)
    dp = [0]*(1<<n)
    for bs in range(1, 1<<n):
        lb = bs&-bs
        dp[bs] = dp[bs-lb] + A[lb.bit_length()-1]
    return dp    



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