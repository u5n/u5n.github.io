from collections import deque
from stringUtil import *

def importFilter(line):
    if line.startswith('import') or line.startswith('from'):
        return False
    if not line.strip(): 
        return False
    return True
def indentLevel(line):
    ind = 0
    for c in line:
        if c == ' ':
            ind += 0.25
        elif c == '\t':
            ind += 1
        else:
            break
    return int(ind)
class Node:
    def __init__(self, level, content):
        self.children = deque()
        self.level = level
        self.content = content
        if self.content!=None:
            self.content = content.strip()
        self.tail = None
        self.wrapper = None
        self.parent = None
    def prependContentAsNode(self, content):
        self.children.appendleft(Node(self.level+1, content))
    def __repr__(self):
        return f"Node:{{{self.content}}}"

def forClauseMapper(s):
    prependChildcontent = None
    if "range" in s:
        # "for i in range(100,10-1,-1)"
        sarr = s.split(' ')
        varN = sarr[1]
        slice = substrFirstPar(sarr[3])
        if slice.count(',')==2:
            sta,end,step = slice.split(',')
            if not end.isdigit():end = f"int({end})"
            if int(step) > 0:
                content = f"for(int {varN}={sta}; {varN}<={end}; {varN}+={step})"+'{'
            else:
                content = f"for(int {varN}={sta}; {varN}<={end}; {varN}+={step})"+'{'
        elif slice.count(',')==1:
            sta,end = slice.split(',')
            if not end.isdigit():end = f"int({end})"
            content = f"for(int {varN}={sta}; {varN}<={end}; {varN}++)"+'{'
        else:
            end = slice
            if not end.isdigit():end = f"int({end})"
            content = f"for(int {varN}=0; {varN}<={end}; {varN}++)"+'{'
    else:
        # "for i,e in enumerate(A)"
        if "enumerate" in s: 
            varN1,varN2 = s.split(' ')[1].split(',')
            conN = substrFirstPar(s)
            content = f"for(int {varN1}=0; {varN1}<{conN}.size(); {varN1}++)"+'{'
            prependChildcontent = f"auto {varN2}={conN}[{varN1}]"
        # "for c in s"
        else:
            varN = s.split(' ')[1]
            conN = s.split(' ')[3][:-1]
            content = f"for(int {varN}=0; {varN}<{conN}.size(); {varN}++)"+'{'
    return (content, prependChildcontent)


def structureChange(node):
    content = node.content
    if not content: return
    if content.count(':')==1 and 'lambda' not in content:
        # example 'if pred: return 0'
        if content[-1]!=':':
            node.prependContentAsNode(content[content.index(':')+1:])
        content = content[:content.index(':')+1]
        
        if 'for' in content:
            content,prepend = forClauseMapper(content)
            if prepend:
                node.prependContentAsNode(prepend)
            node.tail = '}'
        elif 'while' in content:
            content = f"while({content[5:-1].strip()}){{"
            node.tail = '}'
        elif 'class' in content or 'struct' in content: 
            node.tail = '};'
        elif 'else' in content: 
            content = content.replace(':', '')
            if len(node.children)>1:
                content += '{'
                node.tail = '}'
        elif 'if' in content:
            content = f"if({content[2:-1].strip()})"
            if len(node.children)>1:
                content += '{'
                node.tail = '}'
        elif 'elif' in content:
            content = f"else if({content[4:-1].strip()}){{"
            if len(node.children)>1:
                content += '{'
                node.tail = '}'
        elif 'def' in content:
            if node.level == 0 or 'def' not in node.parent.content:
                # ECLO "def solve(A, B):"
                funcN = content.split()[1].split('(')[0]
                paraList = substrFirstPar(content).split(',')
                paraList = ["auto "+para.strip() for para in paraList]
                content = f"auto {funcN}({', '.join(paraList)})"+'{'
                node.tail = '}'
            else:
                # ECLO "def dfs(root):"
                # ECLO "auto dfs = [&](auto root){"
                funcN = content.split()[1].split('(')[0]
                paraList = substrFirstPar(content).split(',')
                paraList = ["auto "+para.strip() for para in paraList]
                content = f"auto {funcN} = [&]({', '.join(paraList)})"+'{'
                node.tail = '};'

        content = content.replace(':','{')

    else:
        if 'for' in content:
            # ECLO "A=[1 for i in range(233)]"
            content = '#' + content 
        elif 'lambda' in content:
            content = '#' + content 
        elif '=' in content:
            for c in '+=','-=','^=','&=','|=','/=','%=','*=':
                if c in content:
                    break
            else:
                if 'auto' not in content:
                    content = 'auto ' + content 
        elif 'print' in content:
            content = '//' + content             
        else:
            pass
        content = content + ';'

    node.content = content

def wordLevelChange(line):
    line = line.replace('//','/')
    line = line.replace('#','// ')
    if 'len' in line:
        # ECLO 'len(A)'
        lenStarted = line.index("len")+3
        varN = substrFirstPar(line, sta=lenStarted)
        line = replacedFirstPar(line, lenStarted, "")
        line = line.replace("len()", f"{varN}.size()")

    if 'append' in line:
        # 'A.append([1,2,3,4])'
        appended = substrFirstPar(line, sta=line.index('append'))
        tup = substrFirstPar(appended)
        if tup.count(',')==1:
            # 'A.append((1,2))
            line = line.replace('append','emplace_back',1)
            line = replacedFirstPar(line, line.index('emplace_back'), f"pair<int, int>({tup})")
        elif tup.count(',')==0:
            line = line.replace('append','push_back',1)
        else:
            line = line.replace('append','push_back',1)
            line = replacedFirstPar(line, "{"+tup+"}")
            
    return line

def customAbbrChange(code):
    code = code.replace('pair<int, int>', 'pii')
    code = code.replace('pair<int,int>', 'pii')
    code = code.replace('vector<int>', 'vi')
    code = code.replace('long long', 'int64')
    code = code.replace('longlong', 'int64')
    code = code.replace('.first', '.fi')
    code = code.replace('.se', '.se')
    return code

with open("l1.py", "r") as f:
    code = f.read()
    code = code.split('\n')
    code = list(filter(importFilter, code))
    code = list(map(wordLevelChange, code))
    code = list(map(lambda line:Node(indentLevel(line), line), code))
    root = Node(-1, None)
    stack = []
    parent = root
    i = 0
    while i<len(code):
        line = code[i]
        while line.level <= parent.level:
            parent = stack.pop()
        
        if line.level == parent.level+2:
            stack.append(parent)
            parent = code[i-1]
        
        if '@' not in line.content:
            parent.children.append(line)
            line.parent = parent
        else:
            parent.children.append(code[i+1])
            code[i+1].parent = parent
            code[i+1].wrapper = code[i].content
            i+=1
        
        i+=1

    def dfs(r):
        structureChange(r)
        for c in r.children:
            dfs(c)
    dfs(root)
    
    ret = []
    def dfs2(r):
        if r.wrapper:
            ret.append(' '*(4*r.level) + r.wrapper)
        if r.content:
            ret.append(' '*(4*r.level) + customAbbrChange(r.content))
        for c in r.children:
            dfs2(c)
        if r.tail:
            ret.append(' '*(4*r.level) + r.tail)
    dfs2(root)
    ret = "\n".join(ret)
    ret = r"""#include "lib/m.h" 
    
""" + ret+ r"""

int main(){
    D(Solution())
}
"""
    print(ret)