from collections import Counter
# seems that it's useless
# class BinaryTrieNode:
#     # child0, child1
#     __slots__ = 'c0', 'c1'
#     def __init__(self):
#         self.c0 = self.c1 = None

# class BinaryTrie:
#     """ implement like a set """
#     def __init__(self, nbit):
#         self.root = BinaryTrieNode()
#         self.digit_bs = [1<<(nbit-1-i) for i in range(nbit)]
#         # self.fullmask = (1<<nbit) - 1

#     def add(self, num):
#         cur = self.root
#         for d in self.digit_bs:
#             if num&d:
#                 if not cur.c0: cur.c0 = BinaryTrieNode()
#                 cur = cur.c0
#             else:
#                 if not cur.c1: cur.c1 = BinaryTrieNode()
#                 cur = cur.c1
#         # when cur at bottom, use cur.c0 to store additional information
#         cur.c0 = 1
#     def remove(self, num):
#         pass
#     def contains(self, num):
#         """ whether has odd number of `num` """
#         cur = self.root
#         for d in self.digit_bs:
#             if num&d:
#                 if not cur.c0: return False 
#                 cur = cur.c0
#             else:
#                 if not cur.c1: return False
#                 cur = cur.c1
#         return cur.c0 == 1

class BinaryTrie:
    """ 
    des:
        can be used as a SortedList(also a Counter)
            additem
            count
            interval_count
            nlt
            kth
            items
        can be used as a SortedDict(can't delete key)
            additem
            count
            keys
            items
            first_key_ge
    practice:
        sorted counter
        xor operation and nbit <= 16 ( trie relate)
        range query ( segmentree related )
    test: @luogu P3369 
    impl: 
        variant of dynamic allocated segment tree which is a perfect binary tree
        use an arraylist to store TrieNode
        there is no delete_node method
        TriNode is represented as a 3-size array@T
            T[:1] are children
            T[2] is the number of leaves
        sentry:
            `self.nodes[0]` represent a null node, its size is 0
    """
    def __init__(self, nbit):
        self.nodes = [[-1,-1],[0,0]]
        self.nbit = nbit
    def additem(self, num, cnt=1):
        """ add(decrease) `cnt` number of `num` into `self` """
        nodes = self.nodes
        cur = 1
        nodes[cur][2] += cnt
        for i in reversed(range(self.nbit)):
            b = (num>>i)&1
            if not nodes[cur][b]: 
                nodes[cur][b] = len(nodes)
                nodes.append([0,0,0])
            cur = nodes[cur][b]
            nodes[cur][2] += cnt
    def count(self, num, default=0):
        nodes = self.nodes
        cur = 1
        for i in reversed(range(self.nbit)):
            cur = nodes[cur][(num>>i)&1]
            if cur == 0: return default
        return nodes[cur][2]

    def items(self, pack=True):
        nodes = self.nodes
        # dfs code:
        #     def dfs(root, d, num):
        #         c0, c1, cnt = nodes[root]
        #         if d==0:
        #             if cnt !=0:
        #                 yield num, cnt
        #             return
        #         if nodes[c0][2] > 0:
        #             yield from dfs(c0, d-1, num<<1)
        #         if nodes[c1][2] > 0:
        #             yield from dfs(c1, d-1, num<<1|1)
        #     yield from dfs(1, self.nbit, 0)
        sta = [(1, self.nbit, 0)]
        while sta:
            root,d,num = sta.pop()
            if d==0:
                cnt = nodes[root][2]
                if cnt!=0: 
                    if pack:
                        yield num, cnt
                    else:
                        for _ in range(cnt): yield num
            else:
                c0, c1 = nodes[root][:2]
                if nodes[c1][2] > 0: sta.append((c1, d-1, num<<1|1))
                if nodes[c0][2] > 0: sta.append((c0, d-1, num<<1))
    def __iter__(self): return self.items(pack=False)
    def keys(self):
        """ similar to dict.keys """
        nodes = self.nodes
        sta = [(1, self.nbit, 0)]
        while sta:
            root,d,num = sta.pop()
            if d==0: yield num
            else:
                c0, c1 = nodes[root][:2]
                if nodes[c1][2] > 0: sta.append((c1, d-1, num<<1|1))
                if nodes[c0][2] > 0: sta.append((c0, d-1, num<<1))
                
    def first_key_ge(self, num):
        """ binary_search on `self.keys()`, if no such key, return 1<<self.nbit
        """
        nodes = self.nodes
        cur = 1
        for i in reversed(range(self.nbit)):
            c0, c1 = nodes[cur][:2]
            # compare with left child num
            # <= -> < to use bisect_right
            if curnum*2>=(num>>i) and nodes[c0][2]>0:
                cur = c0
                curnum *= 2
            else:
                cur = c1
                curnum = 2*curnum + 1
            if not cur: return 1<<self.nbit
        return curnum

    def __len__(self): return self.nodes[1][2]  


    def kth(self, k):
        """ Counter-only function: works only if the value if count of key
        return the kth smallest element, k start from 0, similar to SortedList.__getitem__ """
        nodes = self.nodes
        cur = 1
        ret = 0
        for i in reversed(range(self.nbit)):
            c0, c1 = nodes[cur][:2]
            if k < nodes[c0][2]:
                cur = c0
            else:
                k -= nodes[c0][2]
                ret |= (1<<i)
                cur = c1
        return ret
    def nlt(self, num):
        """ Counter-only function: works only if the value if count of key
        number of number less than `num`, i.e get rank of `num`
        similar to SortedList.bisect_left """
        nodes = self.nodes
        # if num has more that `nbit` bits
        if num >= (1<<self.nbit): return len(self)
        cur = 1
        ret = 0
        for i in reversed(range(self.nbit)):
            c0, c1 = nodes[cur][:2]
            if (num>>i)&1:
                ret += nodes[c0][2]
                cur = c1
            else:
                cur = c0
            if not cur: break
        return ret
    def interval_count(self, left, right): 
        """ Counter-only function: works only if the value if count of key
        query [left, right) """
        return self.nlt(right) - self.nlt(left)
    
    
class BinaryTrieCounter(BinaryTrie):
    pass