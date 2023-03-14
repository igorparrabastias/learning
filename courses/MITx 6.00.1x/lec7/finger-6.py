def rem(x, a):
    """
    x: a non-negative integer argument
    a: a positive integer argument

    returns: integer, the remainder when x is divided by a.
    """
    print(x, a)
    if x == a:
        return 0
    elif x < a:

        print('x', x)
        return x
    else:
        return rem(x-a, a)


print(rem(2, 5))
