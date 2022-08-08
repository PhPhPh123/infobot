"""

"""
from abc import ABC

from settings_and_imports import *


class Artifact:
    def __init__(self, name):
        self.name = name
        self.grade = ''
        self.weight = ''
        self.unique_bonus = ''
        self.stat_requeriments = ''


class Armor(Artifact, ABC):
    def __init__(self):
        super().__init__()
        self.armor = ''
        self.speed_modifier = ''
        self.evasion_modifier = ''

    def get_armor(self):
        pass


class Weapon(Artifact, ABC):
    def __init__(self):
        super().__init__()
        self.damage = ''
        self.penetration = ''
        self.prescision_modifier = ''

    def get_damage(self):
        pass


class Jewerly(Artifact, ABC):
    def __init__(self):
        super().__init__()
        self.jewerly_bonus = ''


class RangeWeapon(Weapon):
    def __init__(self):
        super().__init__()
        self.range = ''
        self.attack_speed = ''


class Lazgun(RangeWeapon):
    def __init__(self):
        super().__init__()
        self.laz_mechanics = True


laz = Lazgun()
print(laz.__dict__)
