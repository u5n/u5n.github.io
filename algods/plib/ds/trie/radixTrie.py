from collections import deque
import itertools
import string
import sys
class RadixTrieNode:
    __slots__ = 'val', 'chi'
    def __init__(self, val=None):
        self.chi = {}
        self.val = val
    def __str__(self):
        if self.val is not None:
            return f"RTN{{val:{self.val} nchi:{len(self.chi)}}}"
        return f"RTN{{nchi:{len(self.chi)} }}"

class RadixTrie:
    """ example: coding, compact multiple lines into one line 
    implement as a `defaultdict`
    for a node, its edges share no common prefix
    currently there is no need for a delete operation
    """
    def __init__(self):
        self.root = RadixTrieNode()
    def __setitem__(self, word, val):
        self._set(word).val = val
    def setdefault(self, word, default):
        node = self._set(word)
        if node.val is None: node.val = default
        return node.val
    def _set(self, word:str):
        """ set TrieNode by word return node that word locates """
        cur = self.root
        i_w, n_w = 0, len(word)
        while i_w < n_w:
            key = word[i_w]; i_w+=1
            if key not in cur.chi:
                # create a new leaf
                new = RadixTrieNode()
                cur.chi[key] = ( word[i_w:],  new)
                return new
            edge, nxt = cur.chi[key]
            i_edge = 0; n_edge = len(edge)
            while i_w < n_w and i_edge<n_edge and word[i_w] == edge[i_edge]:
                i_edge += 1; i_w += 1
            
            if i_edge != n_edge:
                # must split edge, create a new intermediate node
                # cur -> new -> nxt
                new = RadixTrieNode()
                cur.chi[key] = ( edge[:i_edge], new)
                new.chi[edge[i_edge]] = ( edge[i_edge+1:], nxt)
                cur = new
            else:
                cur = nxt
        return cur

    def _get(self, word):
        """ get TrieNode by key if not found return None """
        cur = self.root
        i_w = 0; n_w = len(word)
        while i_w < n_w:
            key = word[i_w]; i_w += 1
            if key not in cur.chi: return None
            edge, nxt = cur.chi[key]
            i_edge = 0; n_edge = len(edge)
            while i_w < n_w and i_edge<n_edge and word[i_w] == edge[i_edge]:
                i_edge += 1; i_w += 1
            
            if i_edge != n_edge: return None
            cur = nxt
        return cur
    
    def pprint(self, file=None):
        """ expand like file folder """
        lines = deque()
        d = 1
        mem = 0
        def preorder(x):
            nonlocal d,mem
            mem += sys.getsizeof(x) + sys.getsizeof(x.chi)
            for k,v in x.chi.items():
                mem += sys.getsizeof(v[0])
                yield k+v[0], v[1].val
                d+=1
                yield from preorder(v[1])
                d-=1
        for complete_key, val in preorder(self.root):
            if val is None:
                line = '    '*d + repr(complete_key)
            else:
                line = '    '*d + repr(complete_key) + f"({val})"
            lines.append(line)
        
        lines.appendleft(f"RadixTrie{{n_node:{1+len(lines)}, mem: {mem/1000:.1f}KB }}:")
        if file is None:
            for line in lines:
                print(line)
        else:
            with open(file, 'w') as f:
                f.write("\n".join(lines))

if __name__ == "__main__":
    def test1():
        T = RadixTrie()
        with open("radixTrie.py", 'r') as f:
            for i,line in enumerate(f.readlines()):
                T[line.strip()] = i
        T.pprint()
    test1()
    T = RadixTrie()
    T['apple'] = 1
    print(T._get('apple'))
    T['app'] = 1
    T.pprint()