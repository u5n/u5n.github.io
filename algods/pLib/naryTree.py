from collections import deque

class NaryTreeNode:
    def __init__(self, val, children=None):
        self.val,self.children = val,children
        
class BinaryTreeNode:
    def __init__(self,val,left=None,right=None):
        self.val,self.left,self.right=val,left,right
    def __repr__(self):
        return self.repr(self.val)
    @staticmethod
    def repr(x):
        """ input node or node.val or None """
        return str(x) if x!=None else 'N'
    def copy(self):
        return decode(self.encode())
    def pprint(self): pprint(self, self.repr)
    def encode(self, returnType="str"):
        q=[self]
        i = 0
        while i<len(q):
            cur = q[i]
            if cur:
                q.append(cur.left)
                q.append(cur.right)
            i+=1
        while q[-1]==None:
            q.pop()
        if returnType=="str":
            return '['+", ".join(str(e) if e!=None else 'null' for e in q)+']'
        else:
            return list(q)

def decode(datastr):
    """ decode use level order """
    if datastr=='': return None
    datastrlist = datastr.strip('[]').split(',')
    data=deque(int(e) if e.strip().isdigit() else None for e in datastrlist)
    root = BinaryTreeNode(data.popleft())
    q=deque([root])
    while q:
        cur=q.popleft()
        if data:
            v=data.popleft()
            if v!=None:
                cur.left=BinaryTreeNode(v)
                q.append(cur.left)
        if data:
            v=data.popleft()
            if v!=None:
                cur.right=BinaryTreeNode(v)
                q.append(cur.right)
    return root
    
def pprint(root, repr, compact=False):
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
        maxnumberlength_list = lambda l:max(map(lambda node:len(repr(node)),l))
        epArr = [ maxnumberlength_list(e) for e in A ]
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
        if compact:
            toappend = ''.join( map(lambda ee: ' '+repr(ee)+' ', e) )
        else:
            toappend = '|'.join( map(lambda ee: paddingaround(repr(ee), epArr[i], emptyspaceArr[i]), e) )
        eltrans.append(" "+toappend)
    
    print("BinaryTree[\n"+"\n".join(eltrans)+"\n]")

if __name__=="__main__":
    r = decode("[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]")
    r.pprint()
