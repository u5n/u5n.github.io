import itertools
class ArrayBIT:
    """ arraylist support insert,pop,getitem in similar O(lgn) 
    for convenience, it create a two layer structure similar to c++ deque or sqrt decomposition
        `self` contain some segments with max size <= `threshold`
    there is not any key and priority
    it use a binary_indexed_tree(treenode 0based index) to quickly find the inserted segment

    glossary:
        C: [len(seg) for seg in segments]
    invariant:
        unless self is empty, there won't be empty segments
    
    there are still unimplemented functions:
        slice_remove
        insert_array
        binary_search
    because the maxns is very small, the bitree version is abandoned
    test:
        no test
    """
    __slots__ = 'segments', 'tarr', 'n', 'maxns', 'threshold'
    def __init__(self, threshold=8192, A=[], maxns = 30):
        self.maxns = maxns
        self.threshold = threshold
        if A:
            csz = int(0.8*threshold)
            self.n = n = len(A)
            self.segments = [A[i:i+csz] for i in range(0,n,csz)]
            self.tarr = [0]*maxns
            self.__bit_rebuild_suffix(0)
        else:
            self.segments = [[]]
            self.tarr = [0]*maxns
            self.n = 0

    def locate(self, rk):
        """ do binary search on bit, find min i that sum(C[:i])>=rk 
        and `rest + sum(C[:i]) == rk`
        assert: 0<=rk<=self.n
        time: O(lgn)
        """
        if self.n == 0: return 0, 0
        tarr, ns = self.tarr, len(self.segments)
        
        trunk = 1<<(ns.bit_length()-1)
        i = 0 # offset of bit treenode, also where to insert 
        rest = rk
        while trunk:
            cur = i + trunk
            if cur <= ns and rest >= tarr[cur-1]:
                # go right
                rest -= tarr[cur-1]
                i = cur
            trunk >>= 1
        
        return i, rest
        
    def insert(self, rk, v):
        segments, T = self.segments, self.threshold
        if not 0<=rk<=self.n: raise IndexError(".insert out of index")
        i, offset = self.locate(rk)
        # push back, instead of insert front
        if offset==0 and i>0 and len(segments[i-1])<T:
            offset = len(segments[i-1])
            i-=1
        
        # create new segment
        if i == len(segments):
            segments.append([v])
            self.__bit_add(i, 1)
        else:
            curseg = segments[i]
            # segment is full
            if len(curseg) == T:
                # transform to left segment
                if i>0 and len(segments[i-1])<T:
                    curseg[offset:offset] = [v]
                    tarseg = segments[i-1]
                    moved = T-len(tarseg)
                    tarseg.extend(curseg[:moved])
                    del curseg[:moved] 

                    self.__bit_add(i, 1-moved)
                    self.__bit_add(i-1, moved)
                # insert leftmost segment
                elif (i|offset)==0:
                    segments[0:0] = [[v], ]
                    self.__bit_rebuild_suffix(0)
                # avg split current into two segments
                else:
                    csz = T//2
                    segments[i+1:i+1] = [ curseg[csz:] ]
                    del curseg[csz:]
                    if offset <= csz:
                        curseg[offset:offset] = [v]
                    else:
                        segments[i+1][offset-csz:offset-csz] = [v]
                    
                    self.__bit_recalc_suffix_rshift(i)

            # insert into one segment
            else:
                segments[i][offset:offset] = [v]
                self.__bit_add(i, 1)
        
        self.n += 1

    def pop(self, rk):
        if not 0<=rk<self.n: raise IndexError(".pop out of index")
        i, offset = self.locate(rk)
        segments = self.segments
        tar = segments[i]
        ret = tar[offset]
        if len(tar)==1 and self.n!=1:
            del segments[i:i+1] 
            self.__bit_recalc_suffix_lshift(i)
        else:
            del tar[offset:offset+1] 
            self.__bit_add(i, -1)
        self.n -= 1
        return ret

    def __getitem__(self, rk):
        if not 0<=rk<self.n: raise IndexError(".getitem out of index")
        i, offset = self.locate(rk)
        return self.segments[i][offset]
    
    def __setitem__(self, rk, v):
        if not 0<=rk<self.n: raise IndexError(".getitem out of index")
        i, offset = self.locate(rk)
        self.segments[i][offset] = v

    def __bit_recalc_suffix_lshift(self, start):
        """
        A[i:] has been changed
        recalculate the bitree
        """
        segments, ns = self.segments, len(self.segments)
        
        if start == len(segments):
            self.__bit_add(start, -1)
        # the suffix is small
        elif self.maxns > 5*ns - 4*start:
            self.__bit_add(start, -1+len(segments[start]))
            for segi in range(start+1, ns):
                self.__bit_add(segi, len(segments[segi])-len(segments[segi-1]))
        else:
            self.__bit_rebuild_suffix(start)

    def __bit_recalc_suffix_rshift(self, start):
        """
        A[i:] has been changed
        recalculate the bitree
        """
        segments, ns, T = self.segments, len(self.segments), self.threshold
        Ai = len(segments[start])
        # don't need rebuild
        if start == len(segments) -1:
            self.__bit_add(start, Ai-T)
            self.__bit_add(start+1, T-Ai)
        # the suffix is small
        elif self.maxns > 5*ns - 4*start:
            self.__bit_add(start, Ai-T)
            self.__bit_add(start+1, T-Ai)
            for segi in range(start+2, ns-1):
                self.__bit_add(segi, len(segments[segi])-len(segments[segi+1]))
            self.__bit_add(ns-1, len(segments[ns-1]))
        else:
            self.__bit_rebuild_suffix(start)
        
    def __bit_add(self, i, delta):
        maxns, tarr = self.maxns, self.tarr
        while i < maxns:
            tarr[i] += delta
            i |= i+1

    def __bit_rebuild_suffix(self, start):
        maxns, tarr, segments = self.maxns, self.tarr, self.segments
        ns = len(segments)
        pre = [0]*(maxns+1)
        for i in range(ns): pre[i+1] = pre[i] + len(segments[i])
        for i in range(ns, maxns): pre[i+1] = pre[i]
        
        for inode in range(start, maxns):
            tarr[inode] = pre[inode+1] - pre[inode&(inode+1)]
        

    def __iter__(self): return itertools.chain(*self.segments)
    def __len__(self): return self.n
