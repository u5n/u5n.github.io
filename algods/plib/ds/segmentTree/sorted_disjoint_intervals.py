"""
diff with sorted_partition_intervals.py 
    interval don't contain value, store interval information only
"""

from sortedcontainers import SortedList

class SortedDisjointIntervals:
    """ des: a collection of ordered and disjoint closed intervals ( endpoint is integers )
    app: the online algorithm of [meeting rooms](https://leetcode.com/problems/meeting-rooms)
    """
    def __init__(self):
        # map left endpoint to right endpoint
        # assumption: sortedlist is faster than sorteddict
        # the code logic insure there won't be duplicates of left_endpoint, there is no need to use SortedDict to avoid duplicate
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
        if itvs[lfind][1] >= r:
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
        split the interval contain point x into two interval, one of them leftendpoint is x
        """
        itvs = self.itvs
        find = itvs.bisect_key_right(x) - 1
        if find == -1: return 
        l, r = itvs[find]
        if r >= x:
            if l == x: return 
            itvs[find] = x-1
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