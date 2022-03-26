from sortedcontainers import SortedList
class Interval:
    __slots__ = 'l', 'r', 'val'
    def __init__(self, l, r, val=None):
        self.l, self.r, self.val = l, r, val
    def __repr__(s): return f"Interval({s.l},{s.r},{s.val})"

class SortedDisjointIntervals:
    """ des: a collection of ordered and disjoint closed intervals ( endpoint is integers )
    app: the online algorithm of [meeting rooms](https://leetcode.com/problems/meeting-rooms)
    """
    def __init__(self):
        self.ints = SortedList(key=lambda x: x.l)

    def get_sub(self, l, r):
        """ find all intervals in `self` that fully contained in [l,r] 
        return two indices on `self.ints`, `self.ints[lfind:rfind+1]` are fully contained in [l,r]
        if no such interval, return the original `lfind` and `rfind`, (`rfind-lfind<0`)
        """
        ints = self.ints 
        # find all intervals that left endpoint in [l,r]
        lfind = ints.bisect_key_left(l)
        rfind = ints.bisect_key_right(r) - 1
        if rfind >= lfind:
            if ints[rfind].r > r:
                return lfind, rfind - 1
        return lfind, rfind

    def get_overlap(self, l, r):
        """  similar to `self.get_sub` """
        ints = self.ints 
        # find all intervals that left endpoint in [l,r]
        lfind = ints.bisect_key_left(l)
        rfind = ints.bisect_key_right(r) - 1
        # add a lefter interval
        if lfind > 0:
            if ints[lfind - 1].r >= l:
                lfind -= 1
        return lfind, rfind

    def get_super(self, l, r):
        """ return index of interval on `self` in which the [l,r] fully contained"""
        ints = self.ints 
        lfind = ints.bisect_key_right(l) - 1
        if ints[lfind].r >= r:
            return lfind
        return -1

    def add(self, l, r):
        """ add interval [l,r],
        automatically merge exactly adjacent interval
            eg. interval_union `[1,2],[4,10]`, add `[3,3]` it becomes `[1,10]`
        then return the merged interval
        """
        ints = self.ints 
        lfind, rfind = self.get_overlap(l, r)
        # if a righter interval can merge with [l,r]
        if rfind < len(ints) - 1:
            rr = ints[rfind + 1]
            if rr.l == r + 1:
                r = rr.r
                ints.pop(rfind + 1)

        # if `self` exist overlaping intervals, merge into [l,r]
        if lfind <= rfind:
            l = min(l, ints[lfind].l)
            r = max(r, ints[rfind].r)
            for _ in range(rfind - lfind + 1):
                ints.pop(lfind)
                # rfind is invalid then

        # if a lefter interval can merge with [l,r]
        if lfind > 0:
            ll = ints[lfind - 1]
            if ll.r == l - 1:
                l = ll.l
                ints.pop(lfind - 1)

        new = Interval(l, r)
        ints.add(new)
        return new

    def remove_point(self, x):
        """ remove_point `x` and break interval into less than 2 intervals at point x """
        # the rightmost interval with left endpoint <= x
        ints = self.ints 
        find = ints.bisect_key_right(x) - 1
        if find == -1: return
        tar = ints[find]
        if tar.r >= x:
            ints.pop(find)
            if tar.l != tar.r:
                if tar.l != x:
                    ints.add(Interval(tar.l, x - 1))
                if tar.r != x:
                    ints.add(Interval(x + 1, tar.r))

    def remove(self, l, r):
        """ remove all intervals fully contained in [l,r], split intervals overlap only
        """
        ints = self.ints 
        # find all intervals that left endpoint in [l,r]
        lfind = ints.bisect_key_left(l)
        rfind = ints.bisect_key_right(r) - 1
        # shorten the interval at rfind
        if rfind < len(ints):
            right = ints[rfind]
            if right.r > r:
                right.l = r+1
                rfind -= 1
        # shorten a lefter interval
        if lfind > 0:
            ll = ints[lfind-1]
            if ll.r >= l:
                ll.r = l-1
        # now ints[lfind : rfind+1] is fully contained in [l:r]
        if lfind <= rfind:
            for _ in range(rfind-lfind+1):
                ints.pop(lfind)

    def __len__(self): return len(self.ints)

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
        assert [(x.l, x.r) for x in tree.ints] == [(-100,22), (24,10000)]
    test_SortedIntervals_1()