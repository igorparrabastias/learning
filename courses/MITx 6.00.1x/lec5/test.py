# def remove_dups(L1, L2):
#     for e in L1:
#         if e in L2:
#             L1.remove(e)


# L1 = [1, 2, 3, 4]
# L2 = [1, 2, 5, 6]
# remove_dups(L1, L2)

# print(L1)


# def remove_dups_new(L1, L2):
#     """
#     avoid mutating a list as you are iterating over it
#     """
#     L1_copy = L1[:]
#     for e in L1_copy:
#         if e in L2:
#             L1.remove(e)


# L1 = [1, 2, 3, 4]
# L2 = [1, 2, 5, 6]
# remove_dups_new(L1, L2)

# print(L1)

# def applyToEach(L, f):
#     for i in range(len(L)):
#         L[i] = f(L[i])


# testList = [1, -4, 8, -9]


# def ff(a):
#     return a**2


# applyToEach(testList, lambda x: x**2)
# print(testList)


# Python3 program for illustration
# of values() method of dictionary


# # numerical values
# dictionary = {"raj": 2, "striver": 3, "vikram": 4}
# print(type (dictionary.keys()))


# # string values
# dictionary = {"geeks": "5", "for": "3", "Geeks": "5"}
# print(dictionary.values())

# get vs [] for retrieving elements
# my_dict = {'name': 'Jack', 'age': 26}

# # Output: Jack
# print(my_dict['name'])

# # Output: 26
# print(my_dict.get('age'))

# # Trying to access keys which doesn't exist throws error
# # Output None
# print(my_dict.get('address'))

# # KeyError
# print(my_dict['address'])


# animals = {
#     'a': ['aardvark'],
#     'b': ['baboon'],
#     'c': ['coati'],
#     'd': ['donkey', 'dog', 'dingo'],
# }


# def how_many(aDict):
#     '''
#     aDict: A dictionary, where all the values are lists.

#     returns: int, how many values are in the dictionary.
#     '''
#     return sum(len(animalList) for animalList in aDict.values())


# print(how_many(animals))


animals = {
    'a': ['aardvark'],
    'b': ['baboon'],
    'c': ['coati'],
    'd': ['donkey', 'dog', 'dingo'],
}


def biggest(aDict):
    '''
    aDict: A dictionary, where all the values are lists.

    returns: The key with the largest number of values associated with it
    '''
    cont = {}
    biggerNumber = 0
    biggerKey = ''
    for tupl in aDict.items():
        if biggerKey == '':
            biggerKey = tupl[0]
        if tupl[0] not in cont:
            cont[tupl[0]] = 0
        cont[tupl[0]] += len(tupl[1])
        if cont[tupl[0]] > biggerNumber:
            biggerNumber = cont[tupl[0]]
            biggerKey = tupl[0]
    return biggerKey


print(biggest(animals))
