def dict_invert(d):
    '''
    d: dict
    Returns an inverted dictionary according to the instructions above
    '''
    di = {}
    for item in d.items():
        # print(item[0])
        # print(di.keys())
        if item[1] in di:
            di[item[1]].append(item[0])

        else:
            di[item[1]] = [item[0]]
    for item in di.items():
        di[item[0]] = sorted(item[1])
    return di


d = {1: 10, 2: 20, 3: 30}
# {10: [1], 20: [2], 30: [3]}
print(dict_invert(d))

d = {1: 10, 2: 20, 3: 30, 4: 30}
# {10: [1], 20: [2], 30: [3, 4]}
print(dict_invert(d))

d = {4: True, 2: True, 0: True}
# {True: [0, 2, 4]}
print(dict_invert(d))
