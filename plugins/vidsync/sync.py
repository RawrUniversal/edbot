from random import randint, choice
import string


def generate_link(log):
    # to generate a random vid sync room, a string 8 characters long must be generated containing
    # either numbers or letters, not case sensitive and in no particular order

    link = 'http://www.sync-video.com/r/'
    # begin by declaring an empty variable to hold the 8 generated characters
    room_id = ''

    log.info("attempting to generate a random room id")
    for i in range(0, 8):
        # generate a random int to determine if the current index (i) is going to be an integer or a character
        # the chance of either is 1/2 / 50%
        rand_int = randint(0, 1)

        # if 0, generate a random letter
        if rand_int == 0:
            # generate a random letter from a - z capitalized or un-capitalized
            rand = choice(string.ascii_letters)

        # if 1, generate a random integer
        elif rand_int == 1:
            rand = str(randint(0, 9))

        if rand is not None:
            # append this random integer or letter to final variable
            room_id += rand
        else:
            log.error('char: {} is not valid'.format(rand))

        # log information about this loop
        log.info('loop {}/8:'.format(i + 1))
        log.info('letter/integer: {}'.format(rand))
        log.info('rand_int = {}'.format(rand_int))

    log.info('final room id: {}'.format(room_id))
    return '**{}{}**'.format(link, room_id)






