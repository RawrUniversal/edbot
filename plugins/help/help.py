from discord import Embed
from datetime import datetime


def create_help_embed(icon):
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
                       "\ned.gif — search for a gif."
                       "\ned.rpg — generate a random rpg character sheet.",
                 inline=True)

    em.set_footer(text=str(datetime.now().strftime('%b %d, %Y %H:%M')),
                  icon_url=icon)

    em.set_thumbnail(url=icon)

    return em
