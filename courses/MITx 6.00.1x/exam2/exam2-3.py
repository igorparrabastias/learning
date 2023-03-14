def cipher(map_from, map_to, code):
    """ map_from, map_to: strings where each contain 
                          N unique lowercase letters. 
        code: string (assume it only contains letters also in map_from)
        Returns a tuple of (key_code, decoded).
        key_code is a dictionary with N keys mapping str to str where 
        each key is a letter in map_from at index i and the corresponding 
        value is the letter in map_to at index i. 
        decoded is a string that contains the decoded version 
        of code using the key_code mapping. """
    key_code = {}
    for l in range(0, len(map_from)):
        key_code[map_from[l]] = map_to[l]

    decoded = ''
    for i in code:
        decoded += i

    return (key_code, decoded)


print(cipher("abcd", "dcba", "dab"))
# ({'a':'d', 'b': 'c', 'd': 'a', 'c': 'b'}, 'adc')
