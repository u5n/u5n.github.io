"""
calculate a expression, where
    the number should be integer
    support parentheses
    unary operator ['+', '-'] 
        assume unary operator has higher priority than binary operator
            example `-2^2` should be 4
        assume unary operator always on the left

    binary opeartor ['+','-','*','%','/','^']
        '^' means `operator.pow`, which is right associative
        '%' means `operator.mod`
        '/' means truncated integer division

test: 
    @acw151; @lc#227; @lc#224; @lc#772
"""
import operator 

# binary operator
class Operator:
    def __init__(self, prec, func, chr='', lasso=True, unary = False):
        self.lasso, self.prec, self.func, self.unary, self.chr = lasso, prec, func, unary, chr
    def __str__(self):
        return self.chr

Opt = Operator
chr_bopt = {
    '+':Opt(1,operator.add,'+'),
    '-':Opt(1,operator.sub,'-'),
    '*':Opt(2,operator.mul,'*'),
    '/':Opt(2,lambda l,r: l//r+(l%r!=0)*(l//r<0),'/'),
    '%':Opt(2,operator.mod,'%'),
    '^':Opt(3,operator.pow,'^',False),
}
lpar_opt = Opt(-10000,None,'(') # a dummy opearator that has the lowest precedence

# all unary opeartor should has the same precedence(also higher than binary opeartor) and be right associative
chr_uopt = {
    '-': Opt(100,operator.neg,'-',False,True),
    '+': Opt(100,operator.pos,'+',False,True),
    '!': Opt(100,operator.pos,'+',False,True),
}

def calc(s):
    """ assume:
        `s` is a valid expression
        unary opertator has higher precedence than binary operator
    """
    s =  '(' + s + ')'
    optsta, valsta = [], []
    def calc_last():
        """ merge two nodes in the expression tree """
        opt = optsta.pop()
        if opt.unary:
            valsta[-1] = opt.func(valsta[-1])
        else:
            r = valsta.pop()
            l = valsta[-1]
            valsta[-1] = opt.func(l, r)

    # 1 means previous token(exclude parenthesis) is a number, used to distinguish unary operator and binary operator
    prvtype = 0 
    ps = 0
    while ps < len(s):
        if s[ps].isspace(): ps += 1
        # is numeric
        elif s[ps].isdigit(): 
            num = 0
            while s[ps].isdigit():
                num = num*10 + (ord(s[ps])-48); ps += 1
            
            valsta.append(num)
            prvtype = 1
        
        elif s[ps] == '(':
            optsta.append(lpar_opt); ps += 1
        
        elif s[ps] == ')':
            while optsta[-1]!=lpar_opt:
                calc_last()
            optsta.pop(); ps += 1

        # is a opt
        else:
            # is a unary opt
            if prvtype==0 and s[ps] in chr_uopt:
                cur_opt = chr_uopt[s[ps]]
            else:
                cur_opt = chr_bopt[s[ps]]
            
            while optsta and (
                (optsta[-1].lasso and optsta[-1].prec >= cur_opt.prec)
                or (not optsta[-1].lasso and optsta[-1].prec > cur_opt.prec)
            ):
                calc_last() 
            optsta.append(cur_opt); ps += 1
            prvtype = 0
        
        # print([str(c) for c in optsta], valsta)
        
    
    return valsta[-1]

if __name__ == "__main__":
    assert calc("-2^2") == 4