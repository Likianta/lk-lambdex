import traceback
# noinspection PyProtectedMember
from sys import _getframe as getframe
from textwrap import dedent
from typing import Union


def lambdex(args: Union[tuple, str, dict], code: str, **kwargs):
    """

    Args:
        args: (str, ..., optional dict)|str|dict.
            e.g. ('x')
                 ('x', 'y')
                 ('x', 'y', {'factor': 1000})
                            ^ put 'kwargs' as a dict in the last pos of args
            tip: dict
        code: long str. you can start with indent, we'll deindent it then.

    References:
        https://github.com/likianta/lambdex/examples

    Usages:
        See `https://github.com/likianta/lambdex/examples`
    """
    _last_frame = getframe(1)
    #   refer: https://www.cnblogs.com/LegendOfBFS/p/3500227.html
    context = _last_frame.f_locals  # type: dict
    
    # 1. args_
    if args:
        if isinstance(args, str):
            args_, globals_ = args, {}
        elif isinstance(args, dict):
            args_, globals_ = '', args
        # else assert isinstance(args, tuple)
        elif isinstance(args[-1], dict):
            args_, globals_ = ', '.join(args[:-1]), args[-1]
        else:
            args_, globals_ = ', '.join(args), {}
    else:
        args_, globals_ = '', {}
    
    # 2. globals_
    globals_.update(context)
    globals_.update(kwargs)
    globals_.update({
        '__source_code': (code := dedent(code).split('\n')),
        'traceback'    : traceback,
    })
    
    # 3. code_
    # note: `somefunc` is the function name of `code`, we need to add a wrapper
    # for `somefunc`, to make sure `somefunc` accepts recursive calls. see
    # reasons at <https://stackoverflow.com/questions/871887/using-exec-with
    # -recursive-functions> and some tests at <https://github.com/likianta
    # /lambdex/examples/03_fibonacci.py>
    code_ = dedent('''
        def __lambdex_func_wrapper({args}):
            
            def somefunc({args}):
                {body}
                
            try:
                return somefunc({args})
            except Exception as e:
                for frame, lineno in traceback.walk_tb(e.__traceback__):
                    lineno -= 5
                    #   number 5 counts the number of lines from `def __lambdex_
                    #   func_wrapper` to `{{body}}`
                    if 0 <= lineno < len(__source_code):
                        print(
                            '\033[31m' +
                            f'error at line {{lineno}}: ' +
                            __source_code[lineno] +
                            '\033[0m'
                        )
                raise e
            
        LAMBDEX_RESULT = __lambdex_func_wrapper
    ''').format(
        args=args_,
        body='\n        '.join(code)
        #       ^------^ 8 whitespaces, follows the indent of '{body}'
    )
    
    somefunc = _exec(code_, globals_, ret="LAMBDEX_RESULT")
    # print(code_, somefunc)
    
    return eval(f'lambda {args_}: somefunc({args_})', {'somefunc': somefunc})


def _exec(code: str, globals_: dict, ret='RESULT'):
    """
    Usages:
        # == 1. no args ==
        a = _exec('''
            x = 1
            y = 2
            RESULT = x + y
        ''')
        print(a)  # -> 3

        # == 2. with args ==
        b = lambda x, y: _exec('''
            RESULT = x + y
        ''', {'x': x, 'y': y})
        print(b(1, 2))  # -> 3

    References:
        https://stackoverflow.com/questions/1463306/how-does-exec-work-with
        -locals
    """
    locals_ = {}
    exec(code, globals_, locals_)
    return locals_[ret]
