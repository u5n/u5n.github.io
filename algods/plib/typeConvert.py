from typing import *
import numpy as np
from string import *
def _namespace_string():
    def int_to_list(x:int, base=10, nbit=None, lsb_right=True)->List[int]:
        """ change an int to list of digits """
        ret = []
        while x:
            ret.append(x%base)
            x//=base
        if nbit and len(ret)<nbit:
            ret.extend([0]*(nbit-len(ret)))
        if lsb_right:
            return ret[::-1]
        else:
            return ret
    def int_to_str(x, base=10, nbit=None, lsb_right=True): 
        return ''.join(int_to_list(x, base, nbit, lsb_right))
    def str_to_int(x, base=10): return int(x, base)

def _namespace_bitset():
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