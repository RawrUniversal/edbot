from random import randint, shuffle
from datetime import datetime
from discord import Embed

import mysql.connector
from mysql.connector import errorcode

import configparser


def config(log):
    Config = configparser.ConfigParser()
    # attempt to parse config.ini file
    try:
        Config.read('plugins/rpg_v2/db_config.ini')
    except configparser.Error as err:
        log.error(str(err))

    # init database auth args
    database_auth = {
        'user': Config.get('Database', 'user'),
        'password': Config.get('Database', 'password'),
        'host': Config.get('Database', 'host'),
        'database': Config.get('Database', 'database'),
        'raise_on_warnings': Config.getboolean('Database', 'raise_on_warnings')}

    return database_auth


def db_connect(log, auth):
    # attempt to connect to mysql database
    try:
        sql_cnx = mysql.connector.connect(**auth)
    except mysql.connector.Error as con_err:
        if con_err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            log.error("bad username/password for db connection")
        elif con_err.errno == errorcode.ER_BAD_DB_ERROR:
            log.error("database " + "'" + auth['database'] + "'" + " does not exist")
        else:
            log.error(str(con_err))

    # return cnx object
    return sql_cnx


# def embed_existing_character(cnx, author_id):
    


def check_for_existing_char(cnx, author_id):
    cursor = cnx.cursor(buffered=True)

    # check if the message author already has a rpg character in the database
    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    # debug
    print(row)

    if row == []:
        return False
    else:
        return True


def generate_new_character(cnx, author_id, author_name, author_server):
    cursor = cnx.cursor(buffered=True)

    # begin looking for users first part of a name (eg. Bob Smith -> Bob)
    # if a users name is one word (eg. John), use just the name John
    print(author_name)
    if author_name.index(" ") is not None:
        player_name = author_name[:author_name.index(" ")]
    else:
        player_name = author_name

    # create a list of name adjectives to follow the users name
    adjs = ['High-pitched', 'General', 'Deadpan', 'Hushed', 'Third',  'Big',  'Hulking', 'Screeching', 'Moaning',
            'Thankful', 'Typical', 'Conscious', 'Succinct', 'Grumpy', 'Waggish', 'Little', 'Telling', 'Obtainable',
            'Coherent',  'Red',  'Marked', 'Steady', 'Squeamish', 'Famous', 'Tedious', 'Truthful', 'Sincere',
            'Abusive', 'Mature', 'Short', 'Silent', 'Needy', 'Caring', 'Graceful', 'Unusual', 'Chunky', 'Draconian',
            'Dull', 'Glib', 'Probable', 'Horrible', 'Half', 'Accessible', 'Glossy', 'Nosy', 'Witty', 'Overjoyed',
            'Wicked', 'Proud', 'Left', 'Terrific', 'Lumpy', 'Harsh', 'Repulsive', 'Lopsided', 'Strange', 'Juicy']

    # choose a random adjective to be used after the users name
    player_name_adj = 'the {}'.format(adjs[randint(0, len(adjs) - 1)])

    classes = ['Rogue', 'Warrior', 'Paladin', 'Wizard', 'Archer', 'Summoner']
    races = ['Human', 'Ogre', 'Elf', 'Dwarf', 'Gnome', 'Orc', 'Goblin', 'Gnoll', 'Minotaur', 'Pixie']

    colors = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694]

    skills = ['hiding', 'gardening', 'horseback riding', 'lip reading', 'inventing', 'marksmanship', 'drawing',
              'playing the violin', 'programming', 'heavy lifting', 'foraging', 'tracking', 'paper cutting',
              'metalworking', 'playing the drums', 'voice impressions', 'baking', 'yo-yo tricks', 'posing',
              'map-making', 'wrapping presents', 'knitting', 'public speaking', 'wood carving', 'boxing']

    # begin creating final vars for db
    player_class = classes[randint(0, len(classes) - 1)]
    player_race = races[randint(0, len(races) - 1)]

    # shuffle skills array and choose first three indexes from now randomized array
    shuffle(skills)
    player_skill_1 = skills[0]
    player_skill_2 = skills[1]
    player_skill_3 = skills[2]

    strength, vitality, dexterity, intellect = 0, 0, 0, 0

    # randomly distribute skills points to the character
    for i in range(0, 100, 1):
        rand_num = randint(0, 4)
        if rand_num == 0:
            strength += 1
        elif rand_num == 1:
            vitality += 1
        elif rand_num == 2:
            dexterity += 1
        elif rand_num == 3:
            intellect += 1

    # calculate base health for generated character
    player_health = vitality * 5

    # init empty color and icon vars
    player_color = None
    player_icon_url = None

    if player_class == 'Rogue':
        player_icon_url = "http://imgur.com/aw2T7kO.png"
    elif player_class == 'Warrior':
        player_icon_url = "http://imgur.com/oowXspQ.png"
    elif player_class == 'Paladin':
        player_icon_url = "http://imgur.com/YS6KmbJ.png"
    elif player_class == 'Wizard':
        player_icon_url = "http://imgur.com/zthtOzW.png"
    elif player_class == 'Archer':
        player_icon_url = "http://imgur.com/wwWjHO1.png"
    else:
        player_icon_url = "http://imgur.com/4AEEg1l.png"

    # sent these values to the database as a new entry
    cursor.execute("INSERT INTO User ( User_ID, Server, Name, Name_Adj, Strength, Vitality, Intellect, "
                   "Dexterity, Skill_1, Skill_2, Skill_3, Health, Class, Race, Icon_URL ) "
                   "VALUES "
                   "({},'{}','{}','{}',{},{},{},{},'{}','{}','{}',{},'{}','{}','{}')"
                   .format(author_id, author_server, player_name, player_name_adj, strength, vitality, intellect,
                           dexterity, player_skill_1, player_skill_2, player_skill_3, player_health, player_class,
                           player_race, player_icon_url))
    cnx.commit()
