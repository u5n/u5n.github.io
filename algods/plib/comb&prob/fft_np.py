"""
tar:
    focus on multiplication of two polynomials
convention: assume all coefficient are integers
glossary:
    conv: multiple of two polynomial is convolution use add opeartor
others:
    np.fft.fft(a)
        equal to -np.real(normal_fft(a)) + np.imag(normal_fft(a))
        where use `ω(n,1) = complex(cos(2*pi/n), -sin(2*pi/n)) `
"""
from math import *
from typing import *
import numpy as np

def conv_np(a,b):
    n = len(a)+len(b)
    return np.round(np.real(np.fft.ifft(np.fft.fft(a, n)*np.fft.fft(b,n)))).astype(np.uint64)

def conv_mod_np(a, b, Mod):
    """ refer: https://github.com/kth-competitive-programming/kactl/blob/master/content/numerical/FastFourierTransformMod.h
    precision: n*log2(n)*Mod < 8.6e16 (in practice) 
    des: there is no need for conv_mod_notnumpy because the some trick is language specifically
    test: 1155
    """
    a_small = []
    a_large = []
    b_small = []
    b_large = []
    Cut = isqrt(Mod)
    for v in a:
        a_small.append(v%Cut)
        a_large.append(v//Cut)
    for v in b:
        b_small.append(v%Cut)
        b_large.append(v//Cut)
    
    r00 = conv_np(a_small, b_small)
    r1 = conv_np(a_small, b_large) + conv_np(a_large, b_small)
    r11 = conv_np(a_large, b_large)

    return ((r11%Mod*Cut + r1)%Mod*Cut + r00)%Mod
