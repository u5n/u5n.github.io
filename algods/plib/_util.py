import typing 
import sys, inspect
from inspect import stack, getframeinfo
from timeit import default_timer as time

from plib.basicds.binaryTree import TreeNode, decode as binaryTree_decode
from plib.basicds.singlyLinkedlist import ListNode, toLinkedlist

def D(*args, **kwargs):
    """des: `print` function that used to debug, wrapper of print function
    """
    kwargs["file"] = sys.stderr
    caller = getframeinfo(stack()[1][0])
    print(f"l{caller.lineno}: ", *args, **kwargs)

def print_ret(func):
    """ decorator that send what function return to stdout
    application: run a function without `print(func(**))` """
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f'`{func.__name__}` return {repr(ret)}')
        return ret
    return wrapper

last_avg_runtime = [None]
def measure(loop=1, maxtime=3600, offset=0):
    """ 
    find the average runtime of a none parameter function 
    the runtime returned decreased by offset(ms)
    """
    def run_func(func):
        if 0>=loop: return 
        acc = 0
        def break_LOOP(*args):
            """ able to break loop from wrapped function """
            errormsg = f'debug info: {args}\n' if len(args)>0 else ''
            raise Exception(errormsg + f'{func.__name__} runs {i_l} loops in {acc/i_l - offset/1000} (ms), intermediate break with breaker')

        for i_l in range(1, 1+loop):
            nargs = len(inspect.signature(func).parameters)
            if nargs==0:
                start = time()
                func()
            elif nargs==1:
                start = time()
                func(break_LOOP)
            else:
                raise Exception("unsupported arguments size")
            
            _t = time(); acc += _t-start; start = _t

            if acc >= maxtime:
                raise Exception(f"run {i_l} loops with TLE")
        acc /= loop
        acc -= offset/1000
        last_avg_runtime[0] = acc*1e3
        if acc >= 1: print(f'{func.__name__} runs in {last_avg_runtime[0]:.0f} (ms)')
        elif acc >= 0.001: print(f'{func.__name__} runs in {last_avg_runtime[0]:.3f} (ms)')
        else: print(f'{func.__name__} each loop runs in {last_avg_runtime[0]:.6f} (ms)')


    # use as `@measure(...)`
    if isinstance(loop, int):
        return run_func
    # use as `@measure`
    else:
        func, loop = loop, 1
        run_func(func)


def repr_return(ret, ret_type):
    """ change the return value into string"""
    
    # try to check the types when [given ret_type in annotations and it was something like `List[int]`]
    if ret_type !="NOT EXIST" and not isinstance(ret_type, typing._GenericAlias): # 
        # allow type conversion
        if ret_type is float and type(ret) is int: 
            pass
        else:
            if (ret_type is None and ret!=None) or (ret_type and not isinstance(ret, ret_type)):
                return f'(return the wrong type) `{ret}` of type `{ret_type}`'

    if ret is None: return 'null'
    if ret_type is str:
        ret = f'"{ret}"' # assume no special chars appears in `ret``
    elif ret_type is typing.Union[TreeNode, type(None)] or ret_type is TreeNode:
        if ret: 
            ret = ret.pprint(returnstr=1)
    elif ret_type is typing.Union[ListNode, type(None)] or ret_type is ListNode:
        # as linkedlist head
        ret = list(ret)
    
    return str(ret)

def input_pyobj(raw_arg, arg_type):
    """ change input string into python object """
    pyobj_arg = eval(raw_arg.replace('null', 'None'))
    if arg_type is typing.Union[TreeNode, type(None)] or arg_type is TreeNode:
        return binaryTree_decode(pyobj_arg)
    # if use isubclass, make sure arg_type is a `class` not `type`
    elif arg_type is typing.Union[ListNode, type(None)] or arg_type is ListNode:
        return toLinkedlist(pyobj_arg)

    return pyobj_arg

def truncated(s, sz=200):
    if len(s)>sz:
        suf = "... too long, hidden"
        return s[:sz-len(suf)] + suf
    return s

def run_function_usestd(f, detail, selected, custom_testcase):
    paras = inspect.getfullargspec(f)
    narg = len(paras.args)-1 # exclude `self` parameter
    
    i_cases = 0
    while True:
        # assumption: there is no testcase take no parameters
        if custom_testcase:
            args, custom_testcase = custom_testcase, None
            selected = {-1} # don't run anyother testcase from input
            print("Custom Test\t")
        else:
            try:
                # get arg from stdin until EOF and change to python type
                raw_args = [input() for _ in range(narg)]
            except EOFError:
                break
            
            if selected and i_cases not in selected:
                i_cases += 1
                continue
        
            args = [None]*(narg)
            for i in range(narg):
                arg_type =  paras.annotations.get(paras.args[1+i], None)
                args[i] = input_pyobj(raw_args[i], arg_type)

            
            if detail:
                str_raw_args  = "; ".join(map(lambda rarg: rarg if len(rarg)<100 else rarg[:100]+'......', raw_args))
                print(f"Testcase {i_cases}\n\tinput:", str_raw_args)

        start = time(); ret = f(*args); duration = time() - start
        ret = truncated(repr_return(ret, paras.annotations.get('return', "NOT EXIST")))

        if detail:
            print("\toutput:", ret)
            print("\ttime: %.3f ms"%(1000*(duration)))
        else:
            print(ret)

        i_cases += 1

def run_obj_usestd(cls, detail, selected, custom_testcase):
    i_cases = 0
    obj = None
    while selected!={-1}:
        # assumption: custom testcase must be nonempty
        if custom_testcase: 
            (function_names, function_paras), custom_testcase = custom_testcase, None
            selected = {-1} # don't run anyother testcase from input
            print("Custom Test\t")
        else:
            try:
                # currently direct use eval, change to `input_pyobj` when needed
                function_names = eval(input())
                function_paras = eval(input())
            except EOFError: 
                break 

            if selected and i_cases not in selected:
                i_cases += 1
                continue
            
            if detail:
                print(f"Test {i_cases}\n\tfunc_names:", truncated(str(function_names)))
                print("\tfunc_args:", truncated(str(function_paras)))

        i_fp = iter(function_paras)
        i_fn = iter(function_names); next(i_fn) # skip the ctor
        obj = cls(*next(i_fp))

        duration = 0
        rets = []
        for method_name, method_paras in zip(i_fn, i_fp):
            f = getattr(obj, method_name)
            start = time()
            ret = f(*method_paras)
            duration += time()-start
            rets.append(ret) # don't use `repr_return`
        
        rets = truncated(str(rets).replace('None', 'null').replace("'", '"'))

        if detail:
            print("\toutput:", rets)
            print("\ttime: %.3f ms"%(1000*(duration)))
        else:
            print(rets)
        
        i_cases += 1
    # return last obj
    return obj

def lc_test(selected={}, detail = False, solution_cls=None, custom_testcase:list =None):
    """ 
    des:
        find solution_name class in module __main__
        if solution_name is "Solution":
            find the first public(not begin with '__') function with annotation
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
        custom_testcase:
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
                    raise Exception("`Solution` doesn't have public method")
                # has only one method
                elif len(cans)==1:
                    f = cans[0]
                # has multiple method, select the first one(function name is sort alphabetically) with return type annotated
                else:
                    f = None
                    for can in cans:
                        try:
                            paras = inspect.getfullargspec(can)
                        except TypeError:
                            # incase the `@cache` wrapper is applied into `can`
                            continue
                        
                        if len(paras.annotations)!=0:
                            f = can
                            break
                        
                    if f is None:
                        raise Exception("no function has annotations ")
                
                run_function_usestd(f, detail, selected, custom_testcase)
                return obj
        else:
            raise Exception(f"don't have a `Solution` class")
    else:
        # return object of `solution_cls`
        return run_obj_usestd(solution_cls, detail, selected, custom_testcase)





def file_code_quantity(filename, nskip=2, template=None):
    d  = {'NAME':0, 'OP':0, 'LITERAL':0,'LINE':0}
    # count not-empty lines, also find some special situations
    with open(filename) as f:
        multilineString = False
        nline = 1
        for line in f.readlines():
            validline = True
            if multilineString:
                if line.rstrip().endswith('"""'):
                    multilineString = False
                validline = False
            elif line.lstrip().startswith('#'): validline = False
            elif line.strip() == '': validline = False
            elif line.lstrip().startswith('"""'):
                multilineString = True
                validline = False

            if validline or nline <= nskip:
                d['LINE'] += 1
            nline += 1
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
                # print(token)
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