from ps4a import *
wordList = loadWords()


def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.

    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    if word not in wordList:
        return False
    handClone = hand.copy()
    handKeys = handClone.keys()
    for i in word:
        if i not in handKeys:
            return False
        if i in handKeys:
            handClone[i] = handClone.get(i, 0) - 1
            if (handClone[i] < 0):
                return False
    return True


# test 1
hand = {'k': 1, 'o': 1, 'b': 1, 'w': 1, 'i': 2, 'j': 1}
word = "kwijibo"
isValidWord(word, hand, wordList)
