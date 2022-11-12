"""
diff with sorted_partition_intervals.py 
    interval don't contain value, store interval information only
    intervals are disjoint and not all interval has adjacent interval
test:
    @lc#2276
        https://leetcode.cn/submissions/detail/314560085/
    @lc#715
        https://leetcode.cn/submissions/detail/315052501/
    @lc#352
        https://leetcode.cn/submissions/detail/315065563/

All of methods can be done with ChthollyTree(value is bool, 1 means the interval added, 0 means removed), but faster
"""

from sortedcontainers import SortedList
import itertools

class BoolList_Groupby:
    """ des: List[bool] with some operations, faster than SortedDisjointIntervals
    can find size of continuous ones
    """
    __slots__ = 'zeros', 'szs'
    def __init__(self, n, A = None):
        if A:
            # self.ones = SortedList([i for i,v in enumerate(A) if v])
            self.zeros = SortedList([i for i,v in enumerate(A) if v==0])
            self.szs = SortedList(len(list(y)) for x,y in itertools.groupby(A) if x)
        else:
            # self.ones = SortedList()
            self.zeros = SortedList(range(n))
            self.szs = SortedList()
        # add two sentry
        self.zeros.add(-1)
        self.zeros.add(n)

    def __setitem__(self, i, v):
        zeros, szs = self.zeros, self.szs
        if v:
            if i in zeros:
                l1sz = i - zeros[zeros.bisect_left(i)-1] - 1
                r1sz = zeros[zeros.bisect_right(i)] - i - 1 
                if l1sz:
                    szs.remove(l1sz)
                if r1sz:
                    szs.remove(r1sz)
                szs.add(l1sz+r1sz+1)
                zeros.remove(i)
        else:
            if i not in zeros:
                l1sz = i - zeros[zeros.bisect_left(i)-1] - 1
                r1sz = zeros[zeros.bisect_right(i)] - i - 1 
                szs.remove(l1sz+r1sz+1)
                if l1sz:
                    szs.add(l1sz)
                if r1sz:
                    szs.add(r1sz)
                zeros.add(i)

    def __repr__(self):
        s = ''
        for i in range(self.zeros[-1]):
            s += '0' if i in self.zeros else '1'
        return s


class SortedDisjointIntervals:
    """ des: a collection of ordered and disjoint closed intervals ( endpoint is integers )
    app: the online algorithm of [meeting rooms](https://leetcode.com/problems/meeting-rooms)
    """
    __slots__ = 'itvs',
    def __init__(self):
        # map left endpoint to right endpoint
        # assumption: sortedlist is faster than sorteddict
        # the code logic insure there won't be duplicates of left_endpoint, there is no need to use SortedDict to avoid duplications
        self.itvs = SortedList(key=lambda x:x[0])

    def get_sub(self, l, r):
        """ find all intervals in `self` that completely contained in [l,r] 
        return two indices@[lfind, rfind] on `self.itvs`, `self.itvs[lfind:rfind]` are completely contained in [l,r]
        if no such interval, satisfing `rfind-lfind<=0`
        assert: l<=r
        """
        itvs = self.itvs 
        # find all intervals that left endpoint in [l,r]
        lfind = itvs.bisect_key_left(l)
        rfind = itvs.bisect_key_right(r)
        # in case partially overlap
        if lfind < rfind and itvs[rfind-1][1] > r:
            rfind -= 1
        return lfind, rfind

    def get_overlap(self, l, r):
        """ [l:r] are indices of intervals on `self` with which the [l,r] overlaps 
        assert: l<=r
        """
        itvs = self.itvs 
        # find all intervals that left endpoint in [l,r]
        lfind = itvs.bisect_key_left(l)
        rfind = itvs.bisect_key_right(r)
        # in case partially overlap
        if lfind > 0 and itvs[lfind - 1][1] >= l:
            lfind -= 1
        return lfind, rfind

    def get_super(self, l, r):
        """ `lfind` are indices of intervals on `self` in which the [l,r] completely contained
        assert: l<=r
        """
        itvs = self.itvs 
        lfind = itvs.bisect_key_right(l) - 1
        if lfind>=0 and itvs[lfind][1] >= r:
            return lfind
        return None


    def add(self, l, r):
        """ add interval [l,r],
        automatically merge exactly adjacent interval
            eg. interval_union `[1,2],[4,10]`, add `[3,3]` it becomes `[1,10]`
        assert: l<=r
        """
        itvs = self.itvs 
        lfind = itvs.bisect_key_left(l)
        # use `r+1` to contain an interval whose leftendpoint is r+1
        rfind = itvs.bisect_key_right(r+1) 
        # if a lefter interval can merge with [l,r]
        if lfind > 0 and itvs[lfind - 1][1] >= l - 1:
            lfind -= 1

        # remove all overlaping(or exactly adjacent) intervals
        if lfind < rfind:
            l = min(l, itvs[lfind][0])
            r = max(r, itvs[rfind-1][1])
            del itvs[lfind: rfind]

        itvs.add([l, r])
        return l,r

    def remove_point(self, x):
        """ remove_point `x` and break interval into less than 2 intervals at point x """
        itvs = self.itvs 
        # the rightmost interval with left endpoint <= x
        find = itvs.bisect_key_right(x) - 1
        if find == -1: return
        l, r = itvs[find]
        if r >= x:
            itvs.pop(find)
            if l != r:
                if l != x:
                    itvs.add([l, x - 1])
                if r != x:
                    itvs.add([x + 1, r])

    def split_at(self, x):
        """
        split the interval contain point x into two intervals, leftendpoint of one of them is x
        """
        itvs = self.itvs
        find = itvs.bisect_key_right(x) - 1
        if find == -1: return 
        l, r = itvs[find]
        if r >= x:
            if l == x: return 
            itvs[find][1] = x-1
            itvs.add([x, r])

    def remove(self, l, r):
        """ remove all intervals completely contained in [l,r], split intervals that partially overlap
        assert: l<=r
        """
        itvs = self.itvs 
        # split at two endpoint
        self.split_at(l)
        self.split_at(r+1)
        # now there won't any interval partially overlap with or contain [l,r]
        lfind = itvs.bisect_key_left(l)
        rfind = itvs.bisect_key_right(r)
        if lfind < rfind:
            del itvs[lfind:rfind]

    def __len__(self): return len(self.itvs)


if __name__ == '__main__':
    def test_SortedIntervals_1():
        tree = SortedDisjointIntervals()
        tree.add(1, 1)
        tree.remove_point(0)
        tree.remove_point(1)
        tree.add(-100, 100)
        tree.remove_point(23)
        tree.remove_point(24)
        tree.remove_point(25)
        tree.remove_point(100)
        tree.remove_point(1022)
        tree.add(239, 10000)
        tree.add(24, 30)
        tree.add(24, 3000)
        assert [(x[0], x[1]) for x in tree.itvs] == [(-100,22), (24,10000)]
    test_SortedIntervals_1()