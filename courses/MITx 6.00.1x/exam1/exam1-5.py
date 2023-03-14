def score(word, f):
    """
       word, a string of length > 1 of alphabetical 
             characters (upper and lowercase)
       f, a function that takes in two int arguments and returns an int

       Returns the score of word as defined by the method:

    1) Score for each letter is its location in the alphabet (a=1 ... z=26) 
       times its distance from start of word.  
       Ex. the scores for the letters in 'adD' are 1*0, 4*1, and 4*2.
    2) The score for a word is the result of applying f to the
       scores of the word's two highest scoring letters. 
       The first parameter to f is the highest letter score, 
       and the second parameter is the second highest letter score.
       Ex. If f returns the sum of its arguments, then the 
           score for 'adD' is 12 
    """
    letterScore = {}
    for i in range(1, 27):
        letterScore[chr(i + 96)] = i

    lettersScore = {}
    i = 0
    for l in word:
        lettersScore[l] = letterScore[l.lower()] * i
        i += 1

    scores = sorted(list(lettersScore.values()))

    l1 = scores.pop()
    l2 = 0
    if len(scores):
        l2 = scores.pop()

    return f(l1, l2)


word = 'bbcdefABCDEF'
word = 'aa'


def f(a, b):
    return a + b


r = score(word, f)
print('RESULTADO', r)
