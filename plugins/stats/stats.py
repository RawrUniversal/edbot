from discord import Embed
from datetime import datetime


def get_stats(config, icon, start_time):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")
    uptime = current_time - start_time

    em = Embed(color=0x00F4FF,
               title="Ed Bot Stats")

    em.add_field(name='Fun Commands',
                 value="\ned.joke: {}\ned.flip: {}\ned.range: {}\ned.gif: {}".format(config.get('Stats', 'jokes'),
                                                                                     config.get('Stats', 'flips'),
                                                                                     config.get('Stats', 'ranges'),
                                                                                     config.get('Stats', 'gifs')),
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

    em.add_field(name='Useful Commands',
                 value='\ned.vidsync: {}'.format(config.get('Stats', 'vidsyncs')))

    em.add_field(name='OSRS Commands',
                 value='\ned.rs.stats: {}\ned.rs.item: {}'.format(config.get('Stats', 'rs_stats'),
                                                                  config.get('Stats', 'rs_items')))

    em.add_field(name='Statistics',
                 value="Current Up time: {}.".format(str(uptime)),
                 inline=True)

    em.set_footer(text=str(datetime.now().strftime('%b %d, %Y %H:%M')),
                  icon_url=icon)

    em.set_thumbnail(url=icon)
    return em


def set_stat(stat, config):
    stat_plus_one = int(config.get('Stats', stat)) + 1
    config.set('Stats', stat, str(stat_plus_one))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
