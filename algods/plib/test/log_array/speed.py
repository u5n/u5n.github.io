"""
数组 和 sl 和 手写平衡树组(BIT) 和 Array

按rk索引(100000): 0.1, 0.6, 0.5
二分搜索: 0.3
写入(随机, 100000): 4, 4, 3
写入(头, 200000): 30, 2, 1
写入(头, 100000): 8, 2, 1.1
写入(头, 10000): 1, 1.3 , 1
写入(头, 1000): 0.4, 1.6, 0.9
删除(随机, 100000): 1.5, 0.8, 0.6
删除(头, 100000): 10, 3.5, 2
删除(头, 10000): 1, 3.5, 2
"""

import sys; sys.path.append('../../../')
from plib._util import measure, last_avg_runtime
from plib.ds.log_array import Array
from sortedcontainers import *
import random
from math import inf, log2

n = 100000
random.seed(23)
threshold = 8192

def test_insert():

    random_range_insert = [random.randrange(i+1) for i in range(n)]
    def gen_random_slrange_insert():
        ret = [0]
        curma = curmi = 0
        for _ in range(n-1):
            v = random.randrange(curmi, curma+1)
            ret.append(v)
            curmi = min(curmi, v)
            curma = min(curma, v)
        return ret
    random_slrange_insert = gen_random_slrange_insert()



    @measure
    def Sl_insert_random():
        S = SortedList()
        for i in random_slrange_insert:
            S.add(i)

    @measure
    def Sl_insert_head():
        S = SortedList()
        for i in reversed(range(n)):
            S.add(i)

    @measure
    def Sl_insert_back():
        S = SortedList()
        for i in range(n):
            S.add(i)

    @measure
    def Ar_insert_random():
        A = Array(threshold=threshold)
        for i in random_range_insert:
            A.insert(i, i)
        print(f"A.ns: {len(A.segments)} \t", end='')


    @measure
    def Ar_insert_head():
        A = Array(threshold=threshold)
        for i in range(n):
            A.insert(0, i)
        print(f"A.ns: {len(A.segments)} \t", end='')


    @measure
    def Ar_insert_back():
        A = Array(threshold=threshold)
        for i in range(n):
            A.insert(i, i)
        print(f"A.ns: {len(A.segments)} \t", end='')

def test_get_pop():
    _t = list(range(n))
    A = Array(_t, threshold)

    S = SortedList(_t)
    random_range_get = [random.randrange(n) for i in range(n)]
    random_range_pop = [random.randrange(i) for i in reversed(range(1, n+1))]

    @measure
    def Sl_get_item():    
        for v in random_range_get:
            S[v]

    @measure
    def Ar_get_item():
        for v in random_range_get:
            A[v]
        print(f"A.ns: {len(A.segments)} \t", end='')


    @measure
    def Sl_pop_random():
        for i in random_range_pop:
            S.pop(i)


    @measure
    def Ar_pop_random():
        for i in random_range_pop:
            A.pop(i)
        print(f"A.ns: {len(A.segments)} \t", end='')


    A = Array(_t, threshold)
    S = SortedList(_t)

    @measure
    def Ar_locate_tail():
        for i in range(n):
            A.locate(n)
        print(f"A.ns: {len(A.segments)} \t", end='')

    @measure
    def Ar_locate_head():
        for i in range(n):
            A.locate(0)

    @measure
    def Sl_pop_head():
        for i in range(n):
            S.pop(0)

    @measure
    def Ar_pop_head():
        for i in range(n):
            A.pop(0)
        print(f"A.ns: {len(A.segments)} \t", end='')



test_insert()
test_get_pop()

