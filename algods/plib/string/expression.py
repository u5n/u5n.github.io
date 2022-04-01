"""
calculate a expression, where
    the number should be integer
    support parentheses
    unary operator ['+', '-'] 
        assume unary operator has higher priority than binary operator
    binary opeartor ['+','-','*','%','/','^']
        '^' means `operator.pow`, which is right associative
        '%' means `operator.mod`
        '/' means truncated integer division
"""
from collections import namedtuple
from operator import *

# only binary operator
Opt = namedtuple("Operator", "prec func lasso", defaults=(True,))
chr_opt = {
    '+':Opt(1,add),
    '-':Opt(1,sub),
    '*':Opt(2,mul),
    '/':Opt(2,lambda l,r: l//r+(l%r!=0)*(l//r<0)),
    '%':Opt(2,mod),
    '^':Opt(3,pow,False),
    '(':Opt(0,None),
}

def calc(s):
    """ assume:
        `s` is a valid expression
        unary opertator has higher precedence than binary operator
    """
    s =  '(' + s + ')'
    optsta, valsta = [], []
    def calc_last():
        opt = optsta.pop()
        r = valsta.pop()
        l = valsta[-1]
        valsta[-1] = chr_opt[opt].func(l, r)

    prvtype = 0 # 1 means previous token(exclude parenthesis) is a number
    ps = 0
    while ps < len(s):
        if s[ps].isspace(): ps += 1
        # is a number or unary operator
        elif s[ps].isdigit() or (prvtype==0 and s[ps] in '-+' ): 
            sig = 1
            # parse continuous unary opeartor + -
            while not s[ps].isdigit():
                if s[ps]=='-': sig*=-1
                ps += 1

            num = 0
            while s[ps].isdigit():
                num = num*10 + (ord(s[ps])-48)
                ps += 1
            
            valsta.append(num*sig)
            prvtype = 1
        
        elif s[ps] == '(':
            optsta.append('('); ps += 1
        
        elif s[ps] == ')':
            while optsta[-1]!='(':
                calc_last()
            optsta.pop(); ps += 1

        # is a binary opt
        else:
            while optsta and (
                (chr_opt[optsta[-1]].lasso and chr_opt[optsta[-1]].prec >= chr_opt[s[ps]].prec)
                or (not chr_opt[optsta[-1]].lasso and chr_opt[optsta[-1]].prec > chr_opt[s[ps]].prec)
            ):
                calc_last()
            optsta.append(s[ps]); ps += 1
            prvtype = 0
    
    return valsta[-1]