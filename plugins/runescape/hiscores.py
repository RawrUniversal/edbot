import requests
import json

from discord import Embed


def get_username(message):
    space_index = message.index(" ")
    uname = message[space_index + 1:]
    return uname


def get_hiscores(username):
    response = requests.get("https://www.tip.it/runescape/json/hiscore_user?rsn={}&old_stats=1".format(username))
    data = json.loads(response.content.decode("utf-8"))
    return data


def gen_embed(stats):
    em = Embed(color=0x00F4FF,
               title="Hi-Scores for {}".format(stats['rsn']))

    em.add_field(name='Stats ({}/2277) - {}'.format(
        stats['stats']['overall']['level'], format(stats['stats']['overall']['exp'], ",d")),

                 value="Attack: {}/99\nStrength: {}/99\nDefence: {}/99\nConstitution: {}/99\n"
                       "Range:{}/99\nMagic: {}/99\nPrayer: {}/99\nAgility: {}/99\nMining: {}/99\n"
                       "Herblore: {}/99\nSmithing: {}/99\nFishing: {}/99\nThieving: {}/99\n"
                       "Cooking: {}/99\nCrafting: {}/99\nFiremaking: {}/99\nFletching: {}/99\n"
                       "Woodcutting: {}/99\nRunecrafting: {}/99\nSlayer: {}/99\nFarming: {}/99\n"
                       "Construction: {}/99\nHunter: {}/99".format(
                     stats['stats']['attack']['level'], stats['stats']['strength']['level'],
                     stats['stats']['defence']['level'], stats['stats']['constitution']['level'],
                     stats['stats']['range']['level'], stats['stats']['magic']['level'],
                     stats['stats']['prayer']['level'], stats['stats']['agility']['level'],
                     stats['stats']['mining']['level'], stats['stats']['herblore']['level'],
                     stats['stats']['smithing']['level'], stats['stats']['fishing']['level'],
                     stats['stats']['thieving']['level'], stats['stats']['cooking']['level'],
                     stats['stats']['crafting']['level'], stats['stats']['firemaking']['level'],
                     stats['stats']['fletching']['level'], stats['stats']['woodcutting']['level'],
                     stats['stats']['runecrafting']['level'], stats['stats']['slayer']['level'],
                     stats['stats']['farming']['level'], stats['stats']['construction']['level'],
                     stats['stats']['hunter']['level']
                 ))

    return em
