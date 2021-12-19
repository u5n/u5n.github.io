from copy import deepcopy
import typing 
import sys, inspect
from timeit import default_timer as time

from plib.basicds.binaryTree import TreeNode, decode as binaryTree_decode
from plib.basicds.singlyLinkedlist import ListNode, toLinkedlist
from pathlib import Path

def D(func):
    """ decorator that send what function return to stdut
    name: Debug """
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print(f'`{func.__name__}` return {repr(ret)}')
        return ret
    return wrapper

def L(loop=1, maxtime=3600):
    """ name: Loop
    find the average runtime of a none parameter function """
    def LOOP_decorator(func):
        if not loop: return 
        acc = 0
        for i_l in range(loop):
            start = time()
            func()
            acc+= (-start+(start:=time()))
            if acc >= maxtime:
                raise Exception(f"run {i_l+1} loops with TLE")
        acc /= loop
        if acc >= 1: print(f'{func.__name__} runs in {acc*1e3:.0f} (ms)')
        elif acc >= 0.001: print(f'{func.__name__} runs in {acc*1e3:.3f} (ms)')
        else: print(f'{func.__name__} runs in {acc*1e3:.6f} (ms)')
    return LOOP_decorator


def run_function_usestd(f, detail, selected):
    paras = inspect.getfullargspec(f)
    narg = len(paras.args)-1 # exclude `self` parameter
    
    i_cases = 0
    while True:
        try:
            raw_args = [input() for _ in range(narg)]
            args = [None]*narg
            for i in range(narg):
                arg_type =  paras.annotations[paras.args[1+i]]
                if arg_type == typing.Union[TreeNode, type(None)]:
                    args[i] = binaryTree_decode(raw_args[i])
                elif arg_type == typing.Union[ListNode, type(None)] or arg_type == ListNode:
                    args[i] = toLinkedlist(eval(raw_args[i]))
                else:
                    args[i] = eval(raw_args[i])

            if selected and i_cases not in selected:
                i_cases += 1
                continue
            
            if detail:               
                str_raw_args  = "; ".join(raw_args)
                if len(str_raw_args) < 100:
                    print(f"Test {i_cases}\n\tinput:", str_raw_args)
                else:
                    print(f"Test {i_cases}\n\tinput: {str_raw_args[:100]}... too long, hiden")
        except EOFError:
            return
        start = time(); ret = f(*args); end = time()


        if 'return' in paras.annotations:
            arg_type = paras.annotations['return']
            if ret is None:
                ret = str(ret)  
            elif arg_type == str or isinstance(ret, str):
                ret = repr(ret)
            elif arg_type == typing.Union[TreeNode, type(None)]:
                ret = ret.encode()
            elif arg_type == typing.Union[ListNode, type(None)] or arg_type == ListNode:
                ret = str(list(ret))    
        ret = str(ret)

        if len(ret) > 200:
            ret = ret[:200] + "... too long, hiden"

        if detail:
            print("\toutput:", ret)
            print("\ttime: %.3f ms"%(1000*(end-start)))
        else:
            print(ret)
        i_cases += 1

def Dl(detail = False, selected=None):
    """ 
    name: Debug for leetcode
    
    find `Solution` class module __main__
    find the first function with annotation
    run it use input from sys.stdin
    create only one `Solution` object
    """
    for name, cls in inspect.getmembers(sys.modules["__main__"]):
        if name == "Solution":
            cans = [] # candidates for function
            obj = cls() # create only one `Solution` object for multiple testcases
            for method_name in dir(cls):
                if not method_name.startswith('__'):
                    cans.append(getattr(obj, method_name))
            if len(cans)==0:
                raise Exception("`Solution` don't have single method")
            elif len(cans)==1:
                f = cans[0]
            else:
                for can in cans:
                    paras = inspect.getfullargspec(can)
                    if len(paras.annotations)!=0:
                        f = can
                        break
                else:
                    raise Exception("no function has annotations ")
            
            run_function_usestd(f, detail, selected)
            return
    else:
        raise Exception("don't have a `Solution` class")
