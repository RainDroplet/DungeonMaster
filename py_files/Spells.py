import Player
import math


class Spells:
    def __init__(self, name, level, desc, baseDmg, cooldown):
        self.name = name
        self.level = level
        self.desc = desc
        self.baseDmg = baseDmg
        self.cooldown = cooldown

    def get_name(self):
        return self.name

    def get_level(self):
        return self.name

    def get_desc(self):
        return self.desc

    def get_base_dmg(self):
        return self.baseDmg

    def get_cooldown(self):
        return self.cooldown


spellIndex = {
    0: Spells(name='Heavy Punch', level=1, desc='You clench your fist to hit harder.', baseDmg=1, cooldown=2)
}


def get_spell(key):
    try:
        return spellIndex[key]
    except IndexError:
        pass


def get_dmg(discordID, spellKey, dmgType):
    dmgCalc = math.sqrt(
        ((spellIndex[spellKey].get_base_dmg() / 3) * Player.get_player_stat(discordID, 'level')) *
        Player.get_player_dmg_mod(discordID, dmgType))
    return dmgCalc


if __name__ == '__main__':
    spell = get_spell(0).get_name()
    print(spell)
