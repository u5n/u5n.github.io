from sortedcontainers import SortedList

class ValueSortedDict:
    """
    app: retainedBestCache
    """
    def __init__(self):
        self.dict = {}
        # only sort by value
        self.sortedEntry = SortedList(key=lambda x:x[1])
    
    def get(self, key, default=None):
        return default if key not in self.dict else self.dict[key]

    def __setitem__(self, key, value):
        ori = self.dict[key] 
        if ori == value: return
        self.sortedEntry.remove((key, ori))
        self.dict[key] = value
        self.sortedEntry.add((key, value))

    def __delitem__(self, key):
        if key in self.dict:
            self.sortedEntry.remove((key, self.dict[key]))
            del self.dict[key]
        else:
            raise Exception(f"KeyError: {key}")

    def setdefault(self, key, default=None):
        if key in self.dict:
            return self.dict[key]
        else:
            self.dict[key] = default
            self.sortedEntry.add((key, default))
            return default

    def get_kth_entry(self, k):
        """ des: k start from 0, find the key with kth smallest value( if there are duplicates, the order is undefined ) """
        return self.sortedEntry[k]