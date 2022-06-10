import sys; sys.path.append('../../../')
from plib._util import measure, last_avg_runtime, D
from plib.ds.sqrtArray import Array
import copy
from random import *

# n = 16
# L = list(range(n))
# A = Array(L, 8)
# L = [45, 61, 57, 58, 30, 54, 39, 59, 37, 48, 63, 9, 64, 31, 56, 60, 40, 52, 41, 28, 17, 32, 55]
# A.segments = [[45, 61], [57], [58, 30], [54, 39], [59, 37], [48, 63], [9, 64], [31], [56, 60], [40, 52], [41, 28], [17, 32, 55]]
# A.n = len(L)
# D(A.locate(5))
# A.insert(5,65)
# L.insert(5,65)
# assert A==L

def random_slice(threshold):
    n = 16
    L = list(range(n))
    A = Array(L, threshold)

    sno = n # sequence number
    for i in range(100000):
        funcname = choice(["set", "get", "del"])
        l = randrange(len(A)+1)
        r = randrange(l, len(A)+1)
        
        if funcname == "set":
            nadd = randrange(n)
            toadd = [sno+z for z in range(nadd)]
            sno += nadd
            
            # oriAseg = copy.deepcopy(A.segments)
            # oriL = L[:]

            A[l:r] = toadd
            L[l:r] = toadd
            
            if A!=L:
                # print(i, toadd, slice(l,r))
                # print(oriAseg)
                # print(oriL)
                raise Exception("set function wrong")
            
        elif funcname == "del":
            del A[l:r]
            del L[l:r]
            assert A == L
        else:
            assert A[l:r] == L[l:r]

def random_point(threshold):
    n = 16
    L = list(range(n))
    A = Array(L, threshold)

    sno = n # sequence number
    for i in range(100000):
        funcname = choice(["insert", "pop", "get"])
        if len(A)==0 or funcname == "insert" :
            i = randrange(len(A)+1)
            
            # oriAseg = copy.deepcopy(A.segments)
            # oriL = L[:]

            A.insert(i, sno)
            L.insert(i, sno)

            sno+=1
            if A!=L:
                print(i, sno-1)
                print(oriAseg)
                print(oriL)
                raise Exception("insert function wrong")
        elif funcname == "pop":
            i = randrange(len(A))
            
            # oriAseg = copy.deepcopy(A.segments)
            # oriL = L[:]

            assert A.pop(i)==L.pop(i)
            assert A==L, (i, oriAseg, oriL)
        else:
            i = randrange(len(A))
            assert A[i]==L[i], (i, A.segments, L)


for i in range(100): 
    random_slice(randrange(4, 32))
    print(i, end=' ')

for i in range(100): 
    random_point(randrange(4, 32))
    print(i, end=' ')