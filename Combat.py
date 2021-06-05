import json
import Enemies
import os


async def combat_setup(discordID, channelID, location):
    if location == 'forest' or location == 'woodlands':
        enemyID = Enemies.rand_forest_enemy()
        enemy = Enemies.get_enemy(enemyID)

    elif location == 'mountains' or location == 'mountain':
        enemyID = Enemies.rand_mountain_enemy()
        enemy = Enemies.get_enemy(enemyID)

    elif location == 'plains' or location == 'grassland':
        enemyID = Enemies.rand_plains_enemy()
        enemy = Enemies.get_enemy(enemyID)

    combat_file = {
        'channel_id': channelID,
        'players': discordID,
        'player_encounters': 1,
        'enemy': {
            'id': enemyID,
            'name': enemy.get_name(),
            'level': enemy.get_level(),
            'health': enemy.get_health(),
            'max_health': enemy.get_health(),
        }
    }

    with open(f'./combat_files/{discordID}_combat.json', 'w') as fileOut:
        json.dump(combat_file, fileOut, indent=2)


async def delete_combat_file(discordID):
    os.remove(f'./combat_files/{discordID}_combat.json')


def save_combat_file(discordID, combat_file):
    with open(f'./combat_files/{discordID}_combat.json', 'w') as fileOut:
        json.dump(combat_file, fileOut, indent=2)


def load_combat_file(discordID):
    with open(f'./combat_files/{discordID}_combat.json', 'r') as fileIn:
        return json.load(fileIn)


def get_enemy_id(discordID):
    combatFile = load_combat_file(discordID)

    return combatFile['enemy']['id']


def get_enemy_name(discordID):
    combatFile = load_combat_file(discordID)

    return combatFile['enemy']['name']


def get_enemy_level(discordID):
    combatFile = load_combat_file(discordID)

    return combatFile['enemy']['level']


def get_enemy_health(discordID):
    combatFile = load_combat_file(discordID)

    return combatFile['enemy']['health']


def get_enemy_max_health(discordID):
    combatFile = load_combat_file(discordID)

    return combatFile['enemy']['max_health']