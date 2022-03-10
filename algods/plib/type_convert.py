from typing import *
import numpy as np
from string import *
"""
numeric
"""
def uint_to_list(x:int, lsb_right=True, radix=10, nbit=None)->List[int]:
    """ change an posint to list of digits """
    ret = []
    while True:
        ret.append(x%radix)
        x//=radix
        if x == 0: break
    if nbit and len(ret)<nbit:
        ret.extend([0]*(nbit-len(ret)))
    if lsb_right:
        return ret[::-1]
    else:
        return ret

def uint_to_str(x:int, lsb_right=True, radix=10, nbit=None)->str: 
    return ''.join(uint_to_list(x, lsb_right, radix, nbit))
def str_to_uint(x:int, radix=10)->str: return int(x, radix)
def list_to_uint(A:list, radix=10,lsb_right=True)->int:
    ret = 0
    iA = iter(A) if lsb_right else iter(reversed(A))
    for v in iA:
        ret = ret*radix + v
    return ret

"""
integer bitset
"""
ordc = {c:1<<(ord(c)-97) for c in ascii_lowercase}
def lowercaseSet_to_BS(s):
    bs = 0
    for c in s: bs += 1<<(ord(c)-97)
    return bs
def BS_to_lowercaseSet(bs):
    s = ''
    for c, bc in ordc.items():
        if bc&bs:
            s += c
    return s
def BS_to_bitarr(bs, lsb_left=False):
    ret = []
    while bs:
        if bs&1:
            ret.append(1)
        else:
            ret.append(0)
        bs//=2
    return ret if lsb_left else ret[::-1]