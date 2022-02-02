from dataclasses import dataclass
from sortedcontainers import SortedDict, SortedList

class Interval:
    __slots__ = 'l', 'r', 'val'
    def __init__(self, l, r, val=None):
        self.l, self.r, self.val = l, r, val


class SortedIntervals:
    """ a collection of ordered and disjoint closed intervals ( endpoint is integers )
    """
    def __init__(self):
        self.ints = SortedList(key=lambda x: x.l)

    def get_sub(self, l, r):
        """ find all intervals in `self` that fully contained in [l,r] 
        return two indices on `self.ints`, `self.ints[lfind:rfind+1]` are fully contained in [l,r]
        if no such interval, `rfind-lfind<=0`
        """
        # find all intervals that left endpoint in [l,r]
        lfind = self.ints.bisect_key_left(l)
        rfind = self.ints.bisect_key_right(r) - 1
        if rfind >= lfind:
            if self.ints[rfind].r > r:
                return lfind, rfind - 1
        return lfind, rfind

    def get_overlap(self, l, r):
        """  similar to `self.get_sub` """
        lfind = self.ints.bisect_key_left(l)
        rfind = self.ints.bisect_key_right(r) - 1
        if lfind > 0:
            if self.ints[lfind - 1].r >= l:
                lfind -= 1
        return lfind, rfind

    def get_super(self, l, r):
        """ return index of interval on `self` in which the [l,r] fully contained"""
        lfind = self.ints.bisect_key_right(l) - 1
        if self.ints[lfind].r >= r:
            return lfind
        return -1

    def add(self, l, r):
        """ add interval [l,r],
        automatically merge exactly adjacent interval
            eg. intervals `[1,2],[4,10]`, add `[3,3]` it becomes `[1,10]`
        then return the merged interval
        """
        lfind, rfind = self.get_overlap(l, r)
        # if `self` exist overlaping intervals, merge into [l,r]
        if lfind <= rfind:
            for _ in range(rfind - lfind + 1):
                poped = self.ints.pop(lfind)
                l = min(l, poped.l)
                r = max(r, poped.r)

        # if a left interval can merge with [l,r]
        if lfind > 0:
            ll = self.ints[lfind - 1]
            if ll.r == l - 1:
                l = ll.l
                self.ints.pop(lfind - 1)

        # if a right interval can merge with [l,r]
        if rfind < len(self.ints) - 1:
            rr = self.ints[rfind + 1]
            if rr.l == r + 1:
                r = rr.r
                self.ints.pop(rfind + 1)

        new = Interval(l, r)
        self.ints.add(new)
        return new

    def erasepoint(self, x):
        """ erasepoint `x` and break interval into less than 2 intervals at point x """
        # the rightmost interval with left endpoint <= x
        find = self.ints.bisect_key_right(x) - 1
        if find == -1: return
        tar = self.ints[find]
        if tar.r >= x:
            self.ints.pop(find)
            if tar.l != tar.r:
                if tar.l != x:
                    self.ints.add(Interval(tar.l, x - 1))
                if tar.r != x:
                    self.ints.add(Interval(x + 1, tar.r))

    def __len__(self):
        return len(self.ints)


if __name__ == "__main__":
    tree = SortedIntervals()
    tree.add(1, 1)
    tree.erasepoint(0)
    tree.erasepoint(1)
    tree.add(-100, 100)
    tree.erasepoint(23)
    tree.erasepoint(24)
    tree.erasepoint(25)
    tree.erasepoint(100)
    tree.erasepoint(1022)
    tree.add(239, 10000)
    tree.add(24, 30)
    tree.add(24, 3000)
    print([(x.l, x.r) for x in tree.ints])