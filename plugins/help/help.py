from discord import Embed
from datetime import datetime


def create_help_embed(icon, log, author):
    time = datetime.utcnow()
    log.info("ATTEMPTING TO SEND ED.FLIP COMMAND FROM {} @ {}...".format(
        author, time
    ))

    em = Embed(color=0x00F4FF,
               title=":robot: Commands")

    em.add_field(name='Ed by Brett Currie',
                 value="*A bot written in Python using the Discord.py library. Say 'ed.help' to get a "
                       "list of commands.*\n",
                 inline=True)

    em.add_field(name='Moderation (Admin Only)',
                 value="ed.purge — purge current channel."
                       "\ned.ban — ban a user from the server."
                       "\ned.kick — kick a user from the server.",
                 inline=True)

    em.add_field(name='Information',
                 value="ed.server — show information regarding the server."
                       "\ned.stats — show Ed's stats."
                       "\ned.help — displays this splash screen."
                       "\ned.school — display the time remaining until classes begin.",
                 inline=True)

    em.add_field(name='Fun',
                 value="ed.joke — hear a hilarious joke."
                       "\ned.flip — flip a coin."
                       "\ned.range — choose a number between zero and x."
                       "\ned.gif — search for a gif.",
                 inline=True)

    em.add_field(name='RPG2 Commands — ed.rpg2.<command>',
                 value="rpg2 — basic command, if user has no character, create one for them, otherwise display users "
                       "player data."
                       "\nrpg2.fight — generate a random monster for the player to fight."
                       "\nrpg2.potion —use one of your players potion if one is available and you aren't already full "
                       "hp."
                       "\nrpg2.freepotion — check if you have a free potion available, players may take one every 20 "
                       "minutes."
                       "\nrpg2.leaders — check the current leaderboards for all living characters."
                       "\nrpg2.fallen — check the best players that have perished while in battle."
                       "\nrpg2.duel @(x) — duel a specific player.",
                 inline=True)

    em.set_footer(text=str(datetime.now().strftime('%b %d, %Y %H:%M')),
                  icon_url=icon)

    em.set_thumbnail(url=icon)

    log.info("SUCCESSFULLY CREATED A HELP EMBED OBJECT, RETURNING...")
    return em
