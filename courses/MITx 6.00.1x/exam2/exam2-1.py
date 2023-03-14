def is_triangular(k):
    """
    k, a positive integer
    returns True if k is triangular and False if not
    """
    n = 1
    total = 0
    while total <= k:
        # print(total, n)
        if total == k:
            return True
        total += n
        n += 1
    return False


print(is_triangular(1))
print(is_triangular(3))
print(is_triangular(5))
print(is_triangular(6))
print(is_triangular(10))
print('r: ', is_triangular(14))
print('r: ', is_triangular(15))
print('r: ', is_triangular(16))
