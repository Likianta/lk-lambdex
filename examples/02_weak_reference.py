from lk_lambdex import lambdex

a = {'a': 'aa'}
b = lambdex({'adict': a}, '''
    print(adict)  # -> {'a': 'aa'}
    adict.update({'b': 'bb'})
''')()
print(a)  # -> {'a': 'aa', 'b': 'bb'}
