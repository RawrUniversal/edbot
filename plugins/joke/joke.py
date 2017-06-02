from random import randint


# grab a random line from 'jokes.txt' file
def get_joke(log):
    log.info("Parsing command - ed.joke")
    try:
        with open('plugins/joke/jokes.txt') as jokes:
            content = jokes.readlines()
    except FileNotFoundError as errnfe:
        log.error(str(errnfe))
        return "Something broke while searching for a joke for you :disappointed:"

    # read each 'joke' or line into 'content' variable.
    jokes = [x.strip() for x in content]
    joke = jokes[randint(0, len(jokes) - 1)]
    log.info("Successfully parsed input...")
    log.info("sending back [{}] to server".format(str(joke)))
    return joke
