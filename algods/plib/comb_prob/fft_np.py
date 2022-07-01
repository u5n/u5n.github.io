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

from numpy.fft import fft, ifft
def int_conv128(a,b):
    n = len(a)+len(b)-1
    return np.round(np.real(ifft(fft(a, n)*fft(b,n)))).astype(np.uint64)

from scipy.fft import fft, ifft
# don't use np.fft, when need complex256
def int_conv256(a,b):
    n = len(a)+len(b)-1
    a, b = np.array(a, dtype=np.complex256), np.array(b, dtype=np.complex256)
    return np.round(np.real(ifft(fft(a, n)*fft(b,n)))).astype(np.uint64)

int_conv = int_conv256

def conv_mod(a, b, Mod):
    """ refer: https://github.com/kth-competitive-programming/kactl/blob/master/content/numerical/FastFourierTransformMod.h
    precision: n*log2(n)*Mod < 8.6e16 (in practice) 
    test: @lc#1155(all possible input)
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
    
    r00 = int_conv(a_small, b_small)
    r1 = int_conv(a_small, b_large) + int_conv(a_large, b_small)
    r11 = int_conv(a_large, b_large)

    return ((r11%Mod*Cut + r1)%Mod*Cut + r00)%Mod

def conv_power_mod(b, e, Mod):
    ret = np.array([1])
    while e:
        if e&1:
            ret = conv_mod(b, ret, Mod)
        b = conv_mod(b, b, Mod)
        e>>=1
    return ret