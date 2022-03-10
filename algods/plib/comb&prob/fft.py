"""
convention: assume all coefficient are integers
"""
from math import *
from typing import *
from fft_np import conv_np

def fft(a: List[complex]):
    n = len(a)
    if n == 1: return [a[0]]
    A1 = fft(a[::2])
    A2 = fft(a[1::2])
    A = [0]*n
    w1 = complex(cos(2*pi/n), sin(2*pi/n)) 
    w = complex(1, 0)
    for k in range(n//2):
        A[k] = A1[k] + w*A2[k]
        A[k+n//2] = A1[k] - w*A2[k]
        w *= w1
    return A


def ifft(A):
    def ifft_dc(A):
        n = len(A)
        if n == 1: return [A[0]]
        a1 = ifft_dc(A[::2])
        a2 = ifft_dc(A[1::2])
        a = [0]*n
        w1 = complex(cos(2*pi/n), -sin(2*pi/n)) 
        w = complex(1, 0)
        for k in range(n//2):
            a[k] = a1[k] + w*a2[k]
            a[k+n//2] = a1[k] - w*a2[k]
            w *= w1
        return a
    # postpone `/n` opeartion to inc the precision
    return [int(round(v.real)/len(A)) for v in ifft_dc(A)]


def conv(a, b):
    n = 1
    while n < len(a)+len(b): n*=2
    a.extend([0]*(n-len(a)))
    b.extend([0]*(n-len(b)))
    A, B = fft(a), fft(b)
    return ifft([Ai*Bi for Ai,Bi in zip(A,B)])


if __name__ == '__main__':
    def test_random1000():
        """ compare with numpy """
        import random
        for _ in range(1):
            n = 1000
            a = [random.randrange(10) for _ in range(n)]
            b = [random.randrange(10) for _ in range(n)]
            res_np = conv(a, b)
            res_pure = conv_np(a, b)
            assert all(isclose(v1, v2, abs_tol=1e-9) for v1,v2 in zip(res_np, res_pure))
        print("test passed")
    test_random1000()