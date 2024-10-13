def myLog(x, b):
    global g
    '''
    x: a positive integer
    b: a positive integer; b >= 2

    returns: log_b(x), or, the logarithm of x relative to a base b.
    '''
    g = x
    while b**g >= x:
        # print('g:', g, 'b:', b)
        # print('g**b:', g**b)
        g -= 1
    return g


print(myLog(27, 3))
print(myLog(26, 3))
print(myLog(28, 3))
