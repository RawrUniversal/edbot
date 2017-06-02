from random import randint
from datetime import datetime
from discord import Embed


def generate_character(author):
    nick = author.nick
    space_loc = nick.index(" ")
    name = nick[:space_loc]

    name_adj = ['High-pitched', 'General', 'Deadpan', 'Hushed', 'Third',  'Big',  'Hulking', 'Screeching', 'Moaning',
                'Thankful', 'Typical', 'Conscious', 'Succinct', 'Grumpy', 'Waggish', 'Little', 'Telling', 'Obtainable',
                'Coherent',  'Red',  'Marked', 'Steady', 'Squeamish', 'Famous', 'Tedious', 'Truthful', 'Sincere',
                'Abusive', 'Mature', 'Short', 'Silent', 'Needy', 'Caring', 'Graceful', 'Unusual', 'Chunky', 'Draconian',
                'Dull', 'Glib', 'Probable', 'Horrible', 'Half', 'Accessible', 'Glossy', 'Nosy', 'Witty', 'Overjoyed',
                'Wicked', 'Proud', 'Left', 'Terrific', 'Lumpy', 'Harsh', 'Repulsive', 'Lopsided', 'Strange', 'Juicy']

    classes = ['Rogue', 'Warrior', 'Paladin', 'Wizard', 'Archer', 'Summoner']
    colors = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694]
    races = ['Human', 'Ogre', 'Elf', 'Dwarf', 'Gnome', 'Orc', 'Goblin', 'Gnoll', 'Minotaur', 'Pixie']

    # init empty skills list
    skills = []

    # open skills.txt file and append lines into 'skills' var
    with open('plugins/rpg/skills.txt') as file:
        for line in file:
            skills.append(line)

    # declare final vars
    final_name = "{} the {}".format(name, name_adj[randint(0, len(name_adj) - 1)])
    final_class = classes[randint(0, len(classes) - 1)]
    final_race = races[randint(0, len(races) - 1)]
    final_skills = skills[randint(0, len(skills) - 1)]

    icon = get_class_icon(final_class, colors)
    stats = calc_char_stats()

    return create_embed(final_name, final_class, final_race, final_skills, icon, stats)


def create_embed(name, fclass, race, skills, icon, stats):
    em = Embed(color=icon[0],
               title="RPG Character Generator")

    em.add_field(name='***{}***'.format(name),
                 value="Race: **{}**\nClass: **{}**\n\n{}".format(race, fclass, skills),
                 inline=True)

    em.add_field(name='Character Stats',
                 value="Strength: *{}*\nVitality: *{}*\nDexterity: *{}*\nIntellect: *{}*\nLuck: *{}*"
                 .format(stats[0],
                         stats[1],
                         stats[2],
                         stats[3],
                         stats[4]),
                 inline=True)

    em.set_footer(text=str(datetime.now().strftime('%b %d, %Y %H:%M')))

    em.set_thumbnail(url=icon[1])

    return em


def calc_char_stats():
    strength = 0
    vitality = 0
    dexterity = 0
    intellect = 0
    luck = 0

    for i in range(0, 100, 1):
        rand_num = randint(0, 5)
        if rand_num == 0:
            strength += 1
        elif rand_num == 1:
            vitality += 1
        elif rand_num == 2:
            dexterity += 1
        elif rand_num == 3:
            intellect += 1
        elif rand_num == 4:
            luck += 1

    return [strength, vitality, dexterity, intellect, luck]


def get_class_icon(final_class, colors):
    final_color = None
    url = None

    if final_class == 'Rogue':
        final_color = colors[0]
        url = "http://imgur.com/aw2T7kO.png"
    elif final_class == 'Warrior':
        final_color = colors[1]
        url = "http://imgur.com/oowXspQ.png"
    elif final_class == 'Paladin':
        final_color = colors[2]
        url = "http://imgur.com/YS6KmbJ.png"
    elif final_class == 'Wizard':
        final_color = colors[3]
        url = "http://imgur.com/zthtOzW.png"
    elif final_class == 'Archer':
        final_color = colors[4]
        url = "http://imgur.com/wwWjHO1.png"
    elif final_class == 'Summoner':
        final_color = colors[5]
        url = "http://imgur.com/4AEEg1l.png"

    return [final_color, url]



