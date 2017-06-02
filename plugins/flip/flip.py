from random import randint


# method to choose the number 1, or 2. return corresponding coin flip answer
def coin_flip():
    num = randint(1, 2)
    if num is 1:
        return 'Heads.'
    else:
        return 'Tails.'
