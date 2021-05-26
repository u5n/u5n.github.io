class ListNode:
    def __init__(self, val=None, nxt=None, prv=None):
        self.val,self.nxt,self.prv = val,nxt,prv
    def __repr__(self): return str(self.val)
    def asHead(self):
        ret = []
        cur = self
        while cur:
            ret.append(cur.val)
            cur=cur.nxt
        return ret
# head = z.senhead.nxt
# z.sentail.prv.nxt = None
# print(head.asHead())
class DoublyLinkedList:
    def __init__(self, arr=None):
        self.senhead = ListNode("senhead") # L[-1]
        self.sentail = ListNode("sentail") # L[n]
        self.senhead.nxt = self.sentail
        self.sentail.prv = self.senhead
        self.sz = 0
        if arr:
            for e in arr:
                self.append(ListNode(e))
    def __len__(self): return self.sz
    def __getitem__(self, i): return self.index(i).val
    def __setitem__(self, i, e): self.index(i).val = e
    def __delitem__(self, i): self.detach(self.index(i))
    def __repr__(self): return f"LL({list(self)})"
    
    def front(self):return self.index(0)
    def back(self):return self.index(self.sz-1)
    def append(self, node): self.insert(self.sz, node)
    def appendleft(self, node): self.insert(0, node)
    def insert(self, i, node):
        nxt = self.index(i, sentinel=True)
        prv = nxt.prv
        prv.nxt = node
        node.nxt = nxt
        node.prv = prv
        nxt.prv = node
        self.sz+=1
    def pop(self, i=None):
        if i==None: i=self.sz
        cur = self.index(i, sentinel=True)
        nxt, prv = cur.nxt, cur.prv
        prv.nxt = nxt
        nxt.prv = prv
        self.detach(cur)
        return cur
    def popleft(self): return self.pop(0)
    def detach(self, *nodes):
        for node in nodes:
            prvNode = node.prv
            nxtNode = node.nxt
            if prvNode:
                prvNode.nxt = nxtNode
            if nxtNode:
                nxtNode.prv = prvNode
            self.sz -= 1
    def index(self, i, sentinel=False):
        if i<0 or i>=self.sz:
            if sentinel:
                if i==-1: return self.senhead
                elif i==self.sz: return self.sentail
            raise IndexError
        if i<=self.sz-1-i:
            cur = self.senhead.nxt
            for _ in range(i):
                cur=cur.nxt
        else:
            cur = self.sentail.prv
            for _ in range(self.sz-1-i):
                cur=cur.prv
        return cur