from random import randint
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


def check_for_existing_char(cnx, author_id):
    cursor = cnx.cursor(buffered=True)

    # check if the message author already has a rpg character in the database
    cursor.execute("SELECT * FROM User WHERE User_ID = '%'".format(author_id))
    row = cursor.fetchall()

    # debug
    print(row)

    if row == []:
        return False
    else:
        return True
