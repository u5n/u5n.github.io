class NaryTreeNode:
    def __init__(self, val, children=None):
        self.val = val
        self.children = children if children else []

    def encode(self, method='preorder'):
        method = method.replace(" ", "").lower()
        if method == 'preorder' or method == 'dfs':
            return self.encode_preorder()
        if method == 'levelorder' or method == 'bfs':
            pass

    def encode_preorder(self):
        stru = []

        def dfs(x):
            uid = len(stru)
            stru.append([x.val, 1])
            for chi in x.children:
                stru[uid][1] += dfs(chi)
            return stru[uid][1]
        dfs(self)
        return stru


def decode_preorder(stru):
    iterstru = iter(stru)

    def dfs():
        val, sz = next(iterstru)
        root = NaryTreeNode(val)
        sz_var = sz - 1
        while sz_var:
            print(val, sz_var)
            child, child_sz = dfs()
            sz_var -= child_sz
            root.children.append(child)
        return root, sz
    return dfs()[0]


if __name__ == '__main__':
    r = NaryTreeNode(1)
    r.children = [NaryTreeNode(2), NaryTreeNode(3), NaryTreeNode(4)]
    r.children[0].children = [NaryTreeNode(5), NaryTreeNode(6), NaryTreeNode(7)]
    r.children[2].children = [NaryTreeNode(8), NaryTreeNode(9)]
    A = r.encoding()
    print(A)
    r2 = decode_preorder(A)
    print(r2.encoding())
