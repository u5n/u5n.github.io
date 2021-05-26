def substrFirstPar(s, sta=0):
    """ substr insider first parenthesis """
    l = 0
    ret = []
    expected = None
    for c in s[sta:]:
        if c=='(' and expected!=']':
            expected = ')'
            l+=1
        elif c=='[' and expected!=')':
            expected = ']'
            l+=1
        elif c==expected:
            l-=1
            if l==0: break
        if l>0:
            ret.append(c)
    return "".join(ret[1:])

def replacedFirstPar(s, sta, sub):
    return s[:sta] + s[sta:].replace(substrFirstPar(s[sta:]), sub, 1)
