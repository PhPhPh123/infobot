"""

"""
import random

from settings_and_imports import *


class Artifact:
    def __init__(self, name, grade, weight, unique_bonus, stat_requeriments):
        self.name = name
        self.grade = grade
        self.weight = weight
        self.unique_bonus = unique_bonus
        self.stat_requeriments = stat_requeriments


class Armor(Artifact):
    def __init__(self, name, grade, weight, unique_bonus, stat_requeriments):
        super().__init__(name, grade, weight, unique_bonus, stat_requeriments)
        self.armor = 'armor'
        self.speed_modifier = 'speed_modifier'
        self.evasion_modifier = 'evasion_modifier'

    def get_armor(self):
        pass


class Weapon(Artifact):
    def __init__(self, name, grade, weight, unique_bonus,
                 stat_requeriments, damage, penetration,
                 prescision_modifier):
        super().__init__(name, grade, weight, unique_bonus, stat_requeriments)
        self.damage = damage
        self.penetration = penetration
        self.prescision_modifier = prescision_modifier

    def get_damage(self, group_of_weapon, grade):
        base_damage_lazgun = 18
        base_damage_lazgpistol = 12
        base_damage_autopistol = 18
        base_damage_autogun = 30

        random_modifier = random.uniform(0.9, 1.1)

        grade_damage = 0
        if grade == 'зеленый':
            grade_damage = 1.05
        elif grade_damage == 'синий':
            grade_damage = 1.10
        elif grade_damage == 'фиолетовый':
            grade_damage = 1.15
        elif grade_damage == 'красный':
            grade_damage = 1.2

        if group_of_weapon == 'Лазган':
            self.damage = base_damage_lazgun * grade_damage * random_modifier
            print(self.damage)


class Jewerly(Artifact):
    def __init__(self, name, grade, weight, unique_bonus, stat_requeriments):
        super().__init__(name, grade, weight, unique_bonus, stat_requeriments)
        self.jewerly_bonus = ''


class RangeWeapon(Weapon):
    def __init__(self, name, grade, weight, unique_bonus,
                 stat_requeriments, damage, penetration, prescision_modifier, weapon_range, attack_speed):
        super().__init__(name, grade, weight,
                         unique_bonus, stat_requeriments, damage,
                         penetration, prescision_modifier)
        self.weapon_range = weapon_range
        self.attack_speed = attack_speed


class Lazgun(RangeWeapon):
    def __init__(self, name, grade, weight, unique_bonus, stat_requeriments,
                 damage, penetration, prescision_modifier, weapon_range, attack_speed):
        super().__init__(name, grade, weight, unique_bonus, stat_requeriments,
                         damage, penetration, prescision_modifier, weapon_range, attack_speed)
        self.laz_mechanics = True


laz = Lazgun(name="Лазган", grade='зеленый', weight=10, unique_bonus=None, stat_requeriments='STR 10',
             damage='3d6', penetration='half', prescision_modifier=0, weapon_range=10, attack_speed=1)
laz.get_damage('Лазган', 'зеленый')

print(laz.__dict__)
