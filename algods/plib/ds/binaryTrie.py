class BinaryTrie:
    """ 
    practice:
        sorted counter
        xor operation and nbit <= 16 ( trie relate)
        range query ( segmentree related )
    test: @luogu P3369 
    impl: 
        variant of dynamic allocated *segment tree* which is a perfect binary tree
        use an arraylist to store TrieNode
        there is no delete_node method
        TrieNode is represented as a 2-size array@T, its value stored in `self.values`
        sentry:
            `self.nodes[0]` represent a null node, its size is 0
    """
    def __init__(self, nbit):
        self.nodes = [[-1,-1],[0,0]]
        self.values = [0,0]
        self.nbit = nbit
        
    def addition(self, num, val=1):
        nodes, values = self.nodes, self.values
        cur = 1
        values[cur] += val
        for i in reversed(range(self.nbit)):
            b = (num>>i)&1
            if not nodes[cur][b]:
                nodes[cur][b] = len(nodes)
                nodes.append([0,0])
                values.append(0)
            cur = nodes[cur][b]
            values[cur] += val
    def getdefault(self, num, default=0):
        nodes, values = self.nodes, self.values
        cur = 1
        for i in reversed(range(self.nbit)):
            cur = nodes[cur][(num>>i)&1]
            if cur == 0: return default
        return values[cur]

    def items(self, pack=True):
        nodes, values = self.nodes, self.values
        sta = [(1, self.nbit, 0)]
        while sta:
            root,d,num = sta.pop()
            if d==0:
                cnt = values[root]
                if cnt!=0: 
                    if pack:
                        yield num, cnt
                    else:
                        for _ in range(cnt): yield num
            else:
                c0, c1 = nodes[root]
                if values[c1] > 0: sta.append((c1, d-1, num<<1|1))
                if values[c0] > 0: sta.append((c0, d-1, num<<1))
    def __iter__(self): return self.items(pack=False)
    def keys(self):
        """ similar to dict.keys """
        nodes = self.nodes
        sta = [(1, self.nbit, 0)]
        while sta:
            root,d,num = sta.pop()
            if d==0: yield num
            else:
                c0, c1 = nodes[root]
                if c1!=0: sta.append((c1, d-1, num<<1|1))
                if c0!=0: sta.append((c0, d-1, num<<1))
                
    def first_key_ge(self, num):
        """ binary_search first key greater than `num` on `self.keys()`, if no such key, return 1<<self.nbit
        """
        nodes = self.nodes
        cur = 1
        for i in reversed(range(self.nbit)):
            c0, c1 = nodes[cur]
            # compare with left child num
            # <= -> < to use bisect_right
            if curnum*2>=(num>>i) and c0!=0:
                cur = c0
                curnum *= 2
            else:
                cur = c1
                curnum = 2*curnum + 1
            if not cur: return 1<<self.nbit
        return curnum

    def __len__(self): return self.values[1]  

class BinaryTrieCounter(BinaryTrie):
    """
    this class, add some, Counter-only function, works only if the value is count of key
    it can be used as a multiset support get rank by element and get element by rank
    example:
        B = BinaryTrieCounter()
        for k,v in Counter(...).items():
            B.addition(k, v)
    """
    def kth(self, k):
        """ return the kth smallest key, k start from 0, similar to SortedList.__getitem__ """
        nodes, values = self.nodes, self.values
        cur = 1
        ret = 0
        for i in reversed(range(self.nbit)):
            c0, c1 = nodes[cur]
            if k < values[c0]:
                cur = c0
            else:
                k -= values[c0]
                ret |= (1<<i)
                cur = c1
        return ret
    def nlt(self, num):
        """ return number of keys less than `num`, i.e get rank of `num`
        similar to SortedList.bisect_left """
        nodes, values = self.nodes, self.values
        # if num has more that `nbit` bits
        if num >= (1<<self.nbit): return len(self)
        cur = 1
        ret = 0
        for i in reversed(range(self.nbit)):
            c0, c1 = nodes[cur]
            if (num>>i)&1:
                ret += values[c0]
                cur = c1
            else:
                cur = c0
            if not cur: break
        return ret
    def interval_count(self, left, right): 
        """ query [left, right) """
        return self.nlt(right) - self.nlt(left)