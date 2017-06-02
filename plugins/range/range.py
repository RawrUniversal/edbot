from random import randint


# pick a random number between two numbers (1, message)
def pick_number(message, log):
    log.info("Parsing command - {}".format(message))
    # attempt to locate index of space character in passed message.
    try:
        space_index = message.index(" ")
    except ValueError as verr:
        log.error("ValueError = [{}] no space found for index search.".format(str(verr)))
        return "Did you remember to give me a max number? (ex: ed.range 100)."

    # check if input is 0
    if int((str(message[space_index + 1:])).strip()) is 0:
        log.error("ValueError = [the number 0 is an invalid input.]")
        return "I can't find a range using the number 0."

    # attempt to convert message object to an integer with white space removed.
    try:
        number = int((str(message[space_index + 1:])).strip())
    except ValueError as verr:
        log.error("ValueError = [{}]".format(str(verr)))
        return "{} isn't a correct input.".format(message[space_index + 1:])

    # choose a random integer between 1 and 'number' passed into method.
    num = str(randint(1, number))
    log.info("Successfully parsed input...")
    log.info("sending back [{}] to server".format(str(num)))
    return num
