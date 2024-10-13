def dotProduct(listA, listB):
    '''
    listA: a list of numbers
    listB: a list of numbers of the same length as listA
    '''
    acc = 0
    for i in range(len(listA)):
        p = listA[i] * listB[i]
        acc += p
    return acc


listA = [1, 2, 3]
listB = [4, 5, 6]

print(dotProduct(listA, listB))
