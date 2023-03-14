def dd(L):
    d1 = {}
    for elem in L:
        if elem not in d1:
            d1[elem] = 1
        else:
            d1[elem] += 1
    # print(d1)
    return d1


def is_list_permutation(L1, L2):
    '''
    L1 and L2: lists containing integers and strings
    Returns False if L1 and L2 are not permutations of each other. 
            If they are permutations of each other, returns a 
            tuple of 3 items in this order: 
            the element occurring most, how many times it occurs, and its type
    '''
    if len(L1) == len(L2) and len(L1) == 0:
        return (None, None, None)
    if len(L1) != len(L2):
        return False

    d1 = dd(L1)
    d2 = dd(L2)

    k1 = d1.keys()
    k2 = d2.keys()

    # Iguales elems
    for i in k1:
        if i not in k2:
            return False
    for i in k2:
        if i not in k1:
            return False

    # Iguales ocurrencias
    for i in k1:
        if d1[i] != d2[i]:
            return False

    maxOcurr = max(d1.values())

    for i in d1:
        if d1[i] == maxOcurr:
            return (i, maxOcurr, type(i))


# L1 = []
# L2 = []
# print('0: ', is_list_permutation(L1, L2))

# L1 = ['a', 'a', 'b']
# L2 = ['a', 'b']
# print('a: ', is_list_permutation(L1, L2))
L1 = [1, 'b', 1, 'c', 'c', 1]
L2 = ['c', 1, 'b', 1, 1, 'c']
print('rr: ', is_list_permutation(L1, L2))
