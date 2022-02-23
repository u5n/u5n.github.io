import typing 
import sys, inspect
from timeit import default_timer as time

from plib.basicds.binaryTree import TreeNode, decode as binaryTree_decode
from plib.basicds.singlyLinkedlist import ListNode, toLinkedlist
from pathlib import Path

def D(func):
    """ decorator that send what function return to stdout
    _:name: Debug 
    application: run a function without `print(func(**))` """
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f'`{func.__name__}` return {repr(ret)}')
        return ret
    return wrapper

def L(loop=1, maxtime=3600, offset=0):
    """ name: Loop
    find the average runtime of a none parameter function 
    the runtime returned decreased by offset(ms)
    application: measure runtime
    """
    def LOOP_decorator(func):
        if 0==loop: return 
        acc = 0
        for i_l in range(loop):
            start = time()
            func()
            acc+= (-start+(start:=time()))
            if acc >= maxtime:
                raise Exception(f"run {i_l+1} loops with TLE")
        acc /= loop
        acc -= offset/1000
        if acc >= 1: print(f'{func.__name__} runs in {acc*1e3:.0f} (ms)')
        elif acc >= 0.001: print(f'{func.__name__} runs in {acc*1e3:.3f} (ms)')
        else: print(f'{func.__name__} runs in {acc*1e3:.6f} (ms)')
    return LOOP_decorator


def str_return(ret, argtype):
    if argtype == type(None):
        ret = 'null'
    elif argtype == str:
        ret = f'"{ret}"' # assume no special chars appears in `ret``
    elif argtype == typing.Union[TreeNode, type(None)]:
        ret = ret.encode()
    elif argtype == typing.Union[ListNode, type(None)] or argtype == ListNode:
        ret = list(ret)
    
    return str(ret)
def run_function_usestd(f, detail, selected, custom_input):
    paras = inspect.getfullargspec(f)
    narg = len(paras.args)-1 # exclude `self` parameter
    
    i_cases = 0
    while True:
        if None!=custom_input:
            args = custom_input
            custom_input = None
            i_cases = -1
            selected = {-1} # don't run anyother testcase from input
            print("Custom Test\t")
        else:
            try:
                # get arg from stdin and change to python type
                raw_args = [input() for _ in range(narg)]
                if selected and i_cases not in selected:
                    i_cases += 1
                    continue
            
                args = [None]*narg
                for i in range(narg):
                    arg_type =  paras.annotations[paras.args[1+i]]
                    if arg_type == typing.Union[TreeNode, type(None)]:
                        args[i] = binaryTree_decode(raw_args[i])
                    elif arg_type == typing.Union[ListNode, type(None)] or arg_type == ListNode:
                        args[i] = toLinkedlist(eval(raw_args[i]))
                    else:
                        args[i] = eval(raw_args[i])

                
                if detail:
                    str_raw_args  = "; ".join(map(lambda rarg: rarg if len(rarg)<100 else rarg[:100]+'......', raw_args))
                    print(f"Test {i_cases}\n\tinput:", str_raw_args)
            except EOFError:
                return

        start = time(); ret = f(*args); duration = time() - start

        arg_type = paras.annotations['return']
        ret = str_return(ret, arg_type)

        if len(ret) > 200:
            ret = ret[:200] + "... too long, hidden"

        if detail:
            print("\toutput:", ret)
            print("\ttime: %.3f ms"%(1000*(duration)))
        else:
            print(ret)

        i_cases += 1

def run_multifunction_usestd(cls, detail):
    # assume only one testcase
    function_names = eval(input())
    function_paras = eval(input())
    i_fp = iter(function_paras)
    i_fn = iter(function_names); next(i_fn) # skip the ctor
    duration = 0
    obj = cls(*next(i_fp))
    rets = []
    for method_name, method_paras in zip(i_fn, i_fp):
        f = getattr(obj, method_name)
        start = time()
        ret = f(*method_paras)
        duration += time()-start
        rets.append(ret)

    rets = str(rets)
    if len(rets) > 200:
        rets = rets[:200] + "... too long, hidden"

    if detail:
        print("\toutput:", rets)
        print("\ttime: %.3f ms"%(1000*(duration)))
    else:
        print(rets)
    return obj
        
def Dl(selected={}, detail = False, solution_cls=None, custom_input=None):
    """ 
    name: Debug for leetcode
    des:
        find solution_name class in module __main__
        if solution_name is "Solution":
            find the first function with annotation
            create one `Solution` object
            run the first function use input from sys.stdin
        else:
            example: @lc#2102
        return: return the object used to run 
    paras:
        selected: 
            type:iterable
            only run testcases if its id in `selected`
            if empty, don't filter testcase
            if None, don't run any testcase
        custom_input:
            when `solution_cls` is None, allow change input in code file, only contain one testcase 
    """
    if selected is None: return
    if solution_cls is None:
        for name, cls in inspect.getmembers(sys.modules["__main__"]):
            if name == "Solution":
                cans = [] # candidates functions
                obj = cls() # create only one `Solution` object for multiple testcases
                for method_name in dir(obj):
                    if not method_name.startswith('__'):
                        cans.append(getattr(obj, method_name))
                
                if len(cans)==0:
                    raise Exception("`Solution` don't have single method")
                # has only one method
                elif len(cans)==1:
                    f = cans[0]
                # has multiple method, select the first one with annotations
                else:
                    for can in cans:
                        try:
                            paras = inspect.getfullargspec(can)
                        except TypeError:
                            # incase the `@cache` wrapper is applied into `can`
                            continue
                        
                        if len(paras.annotations)!=0:
                            f = can
                            break
                    else:
                        raise Exception("no function has annotations ")
                
                run_function_usestd(f, detail, selected, custom_input)
                return obj
        else:
            raise Exception(f"don't have a `Solution` class")
    else:
        # return object of `solution_cls`
        return run_multifunction_usestd(solution_cls, detail)

def C(filename, nskip=2, template=None):
    d  = {'NAME':0, 'OP':0, 'LITERAL':0,'LINE':0}
    # count not-empty lines, also find some special situations
    with open(filename) as f:
        multilineString = False
        for line in f.readlines():
            if multilineString:
                if line.rstrip().endswith('"""'):
                    multilineString = False
                continue
            if line.lstrip().startswith('#'): continue
            elif line.strip() == '': continue
            elif line.lstrip().startswith('"""'):
                multilineString = True
            d['LINE'] += 1
    d['LINE'] -= nskip

    """ find code complexity """
    import tokenize
    import io
    def update_d(token, add=1, prvtoken=None):
        if token.type==1: 
            if token.string == 'False' or token.string == 'True':
                d['LITERAL'] += add
            else:
                d['NAME'] += add
        elif token.type==54: # OP
            if token.string in '}]);': 
                return
            if prvtoken and prvtoken.type==54:
                # special case1, "1 - -----2", only has one operator
                if token.string in '+-' and prvtoken.string in '+-':
                    return
            d['OP'] += add
        elif token.type in {2,3}: 
            # token.type == 2: # NUMBER
            d['LITERAL'] += add
        
    def checkfile(filename):
        """ use `tokenize` analysis a python file """
        with tokenize.open(filename) as f:
            for _ in range(nskip):
                f.readline()
            tokens = tokenize.generate_tokens(f.readline)
            prvtoken = None
            for token in tokens:
                update_d(token, prvtoken=prvtoken)
                prvtoken = token
        if template:
            d['LINE'] -= template.count('\n')
            for token in tokenize.generate_tokens(io.StringIO(template).readline):
                update_d(token, -1)

    checkfile(filename)
    # print(f"code complexity: {{words:{d['NAME']+d['LITERAL']}, opt:{d['OP']} }}")
    print(d)
    print(f"code complexity: {d['NAME']+d['LITERAL']+d['OP']}")