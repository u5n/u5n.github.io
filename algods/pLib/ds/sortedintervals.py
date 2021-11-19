from sortedcontainers import SortedDict, SortedList
# def: a collection of disjoint closed intervals ( endpoint only integers )
#   have no complicated structures than sortedcontainers
# usg: get related operation access `self.sizes` or `self.ints` directly
# req: every inveral [l,r] appears, l should <= r 
class SortedIntervals:
    def __init__(self):
        # key: left endpoint
        # val: right endpoint
        self.ints = SortedDict()
        # enable to process interval by priority of interval size
        # (size, left endpoint)
        self.sizes = SortedList()
    
    def get_overlap(self, l, r):
        lfind = self.ints.bisect_left(l)
        rfind = self.ints.bisect_right(r) - 1
        if lfind > 0:
            if self.ints.peekitem(lfind - 1)[1] >= l:
                lfind -= 1
        return lfind, rfind
    def get_sub(self, l, r):
        # fully contained in [l,r]
        lfind = self.ints.bisect_left(l)
        rfind = self.ints.bisect_right(r) - 1
        # left endpoint in [l,r]
        if rfind >= lfind:
            if self.ints.peekitem[rfind][1] > r:
                return lfind, rfind-1
        return lfind, rfind
    def get_super(self, l, r):
        # [l,r] fully contained in
        lfind = self.ints.bisect_right(l) - 1
        if self.ints.peekitem[lfind][1] >= r:
            return lfind
        return -1
    def add(self, l, r):
        """ add interval [l,r] 
        if overlap 
            return None
        else 
            add this and automatically merge into big interval if possible 
            then return the merged interval
        """
        # rfind means first right interval of l
        # overlap_rfind means last right interval before r
        rfind, overlap_rfind = self.get_overlap(l, r)
        if rfind <= overlap_rfind: return None
        if rfind > 0:
            ll,lr = self.ints.peekitem(rfind-1)
            if lr == l-1:
                l = ll
                self.sizes.remove((lr-ll+1, ll))
        
        self.sizes.add((r-l+1,l))
        self.ints[l] = r
        if rfind != len(self.ints):
            rl, rr = self.ints.peekitem(rfind)
            if rl == r+1:
                r = rr
                self.ints[l] = r
                self.sizes.add((r-l+1, l))
                self.ints.pop(rl)
                self.sizes.remove(rr-rl+1, rl)
        return l,r
    
    def add_overlap(self, l, r):
        """ add interval [l,r]
        add this and automatically merge into big interval if possible 
        """
        lfind, rfind = self.get_overlap(l ,r)
        if lfind<=rfind:
            l = min(l, self.ints.peekitem(lfind)[0])
            r = max(r, self.ints.peekitem(rfind)[1])
            for _ in range(rfind-lfind+1):
                pop_l, pop_r = self.ints.popitem(lfind)
                self.sizes.remove((pop_r-pop_l+1, pop_l))
        self.ints[l] = r
        self.sizes.add((r-l+1,l))

    def break_at(self, x):
        """ break interval into less than 2 intervals at point x """
        # rightmost interval with left endpoint <= x
        find = self.ints.bisect_right(x) - 1
        if find == -1: return
        l,r = self.ints.peekitem(find)
        if r>=x:
            self.sizes.remove((r-l+1, l))
            self.ints.popitem(find)
            if l!=r:
                if l!=x:
                    self.ints[l] = x-1
                    self.sizes.add((x-l, l))
                if r!=x:
                    self.ints[x+1] = r
                    self.sizes.add((r-x, x+1))
    def __len__(self):
        return len(self.ints)

if __name__ == "__main__":
    tree = SortedIntervals()
    tree.add(1,1)
    tree.break_at(0)
    tree.break_at(1)
    tree.add(-100,100)
    tree.break_at(23)
    tree.break_at(24)
    tree.break_at(25)
    tree.break_at(100)
    tree.break_at(1022)
    tree.add(239, 10000)
    tree.add_overlap(24, 30)
    tree.add_overlap(24, 3000)
    print(tree.ints, tree.sizes)


