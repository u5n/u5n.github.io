import bisect
from collections import defaultdict
from functools import partial
import operator
from naryTree import pprint
pprint = partial(pprint, repr=lambda x:f"{x.key}({x.size})" if x else 'Nil')
lessthan = lambda l,r: l-r
# left lean red black tree
# top down implement
# for convenience, can't delete treenode, 
# refer to <Algorithm 4th ed.> https://algs4.cs.princeton.edu/33balanced/RedBlackBST.java
# similar to std::dict
class Node:
    __slots__ = 'key','val','color','left','right','size'
    def __init__(self, key, val, color=0, size=1, left=None, right=None):
        self.color,self.key,self.val,self.size = color, key, val, size
        self.left,self.right = left, right
        # color, 1 means red

def setitem(root, key, val):
    """ usage root = setitem(root, key, val)"""
    def dfs(h):
        if h==None: return Node(key, val, 1)
        if key<h.key: h.left = dfs(h.left)
        elif key>h.key: h.right = dfs(h.right)
        else: h.val = val
        return balance(h)
    root = dfs(root)
    root.color = 0
    return root

def rotateLeft(h):
    x = h.right
    h.right = x.left
    x.left = h
    x.color = h.color
    h.color = 1
    x.size = h.size
    h.size = size(h.left) + size(h.right) + 1
    return x

def rotateRight(h):
    x = h.left
    h.left = x.right
    x.right = h
    x.color = h.color
    h.color = 1
    x.size = h.size
    h.size = size(h.left) + size(h.right) + 1
    return x

def flipColor(h):
    """ h Black, two chilren Red """
    h.color = 1
    h.left.color = 0
    h.right.color = 0

def isRed(h): return h and h.color == 1
def size(h): return h.size if h else 0
def balance(h):
    if isRed(h.right) and not isRed(h.left): h = rotateLeft(h)
    if isRed(h.left) and isRed(h.left.left): h = rotateRight(h)
    if isRed(h.right) and isRed(h.left): flipColor(h)
    h.size = size(h.left) + size(h.right) + 1
    return h

def get(x, key, cmp=lessthan, default=None):
    while x:
        if (r:=cmp(key, x.key))<0: x=x.left
        elif r==0: return x.val
        else: x=x.right
    return default

def iloc(x, rank):
    """ select key by rank (start from 0)"""
    assert 0<=rank<size(x)
    while x:
        if size(x.left) > rank:
            x = x.left
        elif size(x.left) < rank:
            rank -= size(x.left) + 1
            x = x.right
        else:
            return x.key

def bound(x, pred):
    """ lowerbound/upperbound, return rank of first key that pred(key) """
    acc = 0
    while x:
        if pred(x.key):
            x=x.left
        else:
            acc += 1 + size(x.left) 
            x=x.right
    return acc

def index(x, key, cmp=lessthan):
    """ binary search, get rank of key """
    acc = 0
    while x:
        if (r:=cmp(key,x.key))<0:
            x=x.left
        elif r==0:
            acc += size(x.left)
            break    
        else:
            acc += 1 + size(x.left)
            x = x.right
    return acc

#####  debug function
def inorder(x):
    ret = []
    def dfs(x):
        if x:
            dfs(x.left)
            ret.append((x.key,x.val))
            dfs(x.right)
    dfs(x)
    return ret
    
if __name__ == '__main__':
    root = Node(23, 298)
    root = setitem(root, 2, 29)
    root = setitem(root, 3, 29)
    root = setitem(root, 293, 29)
    root = setitem(root, 29, 29)
    root = setitem(root, 33, 29)
    root = setitem(root, 54, 29)
    root = setitem(root, 43, 29)
    root = setitem(root, 27, 29)
    root = setitem(root, 1, 29)
    root = setitem(root, 94, 29)
    pprint(root)
    A = inorder(root)
    print(A)