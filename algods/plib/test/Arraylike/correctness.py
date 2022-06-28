import sys; sys.path.append('../../../')
from plib._util import measure, last_avg_runtime, D
from plib.ds.sqrtArray import Array
from plib.ds.skiplist.skiplist import SkiplistArray
import copy
from random import *

def random_slice(threshold):
    n = 16
    L = list(range(n))
    A = Array(L, randrange(4, 32))


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
            if A != L: 
                raise Exception()
        else:
            if A[l:r] != L[l:r]: 
                raise Exception()

def random_point():
    n = 16
    L = list(range(n))
    A = Array(L, randrange(4, 32))
    S = SkiplistArray(A=L)

    sno = n # sequence number
    for i in range(100000):
        funcname = choice(["insert", "pop", "get"])
        if len(A)==0 or funcname == "insert" :
            i = randrange(len(A)+1)
            
            # oriAseg = copy.deepcopy(A.segments)
            # oriL = L[:]
            A.insert(i, sno)
            L.insert(i, sno)
            S.insert(i, sno)
            sno+=1
            if A!=L:
                # print(i, sno-1)
                # print(oriAseg)
                # print(oriL)
                raise Exception()
            if L!=S:
                raise Exception()

        elif funcname == "pop":
            i = randrange(len(A))
            
            # oriAseg = copy.deepcopy(A.segments)
            # oriL = L[:]

            r1= A.pop(i)
            r2=L.pop(i)
            r3=S.pop(i)
            if r1!=r2:
                raise Exception()
            if r1!=r3:
                raise Exception()

        else:
            i = randrange(len(A))
            if A[i]!=L[i]:
                raise Exception()
            
            if L[i]!=S[i]:
                raise Exception()


for i in range(100): 
    random_slice()
    print(i, end=' ')
print("random_slice pass")

for i in range(100): 
    random_point()
    print(i, end=' ')
print("random_point pass")

