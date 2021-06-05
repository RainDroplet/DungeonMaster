import json
import random


class Enemies:
    def __init__(self, name, level, health, damage, magic_resistance, physical_resistance, rewards,
                 experience, triggers):
        self.name = name
        self.level = level
        self.health = health
        self.damage = damage
        self.magic_resistance = magic_resistance
        self.physical_resistance = physical_resistance
        self.rewards = rewards
        self.experience = experience
        self.triggers = triggers

    def get_name(self):
        return self.name

    def get_level(self):
        return self.level

    def get_health(self):
        return self.health

    def get_damage(self):
        return self.damage

    def get_magic_resist(self):
        return self.magic_resistance

    def get_physical_resist(self):
        return self.physical_resistance

    def get_rewards(self):
        return self.rewards

    def get_experience(self):
        return self.experience

    def get_triggers(self):
        return self.triggers


enemyIndex = {
    -1: Enemies(name='Test Dummy', level=1, health=99999999, damage=0, magic_resistance=0, physical_resistance=0,
                rewards=None, experience=0, triggers=None),
    0: Enemies(name='Slime', level=1, health=10, damage=5, magic_resistance=1, physical_resistance=1,
               rewards=None, experience=4, triggers=None),
    1: Enemies(name='Skeleton', level=2, health=20, damage=7, magic_resistance=2, physical_resistance=1,
               rewards=None, experience=6, triggers=None)
}

rareEnemyIndex = {
    0: Enemies(name='Skelington', level=5, health=50, damage=15, magic_resistance=3, physical_resistance=1,
               rewards=[3], experience=15, triggers=[50])
}

forestEnemyIndex = [0, 1]
rareForestEnemyIndex = [0]


def rand_forest_enemy():
    return random.choice(forestEnemyIndex)


def rand_rare_forest_enemy():
    return random.choice(rareForestEnemyIndex)


mountainEnemyIndex = []
rareMountainEnemyIndex = []


def rand_mountain_enemy():
    return random.choice(mountainEnemyIndex)


def rand_rare_mountain_enemy():
    return random.choice(rareMountainEnemyIndex)


plainsEnemyIndex = []
rarePlainsEnemyIndex = []


def rand_plains_enemy():
    return random.choice(plainsEnemyIndex)


def rand_rare_plains_enemy():
    return random.choice(rarePlainsEnemyIndex)


def get_enemy(key):
    try:
        return enemyIndex[key]
    except IndexError:
        pass


def get_rare_enemy(key):
    try:
        return rareEnemyIndex[key]
    except IndexError:
        pass
