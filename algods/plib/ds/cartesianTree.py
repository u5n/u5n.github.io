import operator
class CartesianTreeNode:
    """
    test: 
        @lc#2334
        @lc#654
    """
    __slots__ = 'key', 'val', 'left', 'right'
    def __init__(self, key, val, left=None, right=None):
        self.key, self.val, self.left, self.right = key, val, left, right
    def __str__(self): return f"({self.key},{self.val})"
    @staticmethod
    def buildfrom(A, opt = operator.lt):
        rchain = []
        for i,v in enumerate(A):
            last = None
            while rchain and opt(v, rchain[-1].val):
                last = rchain.pop()
            
            new = CartesianTreeNode(i, v, last)
            if rchain:
                rchain[-1].right = new
            rchain.append(new)
        
        return rchain[0]