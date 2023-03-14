def laceStringsRecur(S1, S2):
    """
    s1 and s2 are strings.

    Returns a new str with elements of s1 and s2 interlaced,
    beginning with s1. If strings are not of same length,
    then the extra elements should appear at the end.
   """
    def helpLaceStrings(s1, s2, out):
        print('s1: ', s1, 's2: ',  s2, ' : out:', out + '\n')
        if s1 == '':
            # print('0000000000s1:::', out)
            return out + s2
        if s2 == '':
            # print('0000000000s2:::', out)
            return out + s1
        else:
            # PLACE A LINE OF CODE HERE
            # print('>>>>>>>>>> ' + str(round(len(out) / 2)))
            return helpLaceStrings(S1[round(len(out) / 2 + 1):],
                                   S2[round(len(out) / 2 + 1):],
                                   out +
                                   s1[0] +
                                   s2[0])

    return helpLaceStrings(S1, S2, '')


s1 = 'abcdef'
s2 = 'ABCDEF'
r = laceStringsRecur(s1, s2)
print('RESULTADO', r)
