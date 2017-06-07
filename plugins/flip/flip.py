from random import randint
from datetime import datetime


# method to choose the number 1, or 2. return corresponding coin flip answer
def coin_flip(log, author):
    time = datetime.utcnow()
    log.info("ATTEMPTING TO SEND ED.FLIP COMMAND FROM {} @ {}...".format(
        author, time
    ))

    # attempt to select a random number between 1 and 2
    try:
        log.info("SELECTING NUMBER BETWEEN 1-2 FOR FLIP...")
        num = randint(1, 2)
        log.info("NUMBER SELECTED = {}".format(num))
    # if an exception is raised, log this exception and log that the command has failed
    except Exception as e:
        log.error(str(e))
        log.error("ED.FLIP COMMAND WAS UNSUCCESSFUL...")
    if num is 1:
        log.info("COIN FLIP IS HEADS... RETURNING TO CLIENT")
        return 'Heads.'
    else:
        log.info("COIN FLIP IS TAILS... RETURNING TO CLIENT")
        return 'Tails.'
