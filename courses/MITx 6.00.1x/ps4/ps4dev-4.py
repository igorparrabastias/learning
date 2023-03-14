from ps4a import *
wordList = loadWords()


def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string int)
    returns: integer
    """
    return sum(hand.values())


# test 1
hand = {'k': 1, 'o': 1, 'b': 1, 'w': 1, 'i': 2, 'j': 1}
print(calculateHandlen(hand))
