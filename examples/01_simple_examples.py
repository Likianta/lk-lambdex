from lk_lambdex import lambdex

# addtion test
add = lambdex(('x', 'y'), '''
    return x + y
''')

print('addition test:', add(1, 2))  # -> 3

# km test
factor = 1000
kilometer_to_meter = lambdex(('km', {'factor': factor}), '''
    return km * factor
''')

print('km test:', kilometer_to_meter(1))  # -> 1000
print('km test:', kilometer_to_meter(2))  # -> 2000
print('km test:', kilometer_to_meter(3))  # -> 3000
