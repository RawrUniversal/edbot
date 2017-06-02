from discord import Embed
from datetime import datetime


def get_stats(config, icon, start_time):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")
    uptime = current_time - start_time

    em = Embed(color=0x00F4FF,
               title="Ed Bot Stats")

    em.add_field(name='Fun Commands',
                 value="\ned.joke: {}\ned.flip: {}\ned.range: {}\ned.gif: {}\ned.rpg: {}"
                 .format(config.get('Stats', 'jokes'), config.get('Stats', 'flips'),
                         config.get('Stats', 'ranges'), config.get('Stats', 'gifs'),
                         config.get('Stats', 'rpgs')
                         ),
                 inline=True)

    em.add_field(name='Information Commands',
                 value='ed.server: {}\ned.stats: {}\ned.help: {}'.format(config.get('Stats', 'servers'),
                                                                         config.get('Stats', 'stats'),
                                                                         config.get('Stats', 'helps'),
                                                                         config.get('Stats', 'schools')))

    em.add_field(name='Moderation Commands',
                 value='\ned.purge: {}\ned.ban: {}\ned.kick: {}'.format(config.get('Stats', 'purges'),
                                                                        config.get('Stats', 'bans'),
                                                                        config.get('Stats', 'kicks')))

    em.add_field(name='Statistics',
                 value="Current Up time: {}.".format(str(uptime)),
                 inline=True)

    em.set_footer(text=str(datetime.now().strftime('%b %d, %Y %H:%M')),
                  icon_url=icon)

    em.set_thumbnail(url=icon)
    return em


def set_stat(stat, config):
    if stat == 'joke':
        jokes = int(config.get('Stats', 'jokes')) + 1
        config.set('Stats', 'jokes', str(jokes))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'flip':
        flips = int(config.get('Stats', 'flips')) + 1
        config.set('Stats', 'flips', str(flips))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'range':
        ranges = int(config.get('Stats', 'ranges')) + 1
        config.set('Stats', 'ranges', str(ranges))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'gif':
        gifs = int(config.get('Stats', 'gifs')) + 1
        config.set('Stats', 'gifs', str(gifs))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'server':
        servers = int(config.get('Stats', 'servers')) + 1
        config.set('Stats', 'servers', str(servers))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'purge':
        purges = int(config.get('Stats', 'purges')) + 1
        config.set('Stats', 'purges', str(purges))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'help':
        helps = int(config.get('Stats', 'helps')) + 1
        config.set('Stats', 'helps', str(helps))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'stat':
        stats = int(config.get('Stats', 'stats')) + 1
        config.set('Stats', 'stats', str(stats))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'rpg':
        rpgs = int(config.get('Stats', 'rpgs')) + 1
        config.set('Stats', 'rpgs', str(rpgs))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'ban':
        bans = int(config.get('Stats', 'bans')) + 1
        config.set('Stats', 'bans', str(bans))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'kick':
        kicks = int(config.get('Stats', 'kicks')) + 1
        config.set('Stats', 'kicks', str(kicks))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    if stat == 'school':
        schools = int(config.get('Stats', 'schools')) + 1
        config.set('Stats', 'schools', str(schools))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
