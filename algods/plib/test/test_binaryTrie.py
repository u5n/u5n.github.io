import sys; sys.path.append('../../')

from plib.ds.trie.binaryTrie import BinaryTrie, BinaryTrieCounter 
from sortedcontainers import SortedList
from collections import Counter
from random import *
from timeit import default_timer as time

""" correctness 
also check with @luogu#3369
    https://www.luogu.com.cn/record/69090587 
"""
def check_correctness():
    Sl=SortedList()
    C = Counter()
    Bt=BinaryTrieCounter(32)
    LOOP_TIME = 1000
    for _ in range(LOOP_TIME):
        random_uint32 = randrange(2**32)
        for _ in range(randrange(3)):
            C[random_uint32]+=1
            Sl.add(random_uint32)
            Bt.addition(random_uint32, 1)

    assert len(Bt)==sum(C.values())==len(Sl), ".__len__ is wrong"
    for num,cnt in Bt.items():
        assert C[num]==cnt, ".items is wrong"
        assert Bt.getdefault(num)==cnt, ".getdefault is wrong"
    for u,v in zip(Bt, Sl):
        assert u==v, ".__iter__ is wrong"
    # check bisect_left and bisect_right
    for _ in range(LOOP_TIME):
        tar = randrange(2**32)
        assert Bt.nlt(tar) == Sl.bisect_left(tar), "`ntl` is wrong"
        rank = randrange(len(Bt))
        assert Bt.kth(rank) == Sl[rank], "`kth` is wrong"
    
check_correctness()  
def compare_Counter():
    """
    result:
        BinaryTrie add 0.272042249009246
        BinaryTrie iterate 0.0010366539936512709
        BinaryTrie get 0.14559309699689038

        Counter add 0.026804948996868916
        Counter iterate 9.140300971921533e-05
        Counter get 0.007423735994962044
    """
    n = 100000
    nbit = 10
    random_pool1 =[randrange(2**nbit) for _ in range(n)]
    random_pool2 =[randrange(2**nbit) for _ in range(100000)]
    def measure_time_Counter():
        C = Counter()
        start = time()
        for v in random_pool1: C[v]+=1
        print("Counter add", -start+(start:=time()))
        for k,v in C.items():
            pass
        print("Counter iterate", -start+(start:=time()))
        for v in random_pool2:
            C[v]
        print("Counter get", -start+(start:=time()))
    def measure_time_Bt():
        Bt = BinaryTrieCounter(nbit)
        start = time()
        for v in random_pool1: Bt.addition(v, 1)
        print("BinaryTrie add", -start+(start:=time()))
        for v in Bt.items():
            pass
        print("BinaryTrie iterate", -start+(start:=time()))
        for v in random_pool2:
            Bt.getdefault(v)
        print("BinaryTrie get", -start+(start:=time()))
    measure_time_Bt()
    measure_time_Counter()

def compare_SortedList():
    """
    results:
        BinaryTrie add 2.370395482008462
        BinaryTrie iterate 0.7003849579923553
        BinaryTrie remove if in 0.42009964400494937
        BinaryTrie get rank 0.645364828989841
        BinaryTrie get key by rank 0.9800872330088168

        SortedList add 0.14785789100278635
        SortedList iterate 0.0044460989884100854
        SortedList remove if in 0.1083783190115355
        SortedList get rank 0.21055147900187876
        SortedList get item by rank 0.24348979198839515
    """
    n = 100000
    nbit = 30
    random_pool1 =[randrange(2**nbit) for _ in range(n)]
    random_pool2 =[randrange(2**nbit) for _ in range(100000)]
    random_pool3 =[randrange(2**nbit) for _ in range(100000)]
    random_pool4 =[randrange(n) for _ in range(100000)]
    def measure_time_Sl():
        Sl = SortedList()
        start = time()
        for v in random_pool1: Sl.add(v)
        print("SortedList add", -start+(start:=time()))
        for v in Sl:
            pass
        print("SortedList iterate", -start+(start:=time()))
        for v in random_pool2:
            if v in Sl:
                Sl.remove(v)
        print("SortedList remove if in", -start+(start:=time()))
        for v in random_pool3:
            Sl.bisect_left(v)
        print("SortedList get rank", -start+(start:=time()))
        for v in random_pool4:
            if v >= len(Sl): continue
            Sl[v]
        print("SortedList get item by rank", -start+(start:=time()))

        
    def measure_time_Bt():
        Bt = BinaryTrie(nbit)
        start = time()
        for v in random_pool1: Bt.addition(v, 1)
        print("BinaryTrie add", -start+(start:=time()))
        for v in Bt:
            pass
        print("BinaryTrie iterate", -start+(start:=time()))
        for v in random_pool2:
            c = Bt.getdefault(v)
            if c>0:
                Bt.addition(v, -1)
        print("BinaryTrie remove if in", -start+(start:=time()))
        for v in random_pool3:
            Bt.nlt(v)
        print("BinaryTrie get rank", -start+(start:=time()))
        for v in random_pool4:
            if v >= len(Bt): continue
            Bt.kth(v)
        print("BinaryTrie get key by rank", -start+(start:=time()))
    measure_time_Bt()
    measure_time_Sl()

# compare_Counter()
# compare_SortedList()