import configparser
import asyncio
import logging
from datetime import datetime

import discord

# import plugin modules
from edbot.plugins.help import help
from edbot.plugins.flip import flip
from edbot.plugins.gif import gif
from edbot.plugins.joke import joke
from edbot.plugins.range import range as prange
from edbot.plugins.school import school
from edbot.plugins.server import server
from edbot.plugins.stats import stats

from edbot.plugins.vidsync import sync

from edbot.plugins.runescape import hiscores
from edbot.plugins.runescape import item_lookup

from edbot.plugins.rpg_v2 import rpg2

# setup logging system for logging to console/file
# create a timestamp when program starts
timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
time = datetime.strptime(timestamp, "%Y-%m-%d %H-%M-%S")

# setup base logger var
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create formatter used before every log entry
formatter = logging.Formatter('%(asctime)s | %(levelname)s --- %(message)s')

# create file handler with unique name on startup
fh = logging.FileHandler("logs/{}.log".format(str(timestamp)))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# create stream handler. put logger info into console as well as file created.
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# setup configparser
config_file = configparser.ConfigParser()
try:
    config_file.read('config/config.ini')
except configparser.Error as cperr:
    logger.error("Error while trying to read config.ini: [{}]".format(str(cperr)))

# create base client variable
client = discord.Client()


# when client connects and bot is ready
@client.event
@asyncio.coroutine
def on_ready():
    logger.info("LOGGED IN AS USER: {} | ID: {}".format(client.user.name, client.user.id))


# main on_message method, when a message is sent to the discord server, it is parsed and checked to see
# if the content in the message starts with, or matches the logic below.
# many of the methods called are done so from the 'plugins' library.
@client.event
@asyncio.coroutine
def on_message(message):

    ################
    # FUN COMMANDS #
    ################

    # if message is ed.flip
    if message.content == 'ed.flip':
        current_flip = flip.coin_flip(logger, message.author.name)
        yield from client.send_message(message.channel, current_flip)
        stats.set_stat('flip', config_file)

    # if message starts with ed.range
    elif message.content.startswith('ed.range'):
        yield from client.send_message(message.channel, prange.pick_number(message.content, logger))
        stats.set_stat('range', config_file)

    # if message is ed.joke
    elif message.content == 'ed.joke':
        yield from client.send_message(message.channel, joke.get_joke(logger))
        stats.set_stat('joke', config_file)

    elif message.content.startswith('ed.gif'):
        yield from client.send_message(message.channel, gif.get_gif_url(message.content, logger, message.author))
        stats.set_stat('gif', config_file)

    # if message is ed.school
    elif message.content == 'ed.school':
        yield from client.send_message(message.channel, school.school_start())
        stats.set_stat('school', config_file)

    ########################
    # INFORMATION COMMANDS #
    ########################

    # if message is ed.server
    elif message.content == 'ed.server':
        yield from client.send_message(message.channel, embed=server.get_server_information(message.server))
        stats.set_stat('server', config_file)

    # if message is ed.help
    elif message.content == 'ed.help':
        em = help.create_help_embed(client.user.avatar_url, logger, message.author)
        yield from client.send_message(message.author, embed=em)
        stats.set_stat('help', config_file)

    elif message.content == 'ed.stats':
        stats.set_stat('stat', config_file)
        yield from client.send_message(message.channel,
                                       embed=stats.get_stats(config_file, client.user.avatar_url, time))

    ###################
    # USEFUL COMMANDS #
    ###################

    elif message.content == 'ed.vidsync':
        yield from client.send_message(message.channel, sync.generate_link(logger))
        yield from client.delete_message(message)

    ######################
    # RUNESCAPE COMMANDS #
    ######################

    elif message.content.startswith('ed.rs.stats'):
        rs_stats = hiscores.get_hiscores(hiscores.get_username(message.content))
        if rs_stats['stats']['overall']['level'] < 50:
            yield from client.send_message(message.channel, "This account doesn't exist, or, the stats are too low!")
        else:
            em = hiscores.gen_embed(rs_stats)
            yield from client.send_message(message.channel, embed=em)

    elif message.content.startswith('ed.rs.item'):
        item = item_lookup.check_item(message.content)
        if item is False:
            yield from client.send_message(message.channel, "That item doesn't exist!")
            return

        data = item_lookup.request_item_json(item)
        yield from client.send_message(message.channel, embed=item_lookup.generate_embed(data))

# attempt to connect client to discord using the discord token located in config.ini file
try:
    client.run(config_file.get('Discord', 'token'))
# in case any error is thrown, log the error
except client.on_error as coeerr:
    logger.error("client.run error: [{}]".format(str(coeerr)))

