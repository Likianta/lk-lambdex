# lk-lambdex

A simple way to compose multi-line anonymous function in Python.

The following examples explain all it has.

**Addition operation**

```py
# no args
add = lambdex((), '''
    x = 1
    y = 2
    return x + y
''')
print(add())

# with args
add = lambdex(('x', 'y'), '''
    return x + y
''')
print(add(1, 2))  # -> 3
```

**Pass globals**

```py
factor = 1000
kilometer_to_meter = lambdex(('km', {'factor': factor}), '''
    #                          ^^   ^----------------^
    #                          A.   B. put the dict at the END of tuple
    return km * factor
    #      ^^   ^----^
    #      A.   B.
''')

print(kilometer_to_meter(1))  # -> 1000
print(kilometer_to_meter(2))  # -> 2000
print(kilometer_to_meter(3))  # -> 3000
#                        ^ km
```

**Working with PyQt/PySide signals**

```py
# Repeater Signals: itemAdded(index, Item item)
repeater.itemAdded.connect(lambdex(('index', 'item'), '''
    print('new item added', index, item.property('objectName'))
'''))

# Button Signals: clicked()
button.clicked.connect(lambdex(({'btn': button}), '''
    btn.text = 'you clicked me'
'''))
```

# Installation

```
pip install lk-lambdex
```

To use it, simply import 'lambdex' from it:

```py
from lk_lambdex import lambdex

hello = lambdex((), '''
    print('hello world')
''')
```

# Advanced Usage

## Trick of "Context Variables"

```py
from lk_lambdex import lambdex


class AAA:
    name = 'aaa'

    def m(self, age):
        lamb1 = lambdex(({'self': self, 'age': age}), '''
            print(self.name)
            print(age)
        ''')

        # It is tedious if we have to pass many key-value with the same name.
        # In lk-lambdex 1.0.0 it supports auto detect context variables.
        # Just coding like this:
        lamb2 = lambdex((), '''
            print(self.name)
            print(age)
        ''')
```

## Callback Function

A special name 'somefunc' is the anonymous function's name.

Below is an example of Fibonacci, you can find the full example at [examples/fibnacci.py](./examples/03_fibonacci.py):

```py
from lk_lambdex import lambdex

fib = lambdex(('n'), '''
    if n <= 0:
        raise ValueError
        
    if n <= 2:
        return 1
        
    return somefunc(n - 1) + somefunc(n - 2)
''')

print(fib(10))  # -> 55
print(fib(2))  # -> 1
print(fib(1))  # -> 1
```

## Nested Function

```py
from lk_lambdex import lambdex

greeting = lambdex((), '''
    def say_hello():
        print('hello')
    say_hello()
''')
greeting()
```
