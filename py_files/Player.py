import json
import math
import discord
from discord import Embed
import Spells


# 143866534866059264


async def create_player_file(discordID):
    player_info = {
        discordID: {
            'inCombat': False,
            'level': 1,
            'exp': 0,
            'total exp': 0,
            'health': 100,
            'max health': 100,
            'dokens': 0,
            'coin': 0,
            'mana_frags': 0,
            'magic_modifier': 0,
            'range_modifier': 0,
            'melee_modifier': 0,
            'dodge_modifier': 0,
            'presist_modifier': 0,
            'mresist_modifier': 0,
            'helm': 0,
            'chest': 0,
            'legs': 0,
            'boots': 0,
            'weapon': 0,
            'summon': 0,
            'pet': 0,
            'psbag': [

            ],
            'ebag': [

            ],
            'ibag': {
                0: 1
            },
            'cbag': {

            },
            'spells': {
                0: 0
            }
        }
    }

    with open(f'./player_files/{discordID}.json', 'w') as fileOut:
        json.dump(player_info, fileOut, indent=2)


def save_player(discordID, playerFile):
    with open(f'./player_files/{discordID}.json', 'w') as fileOut:
        json.dump(playerFile, fileOut, indent=2)


def load_player(discordID):
    with open(f'./player_files/{discordID}.json', 'r') as fileIn:
        return json.load(fileIn)


def get_player_stat(discordID, statName):
    playerFile = load_player(discordID)

    return playerFile[f'{discordID}'][statName]


def get_player_dmg_mod(discordID, dmgType):
    playerFile = load_player(discordID)

    if dmgType == 'magic':
        return 1 + playerFile[f'{discordID}']['magic_modifier'] * 0.02
    if dmgType == 'range':
        return 1 + playerFile[f'{discordID}']['range_modifier'] * 0.02
    if dmgType == 'melee':
        return 1 + playerFile[f'{discordID}']['melee_modifier'] * 0.02


def get_player_equip(discordID, equipName):
    playerFile = load_player(discordID)

    if playerFile[f'{discordID}'][equipName] == '0':
        return 'Nothing'
    else:
        pass


def get_player_summon(discordID, sumName):
    playerFile = load_player(discordID)

    if playerFile[f'{discordID}'][sumName] == 0:
        return 'No summon found!'
    else:
        pass


def get_player_pet(discordID, petName):
    playerFile = load_player(discordID)

    if playerFile[f'{discordID}'][petName] == 0:
        return 'No pet found!'
    else:
        pass


def get_player_combat_boolean(discordID):
    playerFile = load_player(discordID)

    return playerFile[f'{discordID}']['inCombat']


def get_player_combat_status(discordID):
    playerFile = load_player(discordID)

    if playerFile[f'{discordID}']['inCombat']:
        return 'In Combat'
    else:
        return 'In Town'


def get_max_player_exp(discordID):
    playerFile = load_player(discordID)

    playerLevel = playerFile[f'{discordID}']['level']

    return next_exp_cap_calc(playerLevel)


def get_player_spell_dic(discordID):
    playerFile = load_player(discordID)
    return playerFile[f'{discordID}']['spells']


def next_exp_cap_calc(playerLevel):
    if playerLevel < 15:
        return int(math.pow((playerLevel + 1), 3) * (((playerLevel + 2) + 24)/30))
    elif 15 <= playerLevel <= 50:
        return int(math.pow((playerLevel + 1), 3) * ((playerLevel + 15) / 30))
    elif 50 < playerLevel <= 100:
        return int(math.pow((playerLevel + 1), 3) * (((playerLevel / 2) + 40) / 30))


def exp_cap_calc(playerLevel):
    if playerLevel < 15:
        return int(math.pow((playerLevel + 1), 3) * (((playerLevel + 2) + 24)/30))
    elif 15 <= playerLevel <= 50:
        return int(math.pow((playerLevel + 1), 3) * ((playerLevel + 15) / 30))
    elif 50 < playerLevel <= 100:
        return int(math.pow((playerLevel + 1), 3) * (((playerLevel / 2) + 40) / 30))


async def switch_player_status(discordID):
    # Opening file to read
    playerFile = load_player(discordID)

    # Changing the file data
    if playerFile[f'{discordID}']['inCombat']:
        playerFile[f'{discordID}']['inCombat'] = False
    else:
        playerFile[f'{discordID}']['inCombat'] = True

    # Saving the new file data
    save_player(discordID, playerFile)
