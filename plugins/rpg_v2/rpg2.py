from random import randint, shuffle
from datetime import datetime
from dateutil.relativedelta import relativedelta
from discord import Embed

from edbot.plugins.rpg_v2 import vars

import mysql.connector
from mysql.connector import errorcode

import configparser


# method to setup the database config file used for connecting to the database
# via the db_connect method
def config(log):
    rpg_config = configparser.ConfigParser()
    # attempt to parse config.ini file
    try:
        rpg_config.read('plugins/rpg_v2/db_config.ini')
    except configparser.Error as err:
        log.error(str(err))

    # init database auth args
    database_auth = {
        'user': rpg_config.get('Database', 'user'),
        'password': rpg_config.get('Database', 'password'),
        'host': rpg_config.get('Database', 'host'),
        'database': rpg_config.get('Database', 'database'),
        'raise_on_warnings': rpg_config.getboolean('Database', 'raise_on_warnings')}

    return database_auth


# method to connect to the database using mysql.connector
def db_connect(log, auth):
    # attempt to connect to mysql database
    try:
        # create the mysql.connector cnx object
        sql_cnx = mysql.connector.connect(**auth)
        # return this object if no errors are thrown while creating
        return sql_cnx
    except mysql.connector.Error as con_err:
        # if access is denied to the database due to bad username/password
        if con_err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            log.error("bad username/password for db connection")
        # if the database specified in db_config.ini does not exist
        elif con_err.errno == errorcode.ER_BAD_DB_ERROR:
            log.error("database " + "'" + auth['database'] + "'" + " does not exist")
        # if any other error is thrown, log it to log file
        else:
            log.error(str(con_err))


# create a Discord Embed object to be sent to the Discord channel that the
# original message originated from
def embed_existing_character(cnx, author_id):
    cursor = cnx.cursor(buffered=True)

    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    for(User_ID, Server, Name, Level, XP, XP_To_LvlUp, Strength, Vitality, Intellect, Dexterity, Skill_1, Skill_2,
            Skill_3, Kills, Health, Class, Race, Name_Adj, Icon_URL, Potions, Potion_Timer) in row:

        em = Embed(color=get_class_color(Class),
                   title="{} {}".format(Name, Name_Adj))

        em.add_field(name="Player Info",
                     value="Race: {}\nClass: {}\nLevel: {}\nXP: {}\nXP To Level Up: {}\nKills: {}\n\nYour skills"
                           " include {}, {}, and {}.".format(Race, Class, Level, XP, XP_To_LvlUp, Kills, Skill_1,
                                                             Skill_2, Skill_3))

        em.add_field(name="Player Stats",
                     value="Health: {}/{}\nPotions: {}\n\nStrength: {}\nVitality: {}\nIntellect: "
                           "{}\nDexterity: {}".format(
                            Health, Vitality * 7, Potions, Strength, Vitality, Intellect, Dexterity
                            ))

        em.set_footer(text="{} --- {}".format(User_ID, str(datetime.now().strftime('%b %d, %Y %H:%M'))))

        em.set_thumbnail(url="{}".format(Icon_URL))

        return em


# simple method to determine the embed color variable based on the class given to the player
def get_class_color(player_class):
    # init color list, used when setting a Discord Embed color value
    # list imported from vars.py file
    colors = vars.colors

    # declare a final color initial var
    final_color = colors[6]

    # pick color of players embed based on the players Class variable from the database
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


# check if a character exists or not based on the messages author_id
def check_for_existing_char(cnx, author_id):
    cursor = cnx.cursor(buffered=True)

    # check if the message author already has a rpg character in the database
    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    # if the returned data inside the row variable is empty or blank '[]', return false because no character
    # exists for the specified author_id being passed
    if row == []:
        return False
    # otherwise, data is contained in row and return True
    else:
        return True


# generate a new player and send it to the database using the authors unique id as the primary key
# and key identifying feature when looking up players
def generate_new_character(cnx, author_id, author, author_server, log):
    # if the author does not have a nickname, use there username in discord instead
    print(author.nick)
    if author.nick is None:
        print(author.name)
        try:
            # attempt to grab authors username up to the first space in name
            player_name = author.name[:author.name.index(" ")]
        # if there is no space present, use the entire author name
        except AttributeError as aerr:
            log.error(str(aerr))
            player_name = author.name
        except ValueError as verr:
            log.error(str(verr))
            player_name = author.name

    # if the user does have a nickname, attempt to use the first word in there nickname
    else:
        try:
            # attempt to grab the authors nickname up to the first space (eg. 'John' Smith -> only John would be used
            player_name = author.nick[:author.nick.index(" ")]
        # if the username has no space in it, just use the authors entire nickname
        except AttributeError as aerr:
            log.error(str(aerr))
            player_name = author.nick
        except ValueError as verr:
            log.error(str(verr))
            player_name = author.nick

    cursor = cnx.cursor(buffered=True)

    # create a list of name adjectives to follow the users name
    adjs = vars.adjs

    # choose a random adjective to be used after the users name
    player_name_adj = 'the {}'.format(adjs[randint(0, len(adjs) - 1)])

    # set multiple vars that are used to generate a random character
    # classes, races, and skills are list objects containing info about the generated character
    classes = vars.classes
    races = vars.races
    skills = vars.skills

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
    player_health = vitality * 7

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
                   "Dexterity, Skill_1, Skill_2, Skill_3, Health, Class, Race, Icon_URL, Potion_Timer ) "
                   "VALUES "
                   "({},'{}','{}','{}',{},{},{},{},'{}','{}','{}',{},'{}','{}','{}',NOW() + INTERVAL 20 MINUTE )"
                   .format(author_id, author_server, player_name, player_name_adj, strength, vitality, intellect,
                           dexterity, player_skill_1, player_skill_2, player_skill_3, player_health, player_class,
                           player_race, player_icon_url))
    cnx.commit()


# create a random monster with values based on the players statistics
def fight_monster(cnx, author_id):
    monster_names = vars.monster_names

    # generate monsters attributes based on the authors current player stats/info in database
    cursor = cnx.cursor(buffered=True)

    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    for (User_ID, Server, Name, Level, XP, XP_To_LvlUp, Strength, Vitality, Intellect, Dexterity, Skill_1, Skill_2,
         Skill_3, Kills, Health, Class, Race, Name_Adj, Icon_URL, Potions, Potion_Timer) in row:

        # generate player stats for fight
        player_min_dmg = round(int(Strength * 0.6 + 12))
        player_max_dmg = round(int(Strength * 1.2 + 10))
        player_health = Health

        # generate enemy statistics
        enemy_name = monster_names[randint(0, len(monster_names) - 1)]

        rand = randint(0, 1)
        if rand == 0:
            enemy_level = Level + 2
        else:
            enemy_level = Level + 1

        enemy_min_dmg = round(int(Strength * 0.2 + 3))
        enemy_max_dmg = round(int(Strength * 0.5 + 5))

        enemy_health = int(Vitality * 3) + 5

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

            return "Oh no... {} {} has been {} by a Level {} {} in battle.".format(
                Name, Name_Adj, vars.death_adjs[randint(0, len(vars.death_adjs) - 1)], enemy_level, enemy_name)

    # the enemy has been successfully defeated, add new stats and calculate database values
    player_kills = Kills + 1
    player_xp = XP + enemy_xp
    player_max_health = Vitality * 7
    cursor.execute("UPDATE User SET XP = {}, Kills = {}, Health = {} WHERE User_ID = {}".format
                   (player_xp, player_kills, player_health, author_id))
    cnx.commit()

    cursor.execute("SELECT * FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    for (User_ID, Server, Name, Level, XP, XP_To_LvlUp, Strength, Vitality, Intellect, Dexterity, Skill_1, Skill_2,
         Skill_3, Kills, Health, Class, Race, Name_Adj, Icon_URL, Potions, Potion_Timer) in row:

        if XP >= XP_To_LvlUp:
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
                           .format(Level + 1, int(XP_To_LvlUp * 1.8), skill_to_add, amount + 1, int(Vitality * 7),
                                   author_id))
            cnx.commit()
            return "{} {} has defeated a Level {} {} successfully and has levelled up, Their HP has been " \
                   "refilled to {}/{} and they gained one point in {}!".format(Name, Name_Adj, enemy_level, enemy_name,
                                                                               Vitality * 7, player_max_health,
                                                                               skill_to_add)

    return "{} {} has defeated a Level {} {} successfully with {}/{} HP remaining, gaining {} XP points. "\
        .format(Name, Name_Adj, enemy_level, enemy_name, player_health, player_max_health, enemy_xp)


# check if a player has a potion available, and consume this potion, healing a random amount of hp
def use_potion(cnx, author_id):
    # check if the player has a potion available to use
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT Name, Name_Adj, Health, Vitality, Potions FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    for (Name, Name_Adj, Health, Vitality, Potions) in row:
        # if the player has no potions at all, let them know they can not use this command
        if Potions == 0:
            return "{} {} does not have any potions remaining! Try typing ed.rpg.freepotion to see if you're eligible" \
                   " for a free potion!".format(Name, Name_Adj)

        # if the players health is already at max health
        if Health == Vitality * 7:
            return "{} {}'s health is already full! {}/{}".format(Name, Name_Adj, Health, Vitality * 7)

        # if the player has more than 0 potions, in the database, calculate the amounts that will be healed
        if Potions > 0:
            health_to_heal = round((int(Vitality * 7) * 0.3)) + randint(10, 25)
            max_health = Vitality * 7

            # add new heal amount to previous amount of total health of player
            new_health = Health + health_to_heal
            # if the amount that the player is going to be healed for is greater or equal to the players
            # max health, heal the player back to full hp, but don't let their hp go over max
            if new_health >= Vitality * 7:
                cursor.execute("UPDATE User SET Health = {}, Potions = {} "
                               "WHERE User_ID = {}".format(Vitality * 7, Potions - 1, author_id))
                cnx.commit()
                return "{} {} has consumed a health potion and restored their health to max!".format(Name, Name_Adj)
            # otherwise the player can be healed properly and given the full amount of healing
            else:
                cursor.execute("UPDATE User SET Health = {}, Potions = {} "
                               "WHERE User_ID = {}".format(new_health, Potions - 1, author_id))
                cnx.commit()
                return "{} {} has consumed a health potion and restored {} health points, their hp is now {}/{}!".\
                    format(Name, Name_Adj, health_to_heal, new_health, max_health)
        # if the player has no potions available to use
        else:
            return "{} {} has no potions available to consume!".format(Name, Name_Adj)


# attempt to give a player a free potion (available every 20 minutes)
def get_free_potion(cnx, author_id):
    # check if the players potion timer is expired and ready to be redeemed for 1 potion
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT Potion_Timer, Potions, Name, Name_Adj FROM User WHERE User_ID = {}".format(author_id))
    row = cursor.fetchall()

    for (Potion_Timer, Potions, Name, Name_Adj) in row:
        # get the timestamp in UTC format
        now = datetime.utcnow()

        # if UTC timestamp for now is greater than the Potion_Timer timestamp from the database, set the timer for the
        # next potion to 20 minutes from utcnow() and take away one potion from the player
        if now > Potion_Timer:
            cursor.execute("UPDATE User SET Potion_Timer = NOW() + INTERVAL 20 MINUTE , Potions = {}"
                           " WHERE User_ID = {}".format(Potions + 1, author_id))
            cnx.commit()
            return "{} {} has claimed a free health potion! They currently have {} potions".format(Name, Name_Adj,
                                                                                                   Potions + 1)
        # otherwise, the time until the player can claim a health potion has not passed yet, display the time remaining
        # to the message author
        else:
            difference = relativedelta(Potion_Timer, now)
            return "{} {} isn't ready to claim a potion for another {} minutes and {} seconds.".format(
                Name, Name_Adj, difference.minutes, difference.seconds
            )


# generate a Discord Embed object containing the top 5 players currently living inside of the database
def gen_leader_embeds(cnx):
    # init var to hold the pixel podium image url
    icon_url = "http://i.imgur.com/VaGOL2B.png"

    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT * FROM ( SELECT * FROM User ORDER by Level ASC LIMIT 5"
                   ") User ORDER by User.Level DESC")
    row = cursor.fetchall()

    em = Embed(color=0xFFDC3F,
               title="Current Leaderboards :trophy:")

    # init int starting at 0 to hold the amount of users iterated over to display top 5 numbers before each name
    current_row = 0
    for (User_ID, Server, Name, Level, XP, XP_To_LvlUp, Strength, Vitality, Intellect, Dexterity, Skill_1, Skill_2,
         Skill_3, Kills, Health, Class, Race, Name_Adj, Icon_URL, Potions, Potion_Timer) in row:

        current_row += 1
        em.add_field(name="{}. {} {}".format(current_row, Name, Name_Adj),
                     value="\nLevel: {}\nKills: {}\nCurrent XP: {}\nClass: {}\nRace: {}\nServer: {}".format(
                         Level, Kills, XP, Class, Race, Server
                     ), inline=True)

    # set footer containing timestamp of date in a string
    em.set_footer(text="{}".format(str(datetime.now().strftime('%b %d, %Y %H:%M'))))

    # set the Embed thumbnail to the icon_url set above containing the pixel podium image
    em.set_thumbnail(url=icon_url)

    return em


# generate a Discord Embed object containing the top 5 players that have perished in the database
def gen_fallen_heroes_embed(cnx):
    # init a var to hold the fallen heroes image url
    icon_url = "http://i.imgur.com/Qu9szxY.png"

    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT Name, Name_Adj, Level, Kills, XP, Class, Race, Server, Time_Defeated "
                   "FROM ( SELECT * FROM Defeated_User ORDER by Level DESC LIMIT 5"
                   ") Defeated_User ORDER by Defeated_User.Level DESC")
    row = cursor.fetchall()

    em = Embed(color=0xFF3434,
               title="Vanquished Heroes")

    # init int starting at 0 to hold the amount of users iterated over to display top 5 numbers before each name
    current_row = 0
    for (Name, Name_Adj, Level, Kills, XP, Class, Race, Server, Time_Defeated) in row:
        time = datetime.strptime(str(Time_Defeated), "%Y-%m-%d %H:%M:%S").strftime('%b %d, %Y %H:%M')

        current_row += 1
        em.add_field(name="{}. {} {}".format(current_row, Name, Name_Adj),
                     value="\nLevel: {}\nKills: {}\nCurrent XP: {}\nClass: {}\nRace: {}\nServer: {}"
                           "\nTime Defeated: {}".format(Level, Kills, XP, Class, Race, Server, time),
                     inline=True)

    # set footer containing timestamp of date in a string
    em.set_footer(text="{}".format(str(datetime.now().strftime('%b %d, %Y %H:%M'))))

    # set the Embed thumbnail to the icon_url set above containing the skull pixel image
    em.set_thumbnail(url=icon_url)
    return em


def get_target_id(message):
    # extract the user id from the message content provided
    target_id = message.content[message.content.index("<"):]
    target_id_final = ''

    # finally, for each item in target_id var, check if it is an int, if it is, add that item to the final
    # target_id var
    for x in target_id:
        try:
            int(x)
            target_id_final += x
        # skip this item if it can not be cast into an int type
        except ValueError:
            continue

    return target_id_final


def fight_player(cnx, author_id, message):
    # extract the user id from the message content provided
    target_id = message.content[message.content.index("<"):]
    target_id_final = ''

    # finally, for each item in target_id var, check if it is an int, if it is, add that item to the final
    # target_id var
    for x in target_id:
        try:
            int(x)
            target_id_final += x
        # skip this item if it can not be cast into an int type
        except ValueError:
            continue

    # check if a target with this user id exists before continuing
    exists = check_for_existing_char(cnx, target_id_final)
    if exists is False:
        return "I can't find a player that exists with that username! Do they have a character?"

    # setup author player stats
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT User_ID, Name, Name_Adj, Level, Strength, Vitality, Intellect, Dexterity"
                   " FROM User WHERE User_ID = {}".format(author_id))

    player_stats = cursor.fetchall()

    cursor.execute("SELECT User_ID, Name, Name_Adj, Level, Strength, Vitality, Intellect, "
                   "Dexterity FROM User WHERE User_ID = {}".format(target_id_final))

    target_player_stats = cursor.fetchall()

    # set some specific vars for fight that aren't in database normally
    player_name = player_stats[0][1]
    player_name_adj = player_stats[0][2]
    player_health = player_stats[0][5] * 7
    player_min_dmg = round(int(player_stats[0][4] * 0.4 + randint(4, 10)))
    player_max_dmg = round(int(player_stats[0][4] * 1.1 + randint(8, 16)))

    target_name = target_player_stats[0][1]
    target_name_adj = target_player_stats[0][2]
    target_health = target_player_stats[0][5] * 7
    target_min_dmg = round(int(target_player_stats[0][4] * 0.4 + randint(4, 10)))
    target_max_dmg = round(int(target_player_stats[0][4] * 1.1 + randint(8, 16)))

    # create an embed and give it a title detailing who is fighting who
    em = Embed(color=0x00FF00,
               title="{} {} ({}/{}) VS. {} {} ({}/{})".format(
                   player_name, player_name_adj, player_health, player_health, target_name, target_name_adj,
                   target_health, target_health))

    # set etc details for embed object
    em.set_footer(text="{}".format(str(datetime.now().strftime('%b %d, %Y %H:%M'))))
    em.set_thumbnail(url="http://i.imgur.com/yPNEy2o.png")

    # start the battle and set the first turn to 1
    current_turn = 0

    # while the players health is greater than or equal to 0, fight will continue infinitely
    while player_health >= 0:
        current_turn += 1

        # calculate both players damage values for this current turn
        player_turn_damage = randint(player_min_dmg, player_max_dmg)
        target_turn_damage = randint(target_min_dmg, target_max_dmg)

        # calculate the new health values for both players
        player_health -= target_turn_damage
        target_health -= player_turn_damage

        # if the target is now dead (<= 0 HP)
        if target_health <= 0:
            em.add_field(name="Winner!".format(current_turn),
                         value="{} has defeated {}!".format(player_name, target_name))
            return em

        # generic damage embed field showing both damage numbers dealt to each player
        em.add_field(name="Turn {}".format(current_turn),
                     value="{} hit {} for -{} damage!\n{} hit {} for -{} damage!".format(
                         player_name, target_name, player_turn_damage, target_name, player_name, target_turn_damage))

    # if the player is now dead (<= 0 HP) the while loop has been broken, add new field and return!
    em.add_field(name="Winner!".format(current_turn),
                 value="{} has defeated {}!".format(target_name, player_name))
    return em









