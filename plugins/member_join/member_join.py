from discord import Embed
from datetime import datetime


def ed_member_join(icon):
    em = Embed(color=0x00F4FF,
               title="Welcome To The NSCC I.T Discord Channel! :nscc_logo:")

    em.add_field(name='Nickname',
                 value="Please set your nickname to your **full name** so that it's easy to keep the member list"
                       "organized!",
                 inline=True)

    em.add_field(name='Server Role',
                 value="Please message ***Brett Currie*** or ***William MacNeil*** to have your role set properly!")

    em.add_field(name='Server Note',
                 value="If you get a second, set your server note to your NSCC W Number.\n")

    em.add_field(name='Questions?',
                 value="If you have any questions about the channel, message Brett Currie or William MacNeil.\n\n"
                       "If you have any questions regarding bot commands, type **ed.help**")

    em.set_footer(text=str(datetime.now().strftime('%b %d, %Y %H:%M')),
                  icon_url=icon)

    em.set_thumbnail(url=icon)

    return em
