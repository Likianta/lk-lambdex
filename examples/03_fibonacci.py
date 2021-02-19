from lk_lambdex import lambdex

''' 注意

`exec(...)` 可以处理自身回调函数的情形, 但是 `lambda: exec(...)` 在处理回调函数
时会引发错误:

NameError: global name 'xxx' is not defined!

要想让回调函数在匿名式中可用, 我们需要对它加一个 "外壳":

```
lambda: exec("""
def shell(...):
    def func(n):
        func(n - 1)  # 这里是一个自身回调
    return func(...)
shell(...)
""")
```
'''

# test 1: failed
# fib = lambda : exec('''
# def somefunc(n):
#
#     if n <= 0:
#         raise ValueError
#
#     if n <= 2:
#         return 1
#
#     return somefunc(n - 1) + somefunc(n - 2)
#
# print('fib test 1:', somefunc(10))
# ''')
# fib()


# test 2: succeed
# fib = lambda: exec('''
# def wrapper(n):
#
#     def somefunc(n):
#
#         if n <= 0:
#             raise ValueError
#
#         if n <= 2:
#             return 1
#
#         return somefunc(n - 1) + somefunc(n - 2)
#
#     return somefunc(n)
#
# print('fib test 2:', wrapper(10))
# ''')
# fib()

# test 3: succeed
fib = lambdex(('n',), '''
    if n <= 0:
        raise ValueError
        
    if n <= 2:
        return 1
        
    return somefunc(n - 1) + somefunc(n - 2)

''')

print('fib test 3.1:', fib(10))  # -> 55
print('fib test 3.2:', fib(2))  # -> 1
print('fib test 3.3:', fib(1))  # -> 1

try:
    print('fib test 3.4:', fib(0))  # -> ValueError
except ValueError:
    pass
