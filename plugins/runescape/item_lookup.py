import requests
import json
from datetime import datetime
from random import randint

from discord import Embed

# set base url of the osrs item db api url
BASE_URL = "http://services.runescape.com/m=itemdb_oldschool"


def check_string(item):
    item = item.lower()  # set all characters of item string to lowercase
    item = item.capitalize()  # capitalize the first letter of the string
    return item


def check_item(message):
    space_index = message.index(" ")  # search the message for the index of first space in string
    item = message[space_index + 1:]  # grab all text starting at first letter after space
    print(item)

    if item.capitalize() == 'Random':
        with open('plugins/runescape/item_id.json') as item_ids:
            jdata = json.load(item_ids)
            item = jdata[randint(0, len(jdata))]['id']
            return item

    if item.isdigit():
        with open('plugins/runescape/item_id.json') as item_ids:
            jdata = json.load(item_ids)

        for i in jdata:
            if i['id'] == int(item):
                return item

    else:
        item = check_string(item)
        with open('plugins/runescape/item_id.json') as item_ids:
            jdata = json.load(item_ids)

        for i in jdata:
            if item == i['name']:
                return i['id']

    item = False
    return item


def request_item_json(item):
    end_point = "/api/catalogue/detail.json?item={}".format(str(item))
    response = requests.get(BASE_URL + end_point)

    item_info = json.loads(response.content.decode("utf-8"))
    return item_info


def generate_embed(item_json):
    print(item_json)
    em = Embed(color=0x00F4FF,
               title='{} ({}) | {}'.format(
                   item_json["item"]["name"].title(),
                   item_json["item"]["id"],
                   item_json["item"]["description"].title()))

    em.add_field(name="Current Price Guide: **{}**".format(item_json['item']['current']['price']),
                 value="Today's Change: **{}**\n30 Day: **{}**\n90 Day: **{}**\n180 Day: **{}**"
                       "\n\nMembers Only?  **{}**\n".format(
                    item_json['item']['today']['price'], item_json['item']['day30']['change'],
                    item_json['item']['day90']['change'], item_json['item']['day180']['change'],
                    item_json['item']['members'].capitalize()))

    em.set_thumbnail(url=item_json['item']['icon_large'])

    em.set_footer(text=str(datetime.now()))

    return em

