from collections import *
import sys
class TrieNode:
    __slots__ = 'chi', 'val'
    def __init__(self, val=None):
        self.chi = {}
        self.val = val
    def __str__(self):
        if self.val is None:
            return f"TrieNode(nchi:{len(self.chi)})"
        return f"TrieNode(val:{repr(self.val)} nchi:{len(self.chi)})"

class Trie:
    """ implement like a `defaultdict`, 
    theoretical data structure, cost too much memory
    key is `str` (allow empty), value can't store `None` 
    """
    def __init__(self):
        self.root = TrieNode()
    
    def __setitem__(self, key, val):
        cur = self._set(key)
        cur.val = val
    def setdefault(self, key, default):
        cur = self._set(key)
        if cur.val is None:  
            cur.val = default
        return cur.val
    def _set(self, key):
        """ create new TrieNode by key and return the node key locate"""
        cur = self.root
        for c in key:
            if c not in cur.chi: cur.chi[c] = TrieNode()
            cur = cur.chi[c]
        return cur
    def _get(self, key):
        """ get TrieNode by key if not found return None """
        cur = self.root
        for c in key:
            if c not in cur.chi: return None
            cur = cur.chi[c]
        return cur
    
    def get(self, key, default=None):
        """ get TrieNode that has val by key, if not found return `default`"""
        node = self._get(key)
        if node is None or node.val is None: return default
        return node.val
    
    def keys(self):
        """ if prefix is empty, it iterate the whole tree """
        path = []
        for node in self._traverse(self.root, path):
            if node.val!=None: yield "".join(path)
    
    def items(self):
        path = []
        for node in self._traverse(self.root,  path):
            if node.val!=None: yield "".join(path), node.val

    def num_nodes(self, valid=False):
        ret = 0
        if valid:
            for node in self._traverse(self.root):
                if node.val!=None: ret += 1
        else:
            for node in self._traverse(self.root): ret += 1
        return ret

    def _traverse(self, root, path=[]):
        """ iterate node of subtree at `root` in preorder """
        def dfs(x):
            yield x
            for k,v in x.chi.items():
                path.append(k)
                yield from dfs(v)
                path.pop()
        yield from dfs(root)
    def pop(self, key, default=None):
        """ """
        cur = self.root
        nodes = deque([(None,cur)]) # from childs to parent
        for c in key:
            if c not in cur.chi: return default
            cur = cur.chi[c]
            nodes.appendleft((c, cur))
        
        ch_tochi, chi = nodes.popleft()
        if chi.val is None : return default
        ret = chi.val; chi.val = None
        if len(chi.chi)!=0: return ret
        while nodes:
            # loop inv: len(chi.chi) == 0 and None==chi.val
            ch_topar, par = nodes.popleft()
            del par.chi[ch_tochi]
            if len(par.chi)>=1 or par.val!=None: return ret
            ch_tochi, chi = ch_topar, par
        # in this case, chi == self.root
        return ret
    def __delitem__(self, key):
        ret = self.pop(key)
        if ret is None: raise KeyError(f"{key}")

    def __getitem__(self, key):
        ret = self.get(key)
        if ret is None: raise KeyError(f"{key}")
        return ret
    def __iter__(self): yield from self.keys()
    def __str__(self):
        """ repr as a dictionary"""
        inner = ", ".join( f'{repr(k)}:{v}' for k,v in self.items )
        return f"Trie{{{inner}}}"
    
    def pprint(self, file=None):
        """ expand like file tree structure"""
        lines = deque()
        d = 0
        mem = 0
        def preorder(x):
            nonlocal d,mem
            mem += sys.getsizeof(x) + sys.getsizeof(x.chi)
            for k,v in x.chi.items():
                yield k,v.val
                d+=1
                yield from preorder(v)
                d-=1
        for key, val in preorder(self.root):
            if val is None:
                line = '    '*d + key
            else:
                line = '    '*d + key + f"({val})"
            lines.append(line)
        
        lines.appendleft(f"Trie{{n_node:{1+len(lines)}, mem: {mem/1000:.1f}KB }}:")
        if file is None:
            for line in lines:
                print(line)
        else:
            with open(file, 'w') as f:
                f.write("\n".join(lines))

class BinaryTrieNode:
    __slots__ = 'c0', 'c1'
    def __init__(self):
        self.c0 = self.c1 = None

class BinaryTrie:
    """ implement like a set"""
    def __init__(self, digit):
        self.root = BinaryTrieNode()
        self.mask = [1<<(digit-1-i) for i in range(digit)]
        # self.U = (1<<digit) - 1
    def set(self, num):
        cur = self.root
        for e in self.mask:
            if num&e:
                if not cur.c0: cur.c0 = BinaryTrieNode()
                cur = cur.c0
            else:
                if not cur.c1: cur.c1 = BinaryTrieNode()
                cur = cur.c1
        # when cur at bottom, use cur.c0 to store additional information
        cur.c0 = 1
    def remove(self, num):
        pass
    def contains(self, num):
        """ whether has odd number of `num` """
        cur = self.root
        for e in self.mask:
            if num&e:
                if not cur.c0: return False 
                cur = cur.c0
            else:
                if not cur.c1: return False
                cur = cur.c1
        return cur.c0 == 1


        
if __name__ == "__main__" :
    T = Trie()
    T['a'] = 1
    T['abc'] = 2
    T['abcd'] = 3
    T['abcde'] = 4
    T['abde'] = 5
    T['accfde'] = 6
    T['babc'] = 7
    T['baba'] = 8
    print(T)
    T.pprint()
    print(T.num_nodes())
    print(T.num_nodes(1))
    del T['abcd']
    print(T)
    for k in list(T):
        print(T.pop(k))
    print(T)
    T[''] = 123
    T.pop('')
    assert T.num_nodes()==1
    assert T.num_nodes(1)==0
    print(T.root)