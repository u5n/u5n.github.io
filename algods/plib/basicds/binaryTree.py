"""
TOC
    class TreeNode
    def decode
    def pprint
    def size_cache
"""
from collections import deque
class TreeNode:
    __slots__ = 'val','left','right'
    def __init__(self,val,left=None,right=None):
        self.val,self.left,self.right=val,left,right
    def __str__(self):
        return f'TreeNode({TreeNode.rep(self)})'
    @staticmethod
    def rep(x):
        """ input node or None """
        return str(x.val) if x!=None else 'N'
    def copy(self):
        return decode(self.encode())
    def pprint(self, returnstr): 
        if returnstr:
            return pprint(self, TreeNode.rep, returnstr=returnstr)
        else:
            pprint(self, TreeNode.rep, returnstr=returnstr)
    def encode(self, returnType="str"):
        q=[self]
        for node in q:
            if node:
                q.append(node.left)
                q.append(node.right)

        while q[-1]==None:
            q.pop()
        if returnType=="str":
            return '['+", ".join(str(e.val) if e!=None else 'null' for e in q)+']'
        else:
            return list(q)

def decode(datastr):
    """ decode by level order """
    if not datastr: return None
    if not isinstance(datastr, str):
        datastr = str(datastr)
    datastrlist = datastr.strip('[]').split(',')

    data= deque(int(e) if e.strip().isdigit() else None for e in datastrlist)
    root = TreeNode(data.popleft())
    q=deque([root])
    while q:
        cur=q.popleft()
        if not data: break
        v=data.popleft()
        if v!=None:
            cur.left=TreeNode(v)
            q.append(cur.left)
    
        if not data: break
        v=data.popleft()
        if v!=None:
            cur.right=TreeNode(v)
            q.append(cur.right)

    return root
    
def pprint(root, rep, compact=False, returnstr=False):
    """
    pprint a binary tree at root, stringify each node use `vrepr` function

    compact:
        BinaryTree[
        5 
        4  8 
        11  N  13  4 
        7  2  N  N  N  N  5  1 
        ]
    uncompact:
        BinaryTree[
                                  5                           
                    4             |             8             
            11      |      N      |     13      |      4      
        7    |  2   |  N   |  N   |  N   |  N   |  5   |  1   
        ]
    """
    def eachlevel_perfect():
        """ iterate as if it's perfect binary tree"""
        q=[root]
        while True:
            level=q
            if all(e==None for e in level):
                return
            yield level
            q=[]
            for node in level:
                if node:
                    q.append(node.left)
                    q.append(node.right)
                else:
                    q.append(None)
                    q.append(None)
    el = list(eachlevel_perfect())
    def emptyspace(A):
        n = len(A)
        ret=[None]*n
        maxnumberlength_list = lambda layer:max(map(lambda node:len(rep(node)),layer))
        epArr = [ maxnumberlength_list(layer) for layer in A ]
        maxi = max(range(n),key=lambda i:epArr[i])
        INI_SPACES = 2
        def choose_bottomspace(x):
            ret[-1]=x
            for i in range(n-1,maxi,-1):
                ret[i-1]=2*(ret[i]+epArr[i])-epArr[i-1]+1
                if ret[i-1]<INI_SPACES: return False
            return True
        def lower_bound():
            r=INI_SPACES
            while choose_bottomspace(r)==False:
                r*=2
            l=INI_SPACES
            while l<r:
                m=(l+r)//2
                if choose_bottomspace(m):
                    r=m
                else:
                    l=m+1
            choose_bottomspace(l)
            
        lower_bound()
        for i in range(maxi-1,0-1,-1):
            ret[i]= (ret[i+1]+epArr[i+1])*2-epArr[i]+1
        return ret,epArr
    emptyspaceArr,epArr = emptyspace(el)
    def paddingaround(s,maxs,rightspace):
        spa = maxs-len(s)+rightspace
        return ' '*(spa//2)+s+' '*(spa-spa//2)
    eltrans = []
    for i,e in enumerate(el):
        # `ee` is TreeNode
        if compact:
            toappend = ''.join( map(lambda ee: ' '+rep(ee)+' ', e) )
        else:
            toappend = '|'.join( map(lambda ee: paddingaround(rep(ee), epArr[i], emptyspaceArr[i]), e) )
        eltrans.append(" "+toappend)
    
    printedstr = "BinaryTree[\n"+"\n".join(eltrans)+"\n]"
    if returnstr:
        return printedstr
    else:
        print(printedstr)

    
if __name__=="__main__":
    import sys
    sys.setrecursionlimit(1000000000)
    def f():
        d = 0
        root = r = TreeNode(d); d+=1
        for _ in range(10000):
            r.left = TreeNode(d); d+=1
            r = r.left
        c = 0
        def dfs(x, d):
            # A = d*[1]
            if x.left:
                dfs(x.left, d+1)
            if x.right:
                dfs(x.right, d+1)
            # c+=d+sum(A)
        dfs(root, d)
    f()