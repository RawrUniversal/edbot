from discord import Embed
from dateutil import tz
from datetime import datetime


# main method to grab all server information
def get_server_information(server):
    # set total amount of members
    members = 0
    for member in server.members:
        members += 1

    # base variables for channel types
    total_channels = 0
    voice_channels = 0
    text_channels = 0

    # calculate different total channel variables
    for channel in server.channels:
        total_channels += 1
        if str(channel.type) == 'voice':
            voice_channels += 1
        elif str(channel.type) == 'text':
            text_channels += 1

    # calculate generic information about the server
    name = str(server.name)
    owner = str(server.owner.name)
    default_channel = str(server.default_channel.name)
    creation_date = get_server_creation_date(server.created_at)
    server_icon = server.icon_url

    # get all roles in server and users in each role
    roles = get_roles(server)

    # call create embed method to return
    return create_embed(members, total_channels, voice_channels, text_channels,
                        name, owner, default_channel, creation_date, roles,
                        server_icon)


# calculate server creation date formatted
def get_server_creation_date(created):
    here = tz.tzlocal()
    utc = tz.gettz('UTC')
    date = created.replace(tzinfo=utc)
    date.astimezone(here)
    return date


# create embed object to send through bot
def create_embed(members, total_channels, voice_channels, text_channels,
                 name, owner, default, created, roles, icon):
    em = Embed(color=0x00F4FF,
               title="{} Server Information".format(name))

    em.add_field(name='Generic',
                 value="Server Owner: *{}*\nTotal Members: *{}*\nDefault Channel: *{}*\nCreated At: *{}*"
                 .format(owner, members, default, created),
                 inline=True)

    em.add_field(name='Channel Information',
                 value='Total Channels: {}\nVoice Channels: {}\nText Channels: {}'
                 .format(total_channels, voice_channels, text_channels),
                 inline=True)

    em.add_field(name='User/Roles Information',
                 value=roles)

    em.set_footer(text=str(datetime.now().strftime('%b %d, %Y %H:%M:%S')),
                  icon_url=icon)

    em.set_thumbnail(url=icon)
    return em


# get all roles in server and amount of users in each role
def get_roles(server):
    roles = {}
    final_string = ""
    for member in server.members:
        for role in member.roles:
            if role.name not in roles:
                roles[role.name] = 0

        for role in member.roles:
            roles[role.name] += 1

    for item in roles.items():
        final_string += "{}: {}\n".format(item[0], item[1])

    return final_string
