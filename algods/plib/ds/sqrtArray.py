from math import ceil
import itertools
import bisect

class Array:
    """
    in the slice related operation, 
        negative parameter is not allowed
        third parameter is not allowed
    invariant:
        segment can't be empty or `n==0`
    convention:
        the inner element type should immutable(or primitive)
            or use `deepcopy` is slow
    """
    __slots__ = 'segments', 'threshold', 'n'
    def __init__(self, A = [], threshold=8192):
        self.threshold = threshold
        self.segments = [[]]
        self.n = 0
        if A:
            self.extend(A)
    
    def insert(self, rk, v):
        segments, T = self.segments, self.threshold
        if not 0<=rk<=self.n: raise IndexError(".insert out of index")
        i, offset = self.locate(rk)
        
        # push back, instead of insert front
        if offset==0 and i>0 and len(segments[i-1])<T:
            offset = len(segments[i-1])
            i -= 1
        
        # create new segment on the right
        if i == len(segments):
            segments.append([v])
        else:
            curseg = segments[i]
            if len(curseg)<T:
                segments[i][offset:offset] = [v]
            else:
                # create new segment to the left
                if (i|offset)==0:
                    segments[0:0] = [[v],]
                # transform to left segment
                elif i>0 and len(segments[i-1])<T:
                    # assert: offset >= 1
                    tarseg = segments[i-1]
                    n_tarseg = len(tarseg)
                    # insert into tarseg
                    if offset + n_tarseg < T:
                        nmove = T - n_tarseg - 1
                        cur_left = curseg[:nmove]
                        del curseg[:nmove]
                        cur_left[offset:offset] = [v]
                        tarseg.extend(cur_left)
                    # insert into curseg
                    else:
                        nmove = T - n_tarseg
                        tarseg.extend(curseg[:nmove])
                        del curseg[:nmove]
                        curseg[offset-nmove:offset-nmove] = [v]
                # avg split current into two segments
                else:
                    csz = T//2
                    segments[i+1:i+1] = [curseg[csz:]]
                    del curseg[csz:] 
                    if offset <= csz:
                        curseg[offset:offset] = [v]
                    else:
                        segments[i+1][offset-csz:offset-csz] = [v]

        self.n += 1
    
    def extend(self, A):
        segments, T = self.segments, self.threshold
        self.n += len(A)
        iA = 0
        # fill last segment
        if segments:
            last = segments[-1]
            if len(last)<T:
                iA = T - len(segments[-1])
                last.extend(A[:iA])

        # avg
        # csz = ceil(n / ceil(n / threshold)) 

        # left lean
        csz = T
        self.segments.extend([A[i:i+csz] for i in range(iA,len(A),csz)])

    def pop(self, rk):
        if not 0<=rk<self.n: raise IndexError(".pop out of index")
        i, offset = self.locate(rk)
        segments = self.segments
        tar = segments[i]
        ret = tar[offset]
        if len(tar)==1 and self.n!=1:
            del segments[i:i+1] 
        else:
            del tar[offset:offset+1]
        self.n -= 1
        return ret

    def locate(self, rk):
        """
        find least i that `sum(len(seg) for seg in segments[:i+1])>rk`
        if not found, i == n
        assert: 0<=rk<=n
        """
        n, segments = self.n, self.segments
        # search forward
        if rk <= n // 2:
            i = 0
            for seg in segments:
                if len(seg) <= rk:
                    rk -= len(seg)
                    i += 1
                else:
                    break
            return i, rk

        # search backward
        # first least i that `n-sum(len(seg) for seg in segments[i+1:])>rk`
        else:
            rk = n - rk
            i = len(segments)
            for seg in reversed(segments):
                lseg = len(seg)
                if lseg <= rk:
                    rk -= lseg
                    i -= 1
                else:
                    if rk == 0: 
                        return i, 0
                    return i-1, lseg-rk
    
    def bisect_left(self, v):
        """ find min i that f[i]>=v, it not found return self.n 
        assert: self is sorted
        """
        i = 0
        for seg in self.segments:
            if seg[-1] >= v:
                return i + bisect.bisect_left(seg, v)
            i += len(seg)
        return i

    def bisect_key_left(self, v, key):
        """ 
        find min i that key(f[i]) >=v, if not found return self.n
        assert: map(key, list(self)) is sorted
        """
        i = 0
        for seg in self.segments:
            if key(seg[-1]) >= v:
                return i + bisect.bisect_left(seg, v, key=key)
            i += len(seg)
        return i

    def __getitem__(self, rk):
        # if not 0<=rk<self.n: raise IndexError(".pop out of index")
        # point get
        if isinstance(rk, int):
            i, offset = self.locate(rk)
            return self.segments[i][offset]
        # slice get
        else:
            segments = self.segments

            rkl, rkr = rk.start, rk.stop
            if rkl >= rkr: return []
            if rkr >= self.n: rkr = self.n
            if rkl < 0: raise Exception("__getitem__ use negative index")
            il, l = self.locate(rkl)
            ir, r = self.locate(rkr)
            
            if il < ir:
                ret = segments[il][l:]
                for segi in range(il+1, ir):
                    ret.extend(segments[segi])
                if ir!=len(segments):
                    ret.extend(segments[ir][:r])
                return ret
            else:
                return segments[il][l:r]
    
    def __setitem__(self, rk, A):
        # if not 0<=rk<self.n: raise IndexError(".pop out of index")
        # point set
        if isinstance(rk, int):
            i, offset = self.locate(rk)
            self.segments[i][offset] = A
        # slice set
        else:
            segments, T = self.segments, self.threshold
            if not A:
                # use clear logic
                del self[rk]
                return 

            rkl, rkr = rk.start, rk.stop
            if rkl > rkr: raise Exception("__setitem__ use invalid range")
            if rkl < 0: raise Exception("__setitem__ use negative index")
            if rkl >= self.n: 
                self.extend(A)
                return
            if rkr >= self.n: rkr = self.n
            
            nA = len(A)
            il, l = self.locate(rkl)
            ir, r = self.locate(rkr)
            self.n += nA

            segl = segments[il]
            nseg = len(segments)
            # delete on one segment
            if il == ir:
                self.n -= r-l
                # don't add any segment
                if nA + l + len(segl) - r <= T:
                    segl[l:r] = A
                else:
                    A = A + segl[r:]
                    iA = T - l
                    segl[l:] = A[:iA]
                    segments[il+1:il+1] = [A[i:i+T] for i in range(iA, len(A), T)]
            # delete on multiple segments
            else:

                self.n -= len(segl) - l + r
                for segi in range(il+1, ir):
                    self.n -= len(segments[segi])

                iA = T - l
                # can put into segl
                if iA >= nA:
                    if ir != nseg:
                        segr = segments[ir]
                        # can merge segl and segr
                        if l + len(segr) + len(A) <= T:
                            segl[l:] = A + segr[r:]
                            del segments[il+1:ir+1]
                        else:
                            segl[l:] = A
                            del segr[:r]
                            del segments[il+1:ir]
                    else:
                        segl[l:] = A
                        del segments[il+1:ir]
                else:
                    segl[l:] = A[:iA]
                    if ir == nseg:
                        segments[il+1:] = [A[i:i+T] for i in range(iA,nA,T)]
                    # try to merge with segr
                    else:
                        segr = segments[ir]
                        last_sz = (nA-iA)%T 
                        # can merge last segment with segments[ir]
                        if last_sz + len(segments[ir]) - r <= T:
                            segr[:r] = A[nA-last_sz:]
                            segments[il+1:ir] = [A[i:i+T] for i in range(iA,nA-last_sz,T)]
                        # ignore last segment
                        else:
                            del segr[:r]
                            segments[il+1:ir] = [A[i:i+T] for i in range(iA,nA,T)]


    def __delitem__(self, rk):
        # point remove
        if isinstance(rk, int):
            self.pop(rk)
        # slice remove
        else:
            segments, T = self.segments, self.threshold

            rkl, rkr = rk.start, rk.stop
            if rkl > rkr: raise Exception("__delitem__ use invalid range")
            if rkr >= self.n: rkr = self.n
            if rkl == rkr: return
            if rkl < 0: raise Exception("__delitem__ use negative index")
            il, l = self.locate(rkl)
            ir, r = self.locate(rkr)
            segl = segments[il]
            nseg = len(segments)
            # delete on one segment
            if il == ir:
                self.n -= r-l
                del segl[l:r]
            # delete on multiple segments
            else:
                self.n -= len(segl) - l + r
                for segi in range(il+1, ir):
                    self.n -= len(segments[segi])
                
                if l > 0:
                    # try to merge segr with segl
                    if ir != nseg:
                        # do merge
                        if len(segments[ir])-r+l<=T:
                            segl[l:] = segments[ir][r:]
                            del segments[il+1:ir+1]
                        # delete without merge
                        else:
                            del segl[l:]
                            del segments[ir][:r]
                            del segments[il+1:ir]
                    else:
                        del segl[l:]
                        del segments[il+1:]
                else:
                    if ir != nseg:
                        del segments[ir][:r]
                    del segments[il:ir]

    def refactor_compact(self):
        T = self.threshold
        tmp = list(self)
        self.segments = [tmp[i:i+T] for i in range(0,self.n,T)]
    
    def refactor(self):
        tmp = list(self)
        self.segments = []
        self.n = 0
        self.extend(tmp)

    def __len__(self):  return self.n
    def __iter__(self): return itertools.chain(*self.segments)
    def __repr__(self): return "Array"+str(tuple(self))
    def __eq__(self, oth):
        if self.n != len(oth): return False
        for v1, v2 in zip(self, oth):
            if v1 != v2: return False
        return True