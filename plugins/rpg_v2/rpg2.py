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


def embed_existing_character(cnx, author_id):
    cursor = cnx.cursor(buffered=True)

    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    for(User_ID, Server, Name, Level, XP, XP_To_LvlUp, Strength, Vitality, Intellect, Dexterity, Skill_1, Skill_2,
            Skill_3, Kills, Health, Class, Race, Name_Adj, Icon_URL) in row:

        em = Embed(color=get_class_color(Class),
                   title="{} {}".format(Name, Name_Adj))

        em.add_field(name="Player Info",
                     value="Race: {}\nClass: {}\nLevel: {}\nXP: {}\nXP To Level Up: {}\nKills: {}\n\nYour skills"
                           " include {}, {}, and {}.".format(Race, Class, Level, XP, XP_To_LvlUp, Kills, Skill_1,
                                                             Skill_2, Skill_3))

        em.add_field(name="Player Stats",
                     value="Health: {}\nStrength: {}\nVitality: {}\nIntellect: {}\nDexterity: {}".format(
                         Health, Strength, Vitality, Intellect, Dexterity
                     ))

        em.set_footer(text="{} --- {}".format(User_ID, str(datetime.now().strftime('%b %d, %Y %H:%M'))))

        em.set_thumbnail(url="{}".format(Icon_URL))

        return em


def get_class_color(player_class):
    # init color list
    colors = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694]

    # pick color of players embed based on their class
    if player_class == 'Rogue':
        final_color = colors[0]
    elif player_class == 'Warrior':
        final_color = colors[1]
    elif player_class == 'Paladin':
        final_color = colors[2]
    elif player_class == 'Wizard':
        final_color = colors[3]
    elif player_class == 'Archer':
        final_color = colors[4]
    elif player_class == 'Summoner':
        final_color = colors[5]

    return final_color


def check_for_existing_char(cnx, author_id):
    cursor = cnx.cursor(buffered=True)

    # check if the message author already has a rpg character in the database
    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    if row == []:
        return False
    else:
        return True


def generate_new_character(cnx, author_id, author, author_server):
    # if the author does not have a nickname, use there username in discord instead
    if author.nick == "None":
        player_name = author.name
    # if the user does have a nickname, attempt to use the first word in there nickname
    else:
        try:
            player_name = author.name[:author.name.index(" ")]
        # if the username has no space in it, just use the authors entire nickname
        except AttributeError as aerr:
            print("Name has no space in it, attempting to make players name just author_name")
            player_name = author.nick
        except ValueError as verr:
            print("Name has no space in it, attempting to make players name just author_name")
            player_name = author.nick

    cursor = cnx.cursor(buffered=True)

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


def fight_monster(cnx, author_id):
    # todo make more monsters
    monster_names = ['Bat', 'Archer', 'Ogre', 'Barbarian', 'Necromancer']

    # generate monsters attributes based on the authors current player stats/info in database
    cursor = cnx.cursor(buffered=True)

    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    for (User_ID, Server, Name, Level, XP, XP_To_LvlUp, Strength, Vitality, Intellect, Dexterity, Skill_1, Skill_2,
         Skill_3, Kills, Health, Class, Race, Name_Adj, Icon_URL) in row:

        # generate player stats for fight
        player_min_dmg = int(Strength * 0.6 + 12)
        player_max_dmg = int(Strength * 1.2 + 10)
        player_health = Health

        # generate enemy statistics
        enemy_name = monster_names[randint(0, len(monster_names) - 1)]
        rand = randint(0, 1)
        enemy_level = Level
        if rand == 0:
            enemy_level = Level + 2
        else:
            enemy_level = Level + 1

        enemy_min_dmg = int(Strength * 0.2 + 3)
        enemy_max_dmg = int(Strength * 0.5 + 5)

        enemy_health = int(Health * 0.7)

        enemy_xp = Level * randint(10, 15)

    while enemy_health > 0:
        enemy_health -= randint(player_min_dmg, player_max_dmg)
        player_health -= randint(enemy_min_dmg, enemy_max_dmg)
        if player_health <= 0:
            # player is dead, add data about this character to the defeated user table in database
            cursor.execute("INSERT INTO Defeated_User ( User_ID, Server, Name, Name_Adj, Level, XP, Strength, Vitality,"
                           " Intellect, Dexterity, Skill_1, Skill_2, Skill_3, Kills, Health, Class, Race ) "
                           "VALUES "
                           "({},'{}','{}','{}',{},{},{},{},{},{},'{}','{}','{}',{},{},'{}','{}')".format(
                                User_ID, Server, Name, Name_Adj, Level, XP, Strength, Vitality, Intellect, Dexterity,
                                Skill_1, Skill_2, Skill_3, Kills, Vitality * 5, Class, Race))
            cnx.commit()

            # delete the character that is now defeated from the User table in database
            cursor.execute("DELETE FROM User WHERE User_ID = {}".format(User_ID))
            cnx.commit()

            return "Oh no... {} {} has been defeated permanently by a Level {} {} in battle.".format(
                Name, Name_Adj, enemy_level, enemy_name
            )

    # the enemy has been successfully defeated, add new stats and calculate database values

    player_kills = Kills + 1
    player_xp = XP + enemy_xp
    cursor.execute("UPDATE User SET XP = {}, Kills = {}, Health = {} WHERE User_ID = {}".format
                   (player_xp, player_kills, player_health, author_id))
    cnx.commit()

    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    for (User_ID, Server, Name, Level, XP, XP_To_LvlUp, Strength, Vitality, Intellect, Dexterity, Skill_1, Skill_2,
         Skill_3, Kills, Health, Class, Race, Name_Adj, Icon_URL) in row:

        if XP > XP_To_LvlUp:
            # choose a skill to add one point to
            rand = randint(0, 4)
            if rand == 0:
                skill_to_add = "Strength"
                amount = Strength
            elif rand == 1:
                skill_to_add = "Dexterity"
                amount = Dexterity
            elif rand == 2:
                skill_to_add = "Vitality"
                amount = Vitality
            else:
                skill_to_add = "Intellect"
                amount = Intellect

            # player has levelled up
            cursor.execute("UPDATE User SET Level = {}, XP_To_LvlUp = {}, {} = {}, Health = {} WHERE User_ID = {}"
                           .format(Level + 1, int(XP_To_LvlUp * 1.5), skill_to_add, amount + 1, int(Vitality * 5),
                                   author_id))
            cnx.commit()
            return "{} {} has defeated a Level {} {} successfully and has levelled up, Their HP has been refilled" \
                   " and they gained one point in {}!".format(Name, Name_Adj, enemy_level, enemy_name, skill_to_add)

    return "{} {} has defeated a Level {} {} successfully with {} HP remaining, gaining {} XP points."\
        .format(Name, Name_Adj, enemy_level, enemy_name, player_health, enemy_xp)
















