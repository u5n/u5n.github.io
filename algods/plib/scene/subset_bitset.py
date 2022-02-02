"""
don't use yield or generator
"""
def depart_single(BS):
    """ of a bitset, depart each single one bit"""
    ret = []
    while BS:
        ret.append(BS&-BS)
        BS&=(BS-1)
    return ret

def subset(BS):
    """ ret: all subset of bitset BS
    """
    ret = []
    bs1 = BS
    while bs1:
        ret.append(bs1)
        bs1 = (bs1-1)&BS
    ret.append(0)
    return ret
    
def partition_two_subset(U):
    """ ret: all unordered pairs@[bs1, bs2]{ bs1 & bs2 = 0; bs1 | bs2 in U; bs1|bs2 !=0}, where bs1>=bs2
    """
    ret = []
    bs1 = U
    while bs1 and bs1*2>=U:
        # ret.append((bs1, U-bs1))
        ret.append((format(bs1, 'b'), format(U-bs1, 'b')))
        bs1 = (bs1-1)&U
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
        U-=1
    return ret