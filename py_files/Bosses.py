import Enemies


class Bosses(Enemies):
    def __init__(self, name, level, health, damage, magic_resistance, physical_resistance, rewards,
                 experience, triggers, isMiniBoss, enrage):
        super().__init__(self, name, level, health, damage, magic_resistance, physical_resistance, rewards,
                         experience, triggers)
        self.isMiniBoss = isMiniBoss
        self.enrage = enrage

    def get_is_mini_boss(self):
        return self.isMiniBoss

    def get_enrage(self):
        return self.enrage

