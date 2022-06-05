"""
array support insert pop getitem in O(lgn)
"""
from sortedcontainers import SortedDict
class array:
    """
    impl use sorted list
    """
    def __init__(self, A=None):
        if A:
            self.A = SortedList([],)

        else:
            self.A = SortedList()